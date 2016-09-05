import os
import json
from flask import Flask, url_for, render_template, request
import os
from time import strftime, time
from random import randrange
import get_top5
from werkzeug.utils import secure_filename
from vis_data import percentvisual, set_default_pic, captcha
from time import time, sleep
from math import trunc
from match import perMatch
from Movie_Finder import getMovies
from graphs import PokemonGOimage
from translator import transStr
from band_former import formBand
#Dict to get more accurate names for keys of data


bad_words = ['fuck', 'suck', 'ass', 'bitch', 'moron', 'retard']

convert_keys = { 'first_name': 'First name',
                 'last_name': 'Last name',
                 'nickname': 'Username',
                 'country': 'Country',
                 'age': 'Age',
                 'major': 'Major',
                 'movie': 'Movie',
                 'pokemon_team': 'Pokemon GO Team',
                 'old': 'Old or new movies',
                 'language': 'Languages you speak',
                 'instrument': 'Music instruments you play',
                 'food': 'Your favorite food',
                 'course': 'CSE11 or CSE8',
                 'college': 'College you are in',
                 'sport': 'Your favorite sports',
                 'sad': 'Sadbys/Sadgirls',
                 'anime': 'Animeeee?'}


map_pics = { 'USA' : [['LA', 'CA', 'AL', 'AK', 'AZ','AR','CO','FL','GA','KY','MI',
                       'MA','MO','NE','NY','NJ','TX','VT','VA','WY'], 'map/usa.png'],
             'SNG' : [['RUSSIA', 'KAZACHSTAN', 'UKRAINE', "BELARUS"], 'map/sng.png'],
             'India' : [['INDIA'], 'map/india.png'],
             'China' : [['CHINA'], 'map/china.png'] }

#Creating new sec. file to place codes in.
secFile = open("sec/codes.sc", "w")
secFile.close()

secCodes = {}

#log = open('log_'+strftime("%Y_%m_%d_%H_%M_%S")+'.txt', 'w')
#log.write('Starting app on localhost..')

app = Flask(__name__)

users_ip = []

