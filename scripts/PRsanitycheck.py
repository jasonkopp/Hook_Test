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
                        csvLine = list(row.values())
                        if 'description' in headers:
                            csvDesc = row['description'].lower()
                        else:
                            csvDesc = "No desc"
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

def duplicatecodes(codes, dupexceptions=[]):
    allcodes = [code[0] for code in codes if code[0] not in dupexceptions]
    # duplicates = sorted([[codes[i][0], codes[i][2]] for i in range(len(codes)) if allcodes.count(codes[i][0]) > 1])

    duplicates = []
    dupcodes = []
    for i in range(len(codes)):
        if allcodes.count(codes[i][0]) > 1:
            duplicates.append([codes[i][3], codes[i][2]])
    duplicates = sorted(duplicates)

    if duplicates == []:
        print("Duplicate 4CCs Test:\n\tNo duplicates found - PASS")
        return 0
    else:
        print("Duplicate 4CCs Test:")
        dupstest = []
        dupsame = []
        dupdiff = []
        for i in range(len(duplicates)):
            dupstest.append([duplicates[i][0][0], duplicates[i][1]])
        for i in range(len(duplicates)):
            if dupstest.count([duplicates[i][0][0], duplicates[i][1]]) == 1:
                print("\t'%s' from '%s'" % (duplicates[i][0], duplicates[i][1]))
                dupdiff.append([duplicates[i][0], duplicates[i][1]])
            if dupstest.count([duplicates[i][0][0], duplicates[i][1]]) > 1:
                print("\t----SAME CSV----'%s' from '%s'" % (duplicates[i][0], duplicates[i][1]))
                dupsame.append([duplicates[i][0], duplicates[i][1]])
        if dupsame != []:
            print("\tDuplicates found in the same CSV - FAIL")
            return 1
        elif dupssame == []:
            print("\tNo duplicates found in the same CSV - PASS")
            return 0

def prsanitycheck():
    #GET CODES
    localrepo = "../CSV/"
    travisrepo = "CSV/"
    codesInCSV = getCSV4CCs(travisrepo)

    #TEST for four characters
    codeExceptions = [] #Type in exceptions if you need to
    not4ccs = notfourcharacters(codesInCSV, codeExceptions)

    #Test for Duplicates
    dupexceptions = ["xml "]
    duplicates = duplicatecodes(codesInCSV, dupexceptions)

    #Exit Codes
    returnvalue = not4ccs + duplicates #+ unregisteredspecs + emptycols
    if returnvalue == 0:
        print("\nPR passed all checks")
        exit(0)
    elif returnvalue != 0:
        if returnvalue == 1:
            print("\nPR failed 1 check")
        elif returnvalue > 1:
            print("\nPR failed %d checks" % returnvalue)
        exit(returnvalue)

prsanitycheck()



    # not4ccs = notfourcharacters(codesInCSV[0], codeExceptions)

    # duplicates = duplicatecodes(codesInCSV[0], dupexceptions)

    # #Test for Specifications
    # specexceptions = ["see (1) below"]
    # unregisteredspecs = registeredspecs(codesInCSV[0], codesInCSV[1], specexceptions)
    #
    # #Test for Filled in Columns
    # # colsexceptions = [""]
    # emptycols = filledcolumns(codesInCSV[0])
