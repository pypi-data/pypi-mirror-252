import json
from pathlib import Path

from tqdm import tqdm


def data_jsonl():
    with open('data.jsonl', 'w') as out:
        def dump(path: Path, number: str):
            record = json.dumps({
                'path': str(path),
                'number': number})

            print(record, file=out)

        with open('data/israeli-plate-ocr/records.jsonl') as f:
            root = Path('data/israeli-plate-ocr')
            for line in tqdm(f):
                record = json.loads(line)
                dump(root / record['plate'], record['number'])
