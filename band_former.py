def formBand(data,ins1, ins2):
    resultDict = {}
    doNotIncl = []

    if type(ins1) in [type(''), type(u'')] and type(ins2) in [type(''), type(u'')]:
        for l in range(len(data)):
            if  ins1 in data[l]['instrument'] or ins2 in data[l]['instrument']:
                doNotIncl.append(data[l]['nickname'])
        for l in range(len(data)):
            if data[l]['nickname'] not in doNotIncl and data[l]['instrument'] not in ['', [], 'no']:
                if type(data[l]['instrument']) == list:
                    if data[l]['instrument'][0] not in resultDict.values():
                        resultDict[data[l]['nickname']] = data[l]['instrument'][0]
                else:
                    if data[l]['instrument'] not in resultDict.values():
                        resultDict[data[l]['nickname']] = data[l]['instrument']
                
        return resultDict

    elif type(ins1) == list and type(ins2) == list:
        for l in range(len(data)):
            for elem in ins1:
                if elem in data[l]['instrument']:
                    doNotIncl.append(data[l]['nickname'])
            for ans in ins2:
                if ans in data[l]['instrument']:
                    doNotIncl.append(data[l]['nickname'])

        for l in range(len(data)):
            if data[l]['nickname'] not in doNotIncl and data[l]['instrument'] not in ['', [], 'no']:
                if type(data[l]['instrument']) == list:
                    if data[l]['instrument'][0] not in resultDict.values():
                        resultDict[data[l]['nickname']] = data[l]['instrument'][0]
                else:
                    if data[l]['instrument'] not in resultDict.values():
                        resultDict[data[l]['nickname']] = data[l]['instrument']

        return resultDict            

    elif type(ins1) == list and type(ins2) in [type(''), type(u'')]:
        for l in range(len(data)):
            for elem in ins1:
                if elem in data[l]['instrument'] or data[l]['instrument'] == ins2:
                    doNotIncl.append(data[l]['nickname'])

        for l in range(len(data)):
            if data[l]['nickname'] not in doNotIncl and data[l]['instrument'] not in ['', [], 'no']:
                if type(data[l]['instrument']) == list:
                    if data[l]['instrument'][0] not in resultDict.values():
                        resultDict[data[l]['nickname']] = data[l]['instrument'][0]
                else:
                    if data[l]['instrument'] not in resultDict.values():
                        resultDict[data[l]['nickname']] = data[l]['instrument']

        return resultDict

    elif type(ins1) in [type(''), type(u'')] and type(ins2) == list:
        for l in range(len(data)):
            if  ins1 in data[l]['instrument']:
                doNotIncl.append(data[l]['nickname'])
            for elem in ins2:
                if elem in data[l]['instrument']:
                    doNotIncl.append(data[l]['nickname'])
                    
        for l in range(len(data)):
            if data[l]['nickname'] not in doNotIncl and data[l]['instrument'] not in ['', [], 'no']:
                if type(data[l]['instrument']) == list:
                    if data[l]['instrument'][0] not in resultDict.values():
                        resultDict[data[l]['nickname']] = data[l]['instrument'][0]
                else:
                    if data[l]['instrument'] not in resultDict.values():
                        resultDict[data[l]['nickname']] = data[l]['instrument']
                    

        return resultDict
