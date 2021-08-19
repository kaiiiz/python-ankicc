from ankicc import __version__
from ankicc.console import parse_args, main
import ankipandas
import os


def test_version():
    assert __version__ == '0.2.2'


def test_cc():
    APKG_PATH = 'tests/test.apkg'
    WORKSPACE = 'tests/workspace'
    OUTPUT_PATH = 'tests/test_out.apkg'

    args = parse_args([
        '--apkg_path', APKG_PATH,
        '--workspace', WORKSPACE,
        '--output_path', OUTPUT_PATH,
        '--convertor', 't2s.json',
    ])
    main(args)

    col = ankipandas.Collection(os.path.join(WORKSPACE, 'test', 'collection.anki21'))
    fields = col.notes.nflds
    assert str(fields[1625832630859]) == "['正面测试', '背面测试']"

    col_info = ankipandas.raw.get_info(col.db)
    assert col_info['decks']['1625832609582']['name'] == "测试"
