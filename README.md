Hodnotící web
=============

Simple Python website for evaluation of some things

How it works:

1. obtain data, convert to JSON format
2. run the website, use it to evaluate data
3. do something useful with the result JSON data

Usage
-----

Obtain source data, for example .xlsx file.

Convert .xlsx file to `dataset.json`. Warning: if the file exists, it will be overwritten.

```shell
$ ./to_json.py Registrace_podzim_2018.xlsx
```

Create file `questions.json`.

Run the website:

```shell

```