@app.route('/')
#Rendering main page: >Take Survey >Edit answers >Get top 5
def render_main():
    #check the IP of connected user
    users_ip.append(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    #log.write(str('Connection to main menu:' + request.environ.get('HTTP_X_REAL_IP', request.remote_addr)) + '\n')
    return render_template('main.html')


@app.route('/survey')
#Rendering survey page with questions
def render_survey():
     secCodes[request.environ.get('HTTP_X_REAL_IP', request.remote_addr)] = generate_code()
     print secCodes[request.environ.get('HTTP_X_REAL_IP', request.remote_addr)]
     secFile = open('sec/codes.sc', 'a')
     secFile.write(request.environ.get('HTTP_X_REAL_IP', request.remote_addr) + ' : ' + str(secCodes[request.environ.get('HTTP_X_REAL_IP', request.remote_addr)]) + '\n')
     secFile.close()
     print secCodes[request.environ.get('HTTP_X_REAL_IP', request.remote_addr)]
     capt = captcha(secCodes[request.environ.get('HTTP_X_REAL_IP', request.remote_addr)])
     print capt
     #log.write(str(request.environ.get('HTTP_X_REAL_IP', request.remote_addr) + ' is going to take a survey.')+ '\n')
     return render_template('survey.html', captcha = capt)


@app.route('/result', methods = ["POST"])
#Process data from /survey page
def render_result():
    if request.method == 'POST':
        req = request.form
        photo = request.files ['profile_pic']

        results = {}

        if request.form['security_code'] != str(secCodes[request.environ.get('HTTP_X_REAL_IP', request.remote_addr)]):
             return render_template('error.html', error = 'invalid sequtiry code')

        ok, results = process_req(req)

        if ok:

            results.pop('security_code')

            #Check returns 2 values: Boolean and Comment
            #for error (depending on type of error)
            if check(results)[0]:
                #works with json file, appending new user's info
                results['profile_pic'] = ''
                if check_file(photo):
                    #filename = secure_filename(photo.filename)
                    photo.save('static/pics/' + results['nickname'] + '.' + photo.filename.rsplit('.', 1)[1])
                    results['profile_pic'] = 'pics/' + results['nickname'] + '.' + photo.filename.rsplit('.', 1)[1]
                    pic = 'pics/' + results['nickname'] + '.' + photo.filename.rsplit('.', 1)[1]
                    print getSize('static/pics/' + results['nickname'] + '.' + photo.filename.rsplit('.', 1)[1])/1024.0
                    if getSize('static/pics/' + results['nickname'] + '.' + photo.filename.rsplit('.', 1)[1])/1024.0 > 2000:
                        set_default_pic('static/pics/' + results['nickname'] + '.jpeg')
                        results['profile_pic'] = 'pics/' + results['nickname'] + '.jpeg'
                        pic = 'pics/' + results['nickname'] + '.jpeg'
                        
                else:
                    set_default_pic('static/pics/' + results['nickname'] + '.jpeg')
                    results['profile_pic'] = 'pics/' + results['nickname'] + '.jpeg'
                    pic = 'pics/' + results['nickname'] + '.jpeg'

                save_res(results)
                return render_template('success.html', name = req['first_name'], pic = pic)
                #log.write(str('Successfully added ' + results['nickname'] + ' IP:' + request.environ.get('HTTP_X_REAL_IP', request.remote_addr))+ '\n')
            else:
                return render_template('error.html', error = check(results)[1])
                #log.write(str('Failed to add ' + results['nickname'] + 'IP:', request.environ.get('HTTP_X_REAL_IP', request.remote_addr) + 'with error:' + check(results)[1]) + '\n')
        else:
            return render_template('error.html', error = results)


def process_req(req):
    result = {}
    for elem in req:
        if elem == 'country' and req[elem].upper() in map_pics['USA'][0]:
            if len(req[elem]) > 2:
                return False, 'wrong input in ' + elem
            result[elem] = req[elem].lower()
        elif elem == 'major' and len(req[elem]) > 4:
            return False, 'wrong input in ' + elem

        elif elem == 'movie' or elem == 'sport' or elem == 'instrument' or elem == 'food' or elem == 'language' or elem == 'music':
            if ',' in req[elem]:
                result[elem] = []
                for k in req[elem].split(','):
                    result[elem].append(k.lower().strip())
            elif req[elem] == '' and elem == 'movie':
                result[elem] = 'harry potter'
            else:
                result[elem] = req[elem].lower().strip()
        elif elem == 'old' and req[elem] == '':
            result[elem] = 3
        elif elem == 'pokemon_team' and req[elem].lower() not in [u'mystic', u'instinct', u'valor', u'']:
            return False, 'wrong input in ' + elem
        elif elem == 'course':
            if req[elem] == 'CSE11' or  req[elem] == 'CSE 11':
                result[elem] = '11'
            elif  req[elem] == 'CSE8' or  req[elem] == 'CSE 8':
                result[elem] = '8'
            else:
                result[elem] = req[elem].lower().strip()

        elif req[elem].lower() in ['no', 'none', 'nope']:
            result[elem] = ''

        elif req[elem].lower() in bad_words:
            return False, 'Hey! No bad words'

        else:
            result[elem] = req[elem].lower().strip()
    return True, result








def check(arr):
    allowed_for_dig = ['old', 'anime', 'movie', 'food', 'age', 'nickname', 'movie', 'course', 'securiry_code', 'profile_pic']
    dig_only = ['old', 'security_code', 'age', 'course']
    '''checks for existing, req fields, isaplha and isdigit '''
    if in_base(arr['nickname']):
        return False, 'username already exists'

    if arr['nickname'] == '' or arr['last_name'] == '' or arr['first_name'] == '':
            return False, 'required fields should be filled'

    for elem in arr:
        if type(elem) == 'str':
            if elem not in allowed_for_dig:
                if not(arr[elem].isalpha()) and arr[elem] != '':
                    print elem
                    return False, 'numbers in a text form ' + elem
            if (elem in dig_only) :
                if not(arr[elem].isdigit()) and (arr[elem] != ''):
                    print elem
                    return False, 'letters in a digit form ' + elem
        if type(elem) == 'list':
            for k in elem:
                if k not in allowed_for_dig:
                    if not(arr[k].isalpha()) and arr[k] != '':
                        print k
                        return False, 'numbers in a text form ' + elem
                if (k in dig_only) :
                    if not(arr[k].isdigit()) and (arr[k] != ''):
                        print k
                        return False, 'letters in a digit form ' + elem


        return True, 'none'


def getSize(fileobject):
    statinfo = os.stat(fileobject)
    return statinfo.st_size


def check_file(f):
    if f.filename == '' or f.filename == ' ':
        return False
    if f.filename.rsplit('.', 1)[1] not in ['jpg', 'jpeg', 'png']:
        return False
    
    return True



def save_res(results):
    f = open('users.json', 'a')
    f.write(str(results) + '\n')
    f.close()
    #log.write(str('User ' + results['nickname'] + ' added to database.')+'\n')



def read_data():
    '''get dict from json file; REMINDER: SEQURITY!!!'''
    f = open('users.json')
    data = []
    for l in f:
        data.append(eval(l))
    f.close()
    return data

def in_base(name):
    '''checks whether the nickname is already in base'''
    data = read_data()
    for elem in data:
        if elem['nickname'] == name:
            return True
    return False


@app.route('/match', methods=["GET","POST"])
def render_match():
    if request.method == "POST":
        users = request.form['users'].split(',')
        match = perMatch(read_data(), users[0], users[1])
        user_data = get_user(read_data(), users[0])
        full_name = ['','']
        full_name[0] = user_data['last_name'][0].upper() + user_data['last_name'][1:]
        full_name[1] = user_data['first_name'][0].upper() + user_data['first_name'][1:]

        res = match['language'][1]

        country_map = ''
        if match['country'][0]:
            country_map = get_map(match['country'][1])

        users_movs = []
        if type(match['movie'][1]) == type([]) and type(match['movie'][2]) == type([]):
            match['movie'][1].extend(match['movie'][2])
            users_movs = match['movie'][1]

        if type(match['movie'][1]) == type([]) and type(match['movie'][2]) in [type(u''), type('')]:
            match['movie'][1].append(match['movie'][2])
            users_movs = match['movie'][1]

        if type(match['movie'][1]) in [type(u''), type('')] and type(match['movie'][2]) in [type(u''), type('')]:
            users_movs.append(match['movie'][1])
            users_movs.append(match['movie'][2])

        if type(match['movie'][1]) in [type(u''), type('')] and type(match['movie'][2]) == type([]):
           # print 'here'
            match['movie'][2].append(match['movie'][1])
            users_movs = match['movie'][2]


        #print users_movs, match['movie'][1], match['movie'][2]



        movies = getMovies(users_movs, 3, int((int(match['old'][1])+int(match['old'][2]))/2))

        total = get_total_pokemon()
        pokeim = ''
        if match['pokemon_team'][0]:
            pokeim = PokemonGOimage(total, match['pokemon_team'][1])


        college_im = ''
        if match['college'][0]:
            college_im = 'colleges/' + match['college'][1] + '.png'

        '''
        if match['language'][0]:
            #try:
                res = transStr(match['language'][1], 'You and your partner can speak ')
            #except:
             #   res = match['language'][1].upper() + '!'
        '''




        match['country'][1] = match['country'][1].upper()

        print request.method

        user1ins = []
        user2ins = []

        if type(get_user(read_data(), users[0])['instrument']) == list:
            user1ins.extend(get_user(read_data(), users[0])['instrument'])
        if type(get_user(read_data(), users[0])['instrument']) in [type(''), type(u'')]:
            user1ins.append(get_user(read_data(), users[0])['instrument'])

        if type(get_user(read_data(), users[1])['instrument']) == list:
            user2ins.extend(get_user(read_data(), users[1])['instrument'])
        if type(get_user(read_data(), users[1])['instrument']) in [type(''), type(u'')]:
            user2ins.append(get_user(read_data(), users[1])['instrument'])



        print user1ins, user2ins
        ins1, ins2 = '', ''
        if user1ins != [] and user2ins != []:
            for elem in user1ins:
                if elem not in user2ins and elem not in ['', 'no']:
                    ins1 = elem
                    ins2 = user2ins[0]
                    break



        tmp_band = {}
        if not(match['instrument'][0]) and match['instrument'][1] not in ['no', ''] and match['instrument'][2] not in ['no', '']:
            tmp_band = formBand(read_data(), ins1, ins2)

        print tmp_band
        band = {}
        if tmp_band != {}:
            i = 0
            for elem in tmp_band:
                band[up_first(get_user(read_data(), elem)['first_name']) + ' ' + up_first(get_user(read_data(), elem)['last_name'])] = tmp_band[elem]
                if i >= 2:
                    break
                i += 1

        if band != {}:
            make_band = True
        else:
            make_band = False

        band[up_first(get_user(read_data(), users[0])['first_name']) + ' ' + up_first(get_user(read_data(), users[0])['last_name'])] = ins1

        band[up_first(get_user(read_data(), users[1])['first_name']) + ' ' + up_first(get_user(read_data(), users[1])['last_name'])] = ins2



        if request.method == "POST":
            return render_template('match.html', match = match, cmap = country_map, movies = movies, full_name = full_name,
                                   pokeim = pokeim, college_im = college_im, band=band, make_band = make_band)



def up_first(s):
    return s[0].upper() + s[1:]


def get_map(co):
    for elem in map_pics:
        print co.upper()
        if co.upper() in map_pics[elem][0]:
            return map_pics[elem][1]

def get_total_pokemon():
    data = read_data()
    total = [0, 0, 0]
    for elem in data:
        if elem['pokemon_team'] == 'valor':
            total[0] += 1

        if elem['pokemon_team'] == 'mystic':
            total[1] += 1


        if elem['pokemon_team'] == 'instinct':
            total[2] += 1
    return total


@app.route('/gettop5')
def render_gettop5():
    return render_template('gettop5.html')

@app.route('/top5')
def render_top5():
    pics = {}
    percents = {}
    user_pics = {}
    data = read_data()
    user = request.args['nickname'].lower()
    t5, total = get_top5.match_by_name(read_data(), user)

    os.chdir('static/images')
    filelist = [ f for f in os.listdir(".") if f.endswith(".jpeg") ]
    for f in filelist:
        os.remove(f)
    os.chdir('../../')
    t5_data = {}
    if t5:
        for user in t5:
            for elem in user:
                user_pics[elem] = get_user(data, elem)['profile_pic']
                pics[elem] = (percentvisual(user[elem]/float(total), 300, 50, (10, 120, 230)))
                percents[elem] = trunc(user[elem]/float(total)*100)
                user_data = get_user(data, elem)
                t5_data[elem] = ['','']
                t5_data[elem][0] = user_data['last_name'][0].upper() + user_data['last_name'][1:]
                t5_data[elem][1] = user_data['first_name'][0].upper() + user_data['first_name'][1:]

        return render_template('top5_result.html', t5_data = t5_data, t5 = t5, pics = pics, per = percents, us_pic = user_pics, cur_name = request.args['nickname'].lower())
    else:
        return render_template('error.html', error = 'no user registered with that nickname')


def get_user(data, user):
    for elem in data:
        if elem['nickname'] == user:
            return elem

@app.route('/forgot')
def render_forgot():
    return render_template('forgot.html')

@app.route('/edit')
def render_edit():
    return render_template('edit.html')


@app.route('/edit_answers')
#Editing data for user that already exists in base
def render_edit_answers():

        name = request.args['nickname'].lower()

        #ASK ABOUT IF SEQ CODE TO SEE WHO I MATCH WITH
        #updating secCode for user
        secCodes[name] = generate_code()
        secFile = open('sec/codes.sc', 'a')
        secFile.write(name + ' : ' + str(secCodes[name]) + '/n')
        secFile.close()
        capt = captcha(secCodes[name])
        data = read_data()
        username_answers = {}
        #getting userdata from data
        for elem in data:
            if elem['nickname'] == name:
                username_answers = {}
                for v in elem:
                    if type(elem[v]) in [type(''), type(u'')]:
                        username_answers[v] = elem[v].upper()
                    if type(elem[v]) in [type([])]:
                        tmp_username_answers = []
                        print elem[v]
                        for k in elem[v]:
                            tmp_username_answers.append(k.upper())
                        username_answers[v] = ', '.join(tmp_username_answers)
                print(username_answers)
                break
        #check whether data for user was found
        print username_answers['movie']
        if str(username_answers) != '{}':
            return render_template('edit_answers.html', data = username_answers,
                                   cdata = convert_keys, captcha = capt)
        else:
            return render_template('error.html', error = 'no user with that nickname')


def low_case(s):
    return s.upper()

def generate_code():
    val = time() % 1000
    val = (randrange(1000, 9999) * val) % 1000000
    return int(val)

@app.route('/edit_result', methods = ["POST"])
def edit_result():
    if request.method == 'POST':
        print request.form, request.files['profile_pic']
        req = request.form
        results = {}
        photo = request.files['profile_pic']

        #checking the sequrity code
        #print str(secCodes[request.args['nickname'].lower()]), request.args['security_code']
        if request.form['security_code'] != str(secCodes[request.form['nickname'].lower()]):
             return render_template('error.html', error = 'invalid sequtiry code')

        #log.write(str('User' + req['nickname'] + 'is trying to edit answers') + '\n')
        ok, results = process_req(req)
        #deleting code from resulting dict
        results.pop('security_code')
        print check_file(photo)
        if check_file(photo) and ok:
                #filename = secure_filename(photo.filename)
                photo.save('static/pics/' + results['nickname'] + '.' + photo.filename.rsplit('.', 1)[1])
                print 'saved pic for ' + results['nickname']
                results['profile_pic'] = 'pics/' + results['nickname'] + '.' + photo.filename.rsplit('.', 1)[1]
        else:
            results['profile_pic'] = get_user_data(results['nickname'])['profile_pic']

        if ok:
            overwrite_ans(results['nickname'], results)
            return render_template('success.html', name = req['first_name'])
        else:
            return render_template('error.html', error = results)

def overwrite_ans(name, results):
    f_tmp = open("users_tmp.json", "w")
    with open("users.json", "r") as f:
        for line in f:
            tmp = eval(line)
            if tmp['nickname'] == name:
               f_tmp.write(str(results) + '\n')
            else:
                f_tmp.write((str(tmp) + '\n'))
    f_tmp.close()
    f_tmp = open("users_tmp.json", "r")
    f = open("users.json", "w")
    for line in f_tmp:
        f.write(line)
    #log.write(str('Successfully overwritten results for ' + name) + '\n')
    f_tmp.close()


def get_user_data(user):
    data = read_data()
    for elem in data:
        if elem['nickname'] == user:
            return elem
    return False
if __name__=="__main__":
    app.run(debug=False,host="localhost", port=53545)
