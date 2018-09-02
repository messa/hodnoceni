#!/usr/bin/env python3

import argparse
import json
import openpyxl


def main():
    p = argparse.ArgumentParser()
    p.add_argument('input_file')
    p.add_argument('--output-file', default='dataset.json')
    args = p.parse_args()
    wb = openpyxl.load_workbook(args.input_file)
    ws, = wb.worksheets
    records = []
    for row_n, ws_row in enumerate(ws.rows):
        row = [cell.value for cell in ws_row]
        if row_n == 0:
            header = row
            continue
        record = dict(zip(header, row))
        records.append(record)
    with open(args.output_file, 'w') as f:
        json.dump(records, f, indent=2)


if __name__ == '__main__':
    main()
