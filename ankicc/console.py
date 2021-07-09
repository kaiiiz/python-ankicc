from ankipandas import Collection
from argparse import ArgumentParser, Namespace
from pathlib import Path
import opencc
import zipfile
import os

from .cc import cc_collection

TARGET_COLLECTION = ['collection.anki2', 'collection.anki20', 'collection.anki21']


def run():
    args = parse_args()

    apkg_name = os.path.splitext(os.path.basename(args.apkg_path))[0]
    collection_dir = os.path.join(args.workspace, apkg_name)
    backup_dir = os.path.join(args.workspace, 'backup')

    with zipfile.ZipFile(args.apkg_path, 'r') as zf:
        zf.extractall(collection_dir)

    cc = opencc.OpenCC(args.convertor)

    for col_name in TARGET_COLLECTION:
        col_path = os.path.join(collection_dir, col_name)
        if os.path.isfile(col_path):
            col = cc_collection(cc, Collection(col_path))
            col.write(modify=True, backup_folder=backup_dir)
   
    with zipfile.ZipFile(args.output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(collection_dir):
            for file_name in files:
                zf.write(os.path.join(root, file_name), file_name)


def parse_args(args=None) -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "--apkg_path", type=Path, required=True,
    )
    parser.add_argument(
        "--workspace", type=Path, default=".",
    )
    parser.add_argument(
        "--output_path", type=Path, required=True,
    )
    parser.add_argument(
        "--convertor", choices=opencc.CONFIGS, default="s2t.json",
    )

    if args:
        args = parser.parse_args(args)
    else:
        args = parser.parse_args()
    return args


if __name__ == "__main__":
    run()
