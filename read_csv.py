import csv
import pandas as pd

"""
with open('test.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
            line_count += 1
    print(f'Processed {line_count} lines.')

with open('test.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Columns: {", ".join(row)}')
            line_count += 1
        print(f'{row["article"]} words in the {row["adj"]} department.')
        line_count += 1
    print(f'Processed {line_count} lines.')

with open('test.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    print(csv_reader)
    print(type(csv_reader))
"""

df = pd.read_csv('test.csv', delimiter=",")
#print(df)
data_dict = df.to_dict()
#print(data_dict)
#print(type(data_dict))
#print(data_dict["subject"])

with open('test.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

print(csv_reader["subject"])


