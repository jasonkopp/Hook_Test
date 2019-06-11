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
                        csvCode = row['code'].replace('$20', ' ')
                        if 'description' in headers:
                            csvDesc = row['description'].lower()
                        else:
                            csvDesc = "No desc"
                        if 'specification' in headers:
                            csvSpec = row['specification'].lower()
                        else:
                            csvSpec = "No spec"
                        csvFile = fileName.lower()

                        codesInCSV.append([csvCode, csvDesc, csvSpec, csvFile])
    return codesInCSV

def notfourcharacters(codes, exceptions=[""]):
    pattern = re.compile("^[A-Za-z0-9 +-]{4}$")
    mistakeCodes = []
    for code in codes:
        if pattern.match(code[0]) == None:
            if code[0] not in exceptions:
                mistakeCodes.append(code[0])
    print("\nFour Character Codes Test:")
    if mistakeCodes == []:
        print("\tAll 4ccs are four characters - PASS")
        return 0
    else:
        print("\tSomething is wrong with these codes: %s - FAIL" % mistakeCodes)
        return 1

def duplicatecodes(codes, exceptions=[]):
    allcodes = [code[0] for code in codes if code[0] not in exceptions]
    dups = []
    for i in range(len(codes)):
        # print(codes[i][0])
        if allcodes.count(codes[i][0]) > 1:
            dups.append(codes[i])
    dupssorted = sorted(dups)

    print("\nDuplicate 4CCs Test:")
    if dupssorted == []:
        print("\tNo duplicates found - PASS")
        return 0
    else:
        dupstest = []
        dupsame = []
        dupdiff = []
        for i in range(len(dupssorted)):
            dupstest.append([dupssorted[i][0], dupssorted[i][3]])
        for i in range(len(dupssorted)):
            if dupstest.count([dupssorted[i][0], dupssorted[i][3]]) == 1:
                print("\t%s" % (dupssorted[i]))
                dupdiff.append(dupssorted[i])
            if dupstest.count([dupssorted[i][0], dupssorted[i][3]]) > 1:
                print("\t----SAME CSV----%s" % (dupssorted[i]))
                dupsame.append([dupssorted[i]])
        if dupsame != []:
            print("\tDuplicates found in the same CSV - FAIL")
            return 1
        elif dupsame == []:
            print("\tNo duplicates found in the same CSV - PASS")
            return 0

def prsanitycheck():
    #GET CODES
    localrepo = "../CSV/"
    travisrepo = "CSV/"
    codesspecs = getCSV4CCs(travisrepo)

    #TEST for four characters
    codeExceptions = [] #Type in exceptions if you need to
    not4ccs = notfourcharacters(codesspecs, codeExceptions)

    #Test for Duplicates
    dupexceptions = ["xml ", "file", " or "]
    duplicates = duplicatecodes(codesspecs, dupexceptions)

    # Exit Codes
    returnvalue = (not4ccs + duplicates) #+ unregisteredspecs + emptycols
    if returnvalue == 0:
        print("\nPR passed all checks")
        exit(0)
    elif returnvalue == 1:
        print("\nPR failed 1 check")
        exit(1)
    elif returnvalue > 1:
        print("\nPR failed %d checks" % returnvalue)
        exit(1)

prsanitycheck()
