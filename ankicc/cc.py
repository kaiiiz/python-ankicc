import ankipandas
import opencc


def cc_list(cc: opencc.OpenCC, x: list) -> list:
    return list(map(cc.convert, x))


def cc_notes(cc: opencc.OpenCC, notes: ankipandas.AnkiDataFrame) -> ankipandas.AnkiDataFrame:
    notes['nflds'] = notes['nflds'].apply(lambda x : cc_list(cc, x))
    notes['nmodel'] = notes['nmodel'].apply(cc.convert)
    return notes


def cc_collection(cc: opencc.OpenCC, col: ankipandas.Collection) -> ankipandas.Collection:
    col_table_cc = eval(cc.convert(str(ankipandas.raw.get_info(col.db))))
    ankipandas.raw.set_info(col.db, col_table_cc)
    notes_cc = cc_notes(cc, col.notes)
    col.notes.update(notes_cc)
    return col
