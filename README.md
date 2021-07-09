# ankicc

將 Anki deck package (*.apkg) 的所有欄位在繁體及簡體中文間進行相互轉換。

## Installation 安裝

```
pip install ankicc
```

## Usage 使用

```
usage: ankicc [-h] --apkg_path APKG_PATH [--workspace WORKSPACE] --output_path OUTPUT_PATH
              [--convertor {t2jp.json,t2tw.json,hk2t.json,tw2s.json,hk2s.json,s2hk.json,tw2t.json,t2s.json,s2tw.json,s2twp.json,t2hk.json,s2t.json,jp2t.json,tw2sp.json}]

optional arguments:
  -h, --help            show this help message and exit
  --apkg_path APKG_PATH
  --workspace WORKSPACE
  --output_path OUTPUT_PATH
  --convertor {t2jp.json,t2tw.json,hk2t.json,tw2s.json,hk2s.json,s2hk.json,tw2t.json,t2s.json,s2tw.json,s2twp.json,t2hk.json,s2t.json,jp2t.json,tw2sp.json}
```

* apkg_path: 待轉換的 apkg 文件位置
* workspace: ankicc 的工作目錄位置，預設為當前執行目錄，轉換過程中的文件都會保存在該執行目錄 (請留意：轉換後不會自動刪除)
* output_path: 轉換後的輸出文件位置
* convertor: OpenCC 的翻譯器設定，預設為簡體轉繁體 (s2t.json)，其他翻譯器設定請參考 [OpenCC #Configurations](https://github.com/BYVoid/OpenCC#configurations-%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6)

## Third Party Library 第三方庫

* [OpenCC](https://github.com/BYVoid/OpenCC) Apache-2.0 License
* [AnkiPandas](https://github.com/klieret/AnkiPandas) MIT License
