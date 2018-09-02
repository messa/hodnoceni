#!/usr/bin/env python3

import json
import openpyxl


def main():
    wb = openpyxl.load_workbook('registrace.xlsx')
    ws, = wb.worksheets
    data = []
    for row_n, ws_row in enumerate(ws.rows):
        row = [cell.value for cell in ws_row]
        if row_n == 0:
            print(row)
            continue
        dt, number, experience, source, expectations, dedication, score, notes = row
        assert number == row_n
        assert score is None
        assert notes is None
        data.append({
            'timestamp': dt.isoformat(),
            'id': number,
            'experience': experience,
            'source': source,
            'expectations': expectations,
            'dedication': dedication,
        })
    with open('registrace.json', 'w') as f:
        json.dump(data, f, indent=2)


if __name__ == '__main__':
    main()
