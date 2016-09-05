
data = [ {'nickname' : 'drazzzer', 'major' : 'CS',
          'gender' : 'male'}, {'nickname' : 'serg98', 'major' : 'CS',
          'gender' : 'female'}]


name1 = data[0]
name2 = data[1]




def perMatch(data, name1,name2):
    '''Takes 2 Dictionaries as paramaters, returns the percentage of matched values'''
    dictname1 = {}
    dictname2 = {}
    match = {}
    for l in range(len(data)): 
        if name1 == data[l]['nickname']:
            dictname1 = data[l]
        elif name2 == data[l]['nickname']:
            dictname2 = data[l]
            
    total = len(dictname1.keys()) - 1
    matchcount = 0
    for l in dictname1:
        if l != 'nickname':
            #print l, type(dictname1[l]), type(dictname2[l]), type(dictname2[l]) == type('')
            
            if type(dictname1[l]) in [type(u''),type('')] and type(dictname2[l]) in [type(u''),type('')]:
                if dictname1[l] == dictname2[l]:  
                    match[l] = [1, dictname1[l], dictname2[l]]
                else:
                    match[l] = [0, dictname1[l], dictname2[l]]
            if type(dictname1[l]) == type([]) and type(dictname2[l]) in [type(u''),type('')]:
                for elem in range(len(dictname1[l])):
                    print dictname1[l]
                    if dictname1[l][elem] == dictname2[l]:
                        match[l] = [1, dictname1[l][elem], dictname2[l]]
                        break
                    else:
                        match[l] = [0, dictname1[l][elem], dictname2[l]]
                        
            if type(dictname1[l]) in [type(u''),type('')] and type(dictname2[l]) == type([]):
                    if dictname1[l] in dictname2[l]:
                        match[l] = [1, dictname1[l], dictname1[l]]
                    else:
                        match[l] = [0, dictname1[l], dictname2[l][0]]
                        
            if type(dictname1[l]) == type([]) and type(dictname2[l]) == type([]):
                for elem in range(len(dictname1[l])):
                    if dictname1[l][elem] in dictname2[l]:
                        match[l] = [1, dictname1[l][elem], dictname1[l][elem]]
                        break
                    else:
                        match[l] = [0, dictname1[l][elem], dictname2[l][0]]

    print match
    return match
    



