#!/usr/bin/env python3
import csv, re, os

def getCSV4CCs(directory):
    codesInCSV = []
    speclist = []
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
                        if 'specification' in headers:
                            csvSpec = row['specification'].lower()
                        else:
                            csvSpec = "No spec"
                        codesInCSV.append([csvCode, csvSpec, csvFile, csvLine])
                if fileName == "specifications.csv":
                    for row in csvReader:
                        linkname = row['linkname']
                        spec = row['specification']
                        desc = row['description']
                        speclist.append([linkname, spec, desc])
    return(codesInCSV, speclist)

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

def duplicatecodes(codes, dupexceptions=[""]):
    allcodes = [code[0] for code in codes if code[0] not in dupexceptions]
    duplicates = sorted([[codes[i][3], codes[i][2]] for i in range(len(codes)) if allcodes.count(codes[i][0]) > 1])

    print("\nDuplicate 4CCs Test:")
    if duplicates == []:
        print("\tNo duplicates found - PASS")
        return 0
    else:
        dupsdif = []
        dupssame = []
        for i in duplicates:
            if duplicates.count(i) == 1:
                print("\t'%s' from '%s'" % (i[0], i[1]))
                # dupsdif.append([i[0], i[1]])
                pass
            elif duplicates.count(i) > 1:
                print("\tWARNING '%s' from '%s' - WARNING" % (i[0], i[1]))
                dupssame.append([i[0], i[1]])

        if dupssame != []:
            print("\tDuplicates found in the same CSV - FAIL")
            return 1
        elif dupssame == []:
            print("\tNo duplicates found in the SAME CSV - PASS")
            return 0


def registeredspecs(codesInCSV, speclist, specexceptions=[""]):
    unregisteredspecs = []
    allspecs = [spec[1].lower() for spec in speclist]+specexceptions
    for a in range(len(codesInCSV)):
        if codesInCSV[a][1].lower() not in allspecs:
            unregisteredspecs.append(codesInCSV[a][1])
    print("\nRegistered Specs Test:")
    if unregisteredspecs == []:
        print("\tAll specexceptions are registered - PASS")
        return 0
    elif unregisteredspecs != []:
        print("\tThese specifications aren't registered: %s - FAIL" % unregisteredspecs)
        return 1

def filledcolumns(codesInCSV):
    missingcols=[]
    for a in range(len(codesInCSV)):
        #fourth index in sample-entry (ObjectType) is okay if it is blank. But print the row if any other columns are blank
        if codesInCSV[a][2] == "sample-entries.csv" and codesInCSV[a][3][4] == '':
            for b in range(0,3):
                if codesInCSV[a][3][b] == "":
                    missingcols.append([codesInCSV[a][3], codesInCSV[a][2]])
        else:
            for b in range(len(codesInCSV[a][3])):
                if codesInCSV[a][3][b] == '' or codesInCSV[a][3][b] == ' ':
                    missingcols.append([codesInCSV[a][3], codesInCSV[a][2]])
    print("\nMissing Columns Test:")
    if missingcols == []:
        print("\tNo missing columns - PASS")
        return 0
    elif missingcols != []:
        for row in missingcols:
            print("\t%s" % row)
        print("\tThere are missing columns - FAIL")
        return 1
    return missingcols


def prsanitycheck():
    #GET CODES
    localrepo = "../CSV/"
    travisrepo = "CSV/"
    codesInCSV = getCSV4CCs(travisrepo) 

    #TEST for four characters
    codeExceptions = [] #Type in exceptions if you need to
    not4ccs = notfourcharacters(codesInCSV[0], codeExceptions)

    #Test for Duplicates
    dupexceptions = ["xml "]
    duplicates = duplicatecodes(codesInCSV[0], dupexceptions)

    #Test for Specifications
    specexceptions = ["see (1) below"]
    unregisteredspecs = registeredspecs(codesInCSV[0], codesInCSV[1], specexceptions)

    #Test for Filled in Columns
    # colsexceptions = [""]
    emptycols = filledcolumns(codesInCSV[0])

    #Exit Codes
    if not4ccs + duplicates + unregisteredspecs == 0:
        print("\nPR passed all checks")
        exit(0)
    elif not4ccs + duplicates + unregisteredspecs != 0:
        if (not4ccs + duplicates + unregisteredspecs) == 1:
            print("\nPR failed 1 check")
        elif (not4ccs + duplicates + unregisteredspecs) > 1:
            print("\nPR failed %d checks" % (not4ccs + duplicates + unregisteredspecs))
        exit(not4ccs + duplicates + unregisteredspecs)

prsanitycheck()
