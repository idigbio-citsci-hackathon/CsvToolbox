#!/usr/bin/env python
# Given a CSV file, generates another CSV anonymizing the column specified
# as usernames while maintaining the other columns (quotes around a value
# may vary from the original file). The column ID specification is 0-based.
import argparse
import csv
import itertools
import time

"""
    Class for anonymizing data from a CSV file (assumed to have a single
    header line)
"""
class Anonymizer:

    def __init__(self, inputFile, outputFile):
        # Input CSV file
        self.inputFile = inputFile
        # Output CSV file
        self.outputFile = outputFile
        # Array with column IDs to check (ID is 0-based)
        self.checkColumns = None
        # Value used to indicate that no user is attached to an entry
        self.noUser = "not-logged-in"
        print "Input:",self.inputFile
        print "Output:",self.outputFile

    def parseColRange(self, rangeStr):
        result = set()
        for part in rangeStr.split(','):
            x = part.split('-')
            result.update(range(int(x[0]), int(x[-1])+1))
        self.checkColumns = sorted(result)
        if len(self.checkColumns) == 0:
            raise Exception("Must provide column IDs that are required to have user data!")

    def anonymize(self):
        # Set up input file reader
        csvInputFile = open(self.inputFile, 'rb')
        csvInputFileReader = csv.reader(csvInputFile, dialect='excel')

        # Set up output files
        csvOutputFile = open(self.outputFile, 'wb')
        csvOutputWriter = csv.writer(csvOutputFile, dialect='excel')
        # Example for forcing double quotes on all fields, and using UNIX-style new line
        # csvOutputWriter = csv.writer(csvOutputFile, dialect='excel', quoting=csv.QUOTE_ALL, lineterminator='\n')

        # Read the header line
        header = csvInputFileReader.next()
        # Retrieve all data columns as rows (cols[0] contains column 0)
        cols = zip(*csvInputFileReader)
        # For each column to be anonymized, sorted and filter duplicates
        for i in self.checkColumns:
            uniqVals = sorted(set(cols[i]))
            uniqVals.remove(self.noUser)
            cleanCol = []
            # Replace value in column with anonymous ID
            for j,item in enumerate(cols[i]):
                try:
                    uid = uniqVals.index(item)
                    cleanCol.append('user' + str(uid))
                except ValueError:
                    cleanCol.append(self.noUser)
            cols[i] = cleanCol
        # Write header back
        csvOutputWriter.writerow(header)
        # Write sorted/filtered columns after transposing the rows back to columns
        # Since each column may have different length, use the length of the
        # longest column and fill other cells with empty string
        csvOutputWriter.writerows(itertools.izip_longest(*cols, fillvalue=''))
        csvInputFile.close()
        csvOutputFile.close()

"""
    Parses input arguments, constructs a Anonymizer to remove user identity
    from a CSV file with crowdsourced information.
    Example execution: python anonymizer.py -i ../data/CrowdsourcedData.csv
        -o ../data/AnonymizedDataset.csv -c 6
"""
def main():
    # Parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", required=True, help="Input csv file to anonymize")
    parser.add_argument("-c", required=True, help="Comma separated list of \
            columns IDs that are to be anonymized, ID is 0-based")
    parser.add_argument("-o", "--output", required=True, help="Output csv file")
    args = parser.parse_args()

    # Instantiate and configure work csv anonymizer
    startTime = time.time()
    anon = Anonymizer(args.i, args.output)
    anon.parseColRange(args.c)
    anon.anonymize()
    print "Done in ", time.time() - startTime, " secs"

if __name__ == "__main__":
    main()