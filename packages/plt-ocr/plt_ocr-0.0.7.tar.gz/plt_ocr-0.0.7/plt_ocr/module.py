
import torch
from torch import nn
from torchvision.models import MobileNet_V2_Weights, mobilenet_v2

CHARS = '0123456789'
NUM_CLASSES = len(CHARS) + 1
NA = NUM_CLASSES - 1
MAX_PLATE_LEN = 8


class OCR(nn.Module):
    def __init__(self):
        super().__init__()
        net = mobilenet_v2(weights=MobileNet_V2_Weights.DEFAULT)
        net.features[0][0] = nn.Conv2d(
            1, 32,
            kernel_size=3,
            stride=2,
            padding=1,
            bias=False)

        net.classifier = nn.Identity()  # type: ignore

        self.net = nn.Sequential(
            net,
            nn.Linear(1280, NUM_CLASSES * MAX_PLATE_LEN))

    def forward(self, x):
        out = self.net(x)
        return out.reshape(-1, NUM_CLASSES, MAX_PLATE_LEN)


def fix_state_dict(state_dict):
    return {
        k.replace('net.net', 'net'): v
        for k, v in state_dict.items()}


def load_from_model_ckpt():
    from importlib.resources import files
    from io import BytesIO

    import plt_ocr

    ckpt = torch.load(
        BytesIO(files(plt_ocr).joinpath('model.ckpt').read_bytes()),
        map_location=torch.device('cpu'))

    model = OCR()
    model.load_state_dict(fix_state_dict(ckpt['state_dict']))

    return model


if __name__ == '__main__':
    model = load_from_model_ckpt()
    model.eval()
    print(model)
