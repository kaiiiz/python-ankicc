from ankipandas import Collection, AnkiDataFrame
from argparse import ArgumentParser, Namespace
from pathlib import Path
import ankipandas
import opencc
import zipfile
import os


TARGET_COLLECTION = ['collection.anki2', 'collection.anki20', 'collection.anki21']


def cc_list(cc: opencc.OpenCC, x: list) -> list:
    return list(map(cc.convert, x))


def cc_notes(cc: opencc.OpenCC, notes: AnkiDataFrame) -> AnkiDataFrame:
    notes['nflds'] = notes['nflds'].apply(lambda x : cc_list(cc, x))
    notes['nmodel'] = notes['nmodel'].apply(cc.convert)
    return notes


def cc_collection(cc: opencc.OpenCC, col: Collection) -> Collection:
    col_table_cc = eval(cc.convert(str(ankipandas.raw.get_info(col.db))))
    ankipandas.raw.set_info(col.db, col_table_cc)
    notes_cc = cc_notes(cc, col.notes)
    col.notes.update(notes_cc)
    return col


def main(args: Namespace):
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
    

def parse_args() -> Namespace:
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
    
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    main(args)
