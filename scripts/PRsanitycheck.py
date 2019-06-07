#!/usr/bin/env python3
import csv, re, os

# X- are all the codes actually 4 characters (or an escape)?
# are the codes unique, at least in their table, (and give a warning if the code is also in another table)
# are the spec shortnames registered, or will they be?
# are all the mandatory columns filled in?

def getCSV4CCs(directory):
    csvCodes = []
    codesInCSV = []
    for fileName in os.listdir(directory):
        if fileName.endswith(".csv") and fileName != "oti.csv" and fileName != "stream-types.csv":
            with open(directory+fileName, 'r') as csvfile:
                csvReader = csv.DictReader(csvfile)
                headers = csvReader.fieldnames
                if 'code' in headers:
                    for row in csvReader:
                        code = row['code']
                        csvCode = code.replace('$20', ' ')
                        csvFile = fileName.lower()
                        csvLine = str(list(row.values()))
                        if 'specification' in headers:
                            csvSpec = row['specification'].lower()
                        else:
                            csvSpec = "No spec"

                        csvCodes.append(csvCode)
                        codesInCSV.append([csvCode, csvSpec, csvFile, csvLine])
    return codesInCSV

def notfourcharacters(codes, exceptions=[""]):
    pattern = re.compile("^[A-Za-z0-9 +-]{4}$")
    mistakeCodes = []
    for code in codes:
        if pattern.match(code[0]) == None:
            if code[0] not in exceptions:
                mistakeCodes.append(code[0])
    if mistakeCodes == []:
        print("All 4ccs are four characters.")
        return 0
    else:
        print("Something is wrong with these codes: %s" % mistakeCodes)
        return 1

def prsanitycheck():
    localrepo = "../CSV/"
    travisrepo = "CSV/"
    codesInCSV = getCSV4CCs(travisrepo)
    exceptions = ["gif","png","tga"]
    mistakes = notfourcharacters(codesInCSV, exceptions)
    if mistakes == 0:
        exit(0)
    elif mistakes != 0:
        exit(1)
    print("This is the working directory: %s" % os.getcwd())
    print("This is the file list: %s" % os.listdir())


prsanitycheck()
