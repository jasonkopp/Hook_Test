#!/usr/bin/env python3
import csv, re, os

# are all the codes actually 4 characters (or an escape)?
# are the codes unique, at least in their table, (and give a warning if the code is also in another table)
# are the spec shortnames registered, or will they be?
# are all the mandatory columns filled in?

def csv4ccs():
    CSVFileDirectory = "../CSV/"
    csvCodes = []
    codesInCSV = []
    for fileName in os.listdir(CSVFileDirectory):
        if fileName.endswith(".csv") and fileName != "oti.csv" and fileName != "stream-types.csv":
            with open(CSVFileDirectory+fileName, 'r') as csvfile:
                csvReader = csv.DictReader(csvfile)
                headers = csvReader.fieldnames
                if 'code' in headers:
                    for row in csvReader:
                        csvCode = row['code']
                        csvFile = fileName.lower()
                        csvLine = str(list(row.values()))
                        if 'specification' in headers:
                            csvSpec = row['specification'].lower()
                        else:
                            csvSpec = "No spec"

                        csvCodes.append(csvCode)
                        codesInCSV.append([csvCode, csvSpec, csvFile, csvLine])

    pattern = re.compile("^[A-Za-z0-9+-]{4}$")
    for code in codesInCSV:
        if pattern.match(code[0]) == None:
            print(code[0])

    print("There are %d CSV Codes" % (len(csvCodes)))

def prsanitycheck():
    csv4ccs()
    exit(0)

prsanitycheck()
