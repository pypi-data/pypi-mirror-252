import json
from functools import cache
from random import shuffle
from typing import List, Literal, Sized, TypedDict, cast

import lightning as pl
import lightning.pytorch.callbacks as cb
import torch
import torch.nn.functional as F
from lightning.pytorch import loggers as pl_loggers
from PIL import Image
from pynvml.smi import nvidia_smi
from torch.optim import Adam
from torch.utils.data import DataLoader, Dataset
from torchmetrics.classification import MulticlassAccuracy
from torchvision.models import MobileNet_V2_Weights
from torchvision.transforms import v2

from plt_ocr.model import (CHARS, MAX_PLATE_LEN, NA, NUM_CLASSES, OCRModule,
                           pre_process)
from plt_ocr.version import version

OCR_VALID_SIZE = 400


class Record(TypedDict):
    path: str
    number: str


def devices(max_devices=16):
    nvsmi = cast(nvidia_smi, nvidia_smi.getInstance())

    devices = nvsmi.DeviceQuery('memory.used')
    devices = devices['gpu']
    devices = [i for i, d in enumerate(
        devices) if d['fb_memory_usage']['used'] < 400]

    devices = devices[:max_devices]

    return devices


def load_records(ocr_jsonl):
    with open(ocr_jsonl) as f:
        records = [json.loads(record) for record in f]

    return cast(List[Record], records)


class SizedDataset(Dataset, Sized):
    pass


class OCRData(SizedDataset):
    def __init__(self, records: List[Record], augment=lambda x: x):
        self.records = records
        self.augment = augment

    def __len__(self):
        return len(self.records)

    @cache
    def item(self, idx):

        record = self.records[idx]
        x = pre_process(Image.open((record['path'])))

        target = [
            CHARS.index(c)
            for c in record['number'] if c in CHARS]

        target += [NA] * (MAX_PLATE_LEN - len(target))

        y = torch.tensor(target, dtype=torch.long)

        return x, y

    def __getitem__(self, idx):
        x, y = self.item(idx)
        return self.augment(x), y


class OCRDataModule(pl.LightningDataModule):
    def __init__(self, data_jsonl='data.jsonl'):
        super().__init__()

        records = load_records(data_jsonl)

        shuffle(records)
        train, valid = records[:-OCR_VALID_SIZE], records[-OCR_VALID_SIZE:]

        self.train = OCRData(
            train,
            augment=v2.AutoAugment(v2.AutoAugmentPolicy.CIFAR10))

        self.valid = OCRData(valid)

    def train_dataloader(self):
        return DataLoader(
            self.train,
            batch_size=32,
            shuffle=True,
            num_workers=4)

    def val_dataloader(self):
        return DataLoader(
            self.valid,
            batch_size=32,
            num_workers=4)


class OCRLightningModule(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.net = OCRModule(weights=MobileNet_V2_Weights.DEFAULT)
        self.accuracy = MulticlassAccuracy(num_classes=NUM_CLASSES)

    def step(self, batch, batch_idx, name: Literal['train', 'valid'], sync_dist=True):
        crops, digits = batch
        digits_hat = self(crops)

        digits = cast(torch.Tensor, digits)

        assert digits.shape == (
            len(crops), MAX_PLATE_LEN), f'Bad shape {digits.shape}'

        assert digits_hat.shape == (
            len(crops), NUM_CLASSES, MAX_PLATE_LEN), f'Bad shape {digits_hat.shape}'

        loss = F.cross_entropy(digits_hat, digits)

        self.log(
            f'{name}/acc',
            self.accuracy(digits_hat, digits),
            prog_bar=True,
            sync_dist=sync_dist)

        self.log(f'{name}/loss', loss, prog_bar=True, sync_dist=sync_dist)

        return loss

    def training_step(self, batch, batch_idx):
        return self.step(batch, batch_idx, 'train')

    def validation_step(self, batch, batch_idx):
        return self.step(batch, batch_idx, 'valid')

    def forward(self, x):
        return self.net(x)

    def configure_optimizers(self):
        return Adam(
            self.parameters(),
            lr=1e-4,
            weight_decay=1e-5)


def sample_data():
    from pathlib import Path
    from shutil import rmtree

    from torchvision.transforms.functional import to_pil_image

    rmtree('tmp', ignore_errors=True)

    tmp = Path('tmp')
    train_path = tmp / 'train'
    valid_path = tmp / 'valid'
    train_path.mkdir(parents=True)
    valid_path.mkdir(parents=True)

    data = OCRDataModule()
    train = data.train_dataloader()
    valid = data.val_dataloader()

    train_batch = next(iter(train))
    valid_batch = next(iter(valid))

    for i, (x, y) in enumerate(zip(*train_batch)):
        label = ''.join(CHARS[i] for i in y if i != NA)
        to_pil_image(x).save(train_path / f'{i}_{label}.jpg')

    for i, (x, y) in enumerate(zip(*valid_batch)):
        label = ''.join(CHARS[i] for i in y if i != NA)
        to_pil_image(x).save(valid_path / f'{i}_{label}.jpg')


def train():
    pl.seed_everything(42)
    name = 'ocr'
    monitor = 'valid/loss'
    monitor_mode = 'min'

    logger = pl_loggers.TensorBoardLogger(
        save_dir='logs/',
        name=name,
        version=version)

    swa = cb.StochasticWeightAveraging(swa_lrs=1e-2)

    early_stopping = cb.EarlyStopping(
        monitor=monitor,
        mode=monitor_mode,
        patience=50)

    model_checkpoint = cb.ModelCheckpoint(
        save_last=False,
        save_weights_only=True,
        dirpath='ckpt/',
        filename=version,
        monitor=monitor,
        mode=monitor_mode)

    trainer = pl.Trainer(
        val_check_interval=0.25,
        accelerator='auto',
        devices=devices(),
        max_epochs=200,
        logger=logger,
        callbacks=[
            swa,
            early_stopping,
            model_checkpoint])

    datamodule = OCRDataModule()
    model = OCRLightningModule()

    trainer.fit(model, datamodule)


if __name__ == '__main__':
    sample_data()
