#!/usr/bin/env python
# Given a CSV file, two columns are merged by copying the contents of the
# second column into the first, unless the cell in the first column is not
# empty, in which case an output is shown with the existing value in both
# columns. The column ID specification is 0-based.
import argparse
import csv
import time

"""
    Class for merging two columns from a CSV file (assumed to have a single
    header line)
"""
class MergeColumns:

    def __init__(self, inputFile, outputFile, toCol, fromCol):
        # Input CSV file
        self.inputFile = inputFile
        # Output CSV file
        self.outputFile = outputFile
        # From column ID (ID is 0-based)
        self.toColumn = toCol
        # To column ID (ID is 0-based)
        self.fromColumn = fromCol
        print "Input:",self.inputFile
        print "Output:",self.outputFile
        print "From column:",self.fromColumn,"to:",self.toColumn

    def merge(self):
        # Set up input file reader
        csvInputFile = open(self.inputFile, 'rb')
        csvInputFileReader = csv.reader(csvInputFile, dialect='excel')

        # Set up output files
        csvOutputFile = open(self.outputFile, 'wb')
        csvOutputWriter = csv.writer(csvOutputFile, dialect='excel')

        # Read the header line
        header = csvInputFileReader.next()
        del header[self.fromColumn]
        csvOutputWriter.writerow(header)

        # Each row is a list of strings
        # Values are data from the row being read
        rowId = 1
        merged = 0
        for row in csvInputFileReader:
            rowId = rowId + 1
            if row[self.toColumn] <> '' and row[self.fromColumn] <> '':
                print "Could not merge:",row[self.fromColumn],"into:", \
                    row[self.toColumn],"row:",rowId
            elif row[self.toColumn] == '' and row[self.fromColumn] <> '':
                row[self.toColumn] = row[self.fromColumn]
                merged = merged + 1
            del row[self.fromColumn]
            csvOutputWriter.writerow(row)
            csvOutputFile.flush()
        csvInputFile.close()
        csvOutputFile.close()
        print merged,"rows successfully merged"

"""
    Parses input arguments, constructs a MergeColumns to merge two columns
    in a CSV file.
    Example execution: python mergeColumns.py -i ../data/CrowdsourcedData.csv
        -o ../data/MergedDataset.csv -c 6
"""
def main():
    # Parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", required=True, help="Input csv file to have columns merged")
    parser.add_argument("-t", required=True, type=int, help="Columns ID to \
        where data will be merged, ID is 0-based")
    parser.add_argument("-f", required=True, type=int, help="Columns ID from \
        where data will be merged, ID is 0-based")
    parser.add_argument("-o", "--output", required=True, help="Output csv file")
    args = parser.parse_args()

    # Instantiate and configure work csv merger
    startTime = time.time()
    merger = MergeColumns(args.i, args.output, args.t, args.f)
    merger.merge()
    print "Done in ", time.time() - startTime, " secs"

if __name__ == "__main__":
    main()