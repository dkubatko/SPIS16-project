import urllib
import tmdbsimple as tmdb
import warnings

warnings.filterwarnings("ignore")
tmdb.API_KEY = '28e38a10930d757502480aa63b2cf036'

'''
search = tmdb.Search()
response = search.movie(query='Ghostbusters')

genres = tmdb.Genres()
print tmdb.Genres(28).movies()
'''
#for l in response:
#    print response[l]

#print search.keyword(id='207600')


def getMovies(movies, num, old):
    results = []
    for movie in movies:
        try:
            tmp_res = findMovie(movie, num, old)
            for res in tmp_res:
                if res[0] not in titles(results):
                    results.append(res)
        except:
            print 'one of movies didnt work'
            
    print titles(results)
    return results


def titles(results):
    titles = []
    for elem in results:
        titles.append(elem[0])
    return titles
        

def findMovie(name, num, old):
    genres_in_com = []
    genres = []
    i = 0
    
    search = tmdb.Search()
    response = search.movie(query=name)
    results = response['results']
    max_pop = 0
    pop_mov = {}
    for movie in results:
        if movie['popularity'] > max_pop:
            max_pop = movie['popularity']
            pop_mov = movie
    for genre in pop_mov['genre_ids']:
        if genre not in genres:
            genres.append(genre)

    
    mov_res = []
    common_movs = {}
    for genre in genres:
        cur_genre = tmdb.Genres(genre)
        same_genre_mov = []
        low, high = old-1, old+1
        if low <= 0:
            low = 1
        for i in range(low, high):
            tmp_res = cur_genre.movies(page=i, include_adult=False)['results']
            same_genre_mov.extend(tmp_res)
        for mov in same_genre_mov:
            if name not in mov['title'].lower() :
                mov_res.append(mov)
                common_movs[mov['title']] = 0
    
    for elem in mov_res:
        common_movs[elem['title']] += 1
    final = sorted(common_movs.iteritems(), key=lambda (k,v): (v,k))
    pen = {}
    for elem in final:
        for mov in mov_res:
            if elem[0] == mov['title']:
                pen[elem[0]] = [elem[1], mov['vote_average'], 'https://image.tmdb.org/t/p/w300_and_h450_bestv2' + mov['poster_path']]
                break
        
    sorted_pen = sorted(pen.iteritems(), key=lambda (k,v): (-v[0],k))
    #print sorted_pen[:num]
    compl1 = [list(sorted_pen[0])]
    compl2 = []
    #print compl1
    for elem in sorted_pen:
        #print elem[1][0]
        if elem[1][0] == compl1[-1][1][0]:
            compl1.append(list(elem))
        else:
            #print elem
            compl2 = [list(elem)]
            break

    compl1.pop(0)
    if compl2 != []:
        for elem in sorted_pen:
            if elem[1][0] == compl2[-1][1][0]:
                compl2.append(list(elem))
            elif elem[0] < compl2[-1][1][0]:
                break

    completed_1 = sorted(compl1, key=lambda x: -x[1][1])
    completed_2 = sorted(compl2, key=lambda x: -x[1][1])
    completed_1.extend(completed_2)
    #for elem in completed_1[:num]:
        
       # print elem[0] + ' : counts:' + str(elem[1][0]) + ', rating:'+ str(elem[1][1])
    
    
            
        
        
    return completed_1[:num]



#print getMovies(['harry potter', 'star wars', 'donnie darko', 'lone'], 1, 3)

