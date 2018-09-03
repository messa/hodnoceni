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
$ python3 evaluation_web.py
```

For argument description see `python3 evaluation_web.py --help`.

Grab some wine, beer, or cocoa, sit down in a beanbag with a tablet device and enjoy evaluating all items :)

The results will be stored in `answers.json` in this format (example):

```
[
  {"aj": "0", "stanoveny_cil": "1"},
  {"aj": "1", "stanoveny_cil": "0"},
  {"aj": "1", "stanoveny_cil": null},
  null
]
```

Value `null` means that no answer was provided for given question - or the datapoint was not submitted at all.

The choice values are stored as strings, even if they were integer in `questions.json`.
