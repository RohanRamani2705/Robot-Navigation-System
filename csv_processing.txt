# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 12:51:18 2025

@author: Rohan
"""

import csv

# Cleaning up empty rows in CSV
input_file = open('Predictions.csv', 'r')
output_file = open('CleanedData.csv', 'w', newline='')
csv_writer = csv.writer(output_file)

for row in csv.reader(input_file):
    if row:
        csv_writer.writerow(row)

input_file.close()
output_file.close()

# Removing unnecessary columns
with open("CleanedData.csv", "r") as source:
    reader = csv.reader(source)
    with open("FilteredData.csv", "w", newline='') as result:
        writer = csv.writer(result)
        for row in reader:
            writer.writerow(row[:1])  # Keep only the first column
