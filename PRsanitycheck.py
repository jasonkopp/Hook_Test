#!/usr/bin/env python3
import csv, re, os

# X- are all the codes actually 4 characters (or an escape)?
# X - are the codes unique, at least in their table, (and give a warning if the code is also in another table)
# are the spec shortnames registered, or will they be?
# are all the mandatory columns filled in?

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
                        csvLine = str(list(row.values()))
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
    if mistakeCodes == []:
        print("Four Character Codes Test:\n\tAll 4ccs are four characters - PASS")
        return 0
    else:
        print("Four Character Codes Test:\n\tSomething is wrong with these codes: %s - FAIL" % mistakeCodes)
        return 1

def duplicatecodes(codes, dupexceptions=[""]):
    allcodes = [code[0] for code in codes if code[0] not in dupexceptions]
    duplicates = sorted([[codes[i][3], codes[i][2]] for i in range(len(codes)) if allcodes.count(codes[i][0]) > 1])

    if duplicates == []:
        print("Duplicate 4CCs Test:\n\tNo duplicates found - PASS")
        return 0
    else:
        print("Duplicate 4CCs Test:")
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
            print("\tNo duplicates found in the same CSV - PASS")
            return 0


def registeredspecs(codesInCSV, speclist, specexceptions=[""]):
    unregisteredspecs = []
    allspecs = [spec[1].lower() for spec in speclist]+specexceptions
    for a in range(len(codesInCSV)):
        if codesInCSV[a][1].lower() not in allspecs:
            unregisteredspecs.append(codesInCSV[a][1])
    print("Registered Specs Test:")
    if unregisteredspecs == []:
        print("\tAll specexceptions are registered - PASS")
        return 0
    elif unregisteredspecs != []:
        print("\tThese specifications aren't registered: %s - FAIL" % unregisteredspecs)
        return 1

def prsanitycheck():
    #GET CODES
    localrepo = "../CSV/"
    travisrepo = "CSV/"
    codesInCSV = getCSV4CCs(travisrepo)

    #TEST for four characters
    codeExceptions = [] #Type in exceptions if you need to
    not4ccs = notfourcharacters(codesInCSV[0], codeExceptions)

    #Test for Duplicates
    dupexceptions = ["m4ae", "tsel", "xml "] #PR SUBMITED TO FIX "tsel" AND "m4ae". - "xml " is actually an exception.
    duplicates = duplicatecodes(codesInCSV[0], dupexceptions)

    #Test for Specifications
    specexceptions = ["see (1) below"]
    unregisteredspecs = registeredspecs(codesInCSV[0], codesInCSV[1], specexceptions)

    #Exit Codes
    if not4ccs + duplicates + unregisteredspecs == 0:
        print("PR passed all checks")
        exit(0)
    elif not4ccs + duplicates + unregisteredspecs != 0:
        if (not4ccs + duplicates + unregisteredspecs) == 1:
            print("PR failed 1 check")
        elif (not4ccs + duplicates + unregisteredspecs) > 1:
            print("PR failed %d checks" % (not4ccs + duplicates + unregisteredspecs))
        exit(not4ccs + duplicates + unregisteredspecs)

prsanitycheck()
