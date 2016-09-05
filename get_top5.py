
qalue = {'major': 1,
         'profile_pic': 1,
         'last_name': 1,
         'old': 1,
         'language': 2,
         'instrument': 2,
         'food': 1,
         'country': 2,
         'age': 1,
         'first_name': 1,
         'course': 1,
         'college': 2,
         'pokemon_team': 2,
         'movie': 1,
         'sport': 1,
         'nickname': 0,
         'anime': 1,
         'sad': 2}
         
         


def get_top5(points):
    top_5 = sorted(points.iteritems(), key=lambda (k,v): (v,k))
    top_5 = [top_5[i] for i in range(len(top_5)-5, len(top_5))]
    t_5 = [{top_5[i][0]: top_5[i][1]} for i in range(len(top_5)-1,-1, -1)]
    return t_5 


        

def match_by_name(data, username):
    points = {}
    sample = {}
    for elem in data:
        if elem['nickname'] == username:
            sample = elem
        else:
            points[elem['nickname']] = 0


    if sample == {}:
        t5 = False
        return 0, t5

    total = len(sample)
    
    for elem in sample:
        if sample[elem] == '':
            total -= qalue[elem]

    
    for elem in data:
        cur_user = elem['nickname']
        if cur_user != username:
            for value in elem:
                if elem[value] == sample[value]:
                    if elem[value] != '' and sample[value] != '':
                        points[cur_user] += qalue[value]

    return get_top5(points), total



