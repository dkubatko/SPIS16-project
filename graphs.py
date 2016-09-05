import matplotlib.pyplot as plt
from collections import defaultdict
from time import time
import os

def PokemonGOimage(totals,highlight):

    os.chdir('static/graphs')
    filelist = [ f for f in os.listdir(".") if f.endswith(".png") ]
    for f in filelist:
        os.remove(f)

    os.chdir('../../')
    labels = 'Valor', 'Mystic', 'Instinct'
    sizes = [totals[0],totals[1],totals[2]]

    colors = ['r', 'deepskyblue', 'gold']

    if highlight == 'valor':
        explode = (0.1, 0, 0)
    elif highlight == 'mystic':
        explode = (0,0.1,0)
    elif highlight == 'instinct':
        explode = (0, 0, 0.1)
    else:
        explode = (0, 0, 0)


    plt.pie(sizes, explode = explode, labels = labels, colors = colors, autopct='%1.1f%%', shadow = True, startangle =90)
    plt.axis('equal')
    rand = str(time()%100)
    image = plt.savefig("static/graphs/pokemon_GO_distribution"+ rand +".png")
    plt.clf()
    return "graphs/pokemon_GO_distribution"+rand+".png"

