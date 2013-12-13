#!/usr/bin/env python
# Given a CSV file with a work per row, removes all rows were the work has
# no information in all fields
import argparse
import csv
import time

"""
    Class for cleaning crowdsourcing work from irrelevant data.
"""
class WorkCleaner:

    def __init__(self, inputFile, outputFile):
        # Input CSV file
        self.inputFile = inputFile
        # Output CSV file
        self.outputFile = outputFile
        # Array with column IDs to check (ID is 0-based)
        self.checkColumns = None
        # Array with list of words considered as empty (no value)
        self.noValueWords = None
        # Indicates if debugging is enabled
        self.debug = None
        print "Input:",self.inputFile
        print "Output:",self.outputFile

    def parseColRange(self, rangeStr):
        result = set()
        for part in rangeStr.split(','):
            x = part.split('-')
            result.update(range(int(x[0]), int(x[-1])+1))
        self.checkColumns = sorted(result)
        if len(self.checkColumns) == 0:
            raise Exception("Must provide column IDs that are required to have data!")

    def parseNoValueWords(self, wordListStr):
        self.noValueWords = wordListStr.split(',')
        self.noValueWords.append('')

    def setDebug(self, dbg):
        self.debug = dbg

    def clean(self):
        # Set up input file reader
        csvInputFile = open(self.inputFile, 'rb')
        csvInputFileReader = csv.reader(csvInputFile, dialect='excel')

        # Set up output files
        csvOutputFile = open(self.outputFile, 'wb')
        csvOutputWriter = csv.writer(csvOutputFile, dialect='excel')

        # Read and write back the header line
        header = csvInputFileReader.next()
        csvOutputWriter.writerow(header)
        # Each row is a list of strings
        # Values are data from the row being read
        rowId = 1
        removed = 0
        kept = 0
        for row in csvInputFileReader:
            rowRemoved = True
            for i in self.checkColumns:
                if row[i] not in self.noValueWords:
                    csvOutputWriter.writerow(row)
                    csvOutputFile.flush()
                    rowRemoved = False
                    kept = kept + 1
                    break
            if rowRemoved:
                removed = removed + 1
                if self.debug:
                    print "Removed row:",rowId,"had:",row
            rowId = rowId + 1
        csvInputFile.close()
        csvOutputFile.close()
        print "Cleaned",removed,"rows from input; kept",kept,"rows from total", \
            (removed+kept)

"""
    Parses input arguments, constructs a WorkCleaner to clean a CSV file and
    output one without work that is completely empty.
    Example execution: python cleanEmptyWork.py -i ../data/CrowdsourcedData.csv
        -o ../data/CleanDataset.csv -c 6-15 -w placeholder -d
"""
def main():
    # Parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", required=True, help="Input csv file to clean")
    parser.add_argument("-c", required=True, help="Comma separated list of \
            columns IDs that are required to have value, ID is 0-based")
    parser.add_argument("-o", "--output", required=True, help="Output csv file")
    parser.add_argument("-w", help="List of comma separated words that are \
            considered as empty values")
    parser.add_argument("-d", action='store_true', help="Prints additional \
            information to help debugging or facilitate verification of the \
            cleaner")
    args = parser.parse_args()

    # Instantiate and configure work csv cleaner
    startTime = time.time()
    cleaner = WorkCleaner(args.i, args.output)
    cleaner.parseColRange(args.c)
    cleaner.parseNoValueWords(args.w)
    cleaner.setDebug(args.d)
    cleaner.clean()
    print "Done in ", time.time() - startTime, " secs"

if __name__ == "__main__":
    main()
