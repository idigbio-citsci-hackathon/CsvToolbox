CsvToolbox
==========

Toolbox for simple generic manipulation of CSV files.

Authors: Andréa Matsunaga, Joshua Campbell

a) To anonymize the users in a CSV file (CrowdsourcedData.csv), assuming
the CSV file has one line header and the usernames are in column 6
(0-based column ID), an example execution is:

python anonymizer.py -i ../data/CrowdsourcedData.csv
        -o ../data/AnonymizedDataset.csv -c 6


b) To merge two columns in a CSV file (CrowdsourcedData.csv), copying the
contents from column 16 to column 15, an example execution is:

python mergeColumns.py -i ../data/CrowdsourcedData.csv
        -o ../data/MergedDataset.csv -f 16 -t 15
        
If the destination cell is not empty, the merge will still occur, but an
output is generated with the existing value in both columns.

c) To remove rows from a CSV file (CrowdsourcedData.csv) that contains only
empty values or values from a defined list of words (e.g., "placeholder")
in columns 6 through 15, an example execution is:

python cleanEmptyWork.py -i ../data/CrowdsourcedData.csv
        -o ../data/CleanDataset.csv -c 6-15 -w placeholder -d

Columns IDs are 0-based, and can be specified as a list of comma-separated
values and or ranges (separated with dashes).
