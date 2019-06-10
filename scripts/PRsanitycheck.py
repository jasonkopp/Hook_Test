#!/usr/bin/env python3
import csv, re, os

# X- are all the codes actually 4 characters (or an escape)?
# X - are the codes unique, at least in their table, (and give a warning if the code is also in another table)
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

def notfourcharacters(codes, codeExceptions=[""]):
    pattern = re.compile("^[A-Za-z0-9 +-]{4}$")
    mistakeCodes = []
    for code in codes:
        if pattern.match(code[0]) == None:
            if code[0] not in codeExceptions:
                mistakeCodes.append(code[0])
    print("\nFour Character Codes Test:")
    if mistakeCodes == []:
        print("\tAll 4ccs are four characters - PASS")
        return 0
    else:
        print("\tSomething is wrong with these codes: %s - FAIL" % mistakeCodes)
        return 1

def uniqueTest(codes, dupexceptions=[]):
    allcodes = [code[0] for code in codes if code[0] not in dupexceptions]
    duplicates = sorted([[codes[i][0], codes[i][2]] for i in range(len(codes)) if allcodes.count(codes[i][0]) > 1])

    if duplicates == []:
        print("Duplicate 4CCs Test:\n\tNo duplicates found - PASS")
        return 0
    else:
        print("Duplicate 4CCs Test:")
        dupsdif = []
        dupssame = []
        for i in duplicates:
            if duplicates.count(i) == 1:
                print("\t'%s' from '%s' is a duplicate" % (i[0], i[1]))
                # dupsdif.append([i[0], i[1]])
                pass
            elif duplicates.count(i) > 1:
                print("\tWARNING '%s' from '%s' is a duplicate WARNING" % (i[0], i[1]))
                dupssame.append([i[0], i[1]])

        if dupssame != []:
            print("\tDuplicates found in the same CSV - FAIL")
            return 1
        elif dupssame == []:
            print("\tNo duplicates found in the same CSV - PASS")
            return 0

def prsanitycheck():
    localrepo = "../CSV/"
    travisrepo = "CSV/"
    codesInCSV = getCSV4CCs(travisrepo)
    codeExceptions = ["gif","png","tga"]
    not4ccs = notfourcharacters(codesInCSV, codeExceptions)
    dupexceptions = ["m4ae", "tsel", "xml "]
    duplicates = uniqueTest(codesInCSV, dupexceptions)
    if not4ccs + duplicates == 0:
        exit(0)
    elif not4ccs + duplicates != 0:
        exit(1)

prsanitycheck()
