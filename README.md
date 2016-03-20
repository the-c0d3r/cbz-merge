# cbz-merge
A simple python script to merge multiple cbz files into one single cbz file. 



```
CBZ merge
----------

usage: cbz-merge.py [-h] [-d DIRECTORY] [-v]

Combine multiple CBZ to one file

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        Directory containing CBZ
  -v, --verbose         Enable Verbose Mode
```

This program assumes your directory and naming convention like below. For example, the cbz files you want to merge are inside `Green_Worldz`, the program assumes the following.

```
Green_Worldz
├── Green_Worldz_c001.cbz
    (When Extracted)
    ├──Green_Worldz_c001_p01.jpg
    ├──Green_Worldz_c001_p02.jpg
    ├──Green_Worldz_c001_p03.jpg
    ├──Green_Worldz_c001_p04.jpg
    ├──Green_Worldz_c001_p05.jpg
├── Green_Worldz_c002.cbz
├── Green_Worldz_c003.cbz
├── Green_Worldz_c004.cbz
├── Green_Worldz_c005.cbz
```

It assumes cbz files have `_cxxx` in them, which is used to correctly sort the cbz files and `_pxxx` is used to sort image files. The built-in sort function doesn't satisify this need, so I need to use it as the key. 

This program is best used with the MangaFox downloaders, which can package the manga into separate cbz files for each chapters. And then use this to combine them into one and put it to your favorite E-Reader. I use this tool for my kindle, after converting it to mobi with **kcc** of course. 