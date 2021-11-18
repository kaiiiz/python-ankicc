import ankipandas
import opencc
import json
import numpy as np


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def cc_list(cc: opencc.OpenCC, x: list) -> list:
    return list(map(cc.convert, x))


def cc_notes(cc: opencc.OpenCC, notes: ankipandas.AnkiDataFrame) -> ankipandas.AnkiDataFrame:
    notes['nflds'] = notes['nflds'].apply(lambda x : cc_list(cc, x))
    notes['nmodel'] = notes['nmodel'].apply(cc.convert)
    return notes


def cc_collection(cc: opencc.OpenCC, col: ankipandas.Collection) -> ankipandas.Collection:
    col_table_str = json.dumps(ankipandas.raw.get_info(col.db), cls=NpEncoder, ensure_ascii=False)
    col_table_cc = json.loads(cc.convert(col_table_str))
    ankipandas.raw.set_info(col.db, col_table_cc)
    notes_cc = cc_notes(cc, col.notes)
    col.notes.update(notes_cc)
    return col
