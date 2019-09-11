from flask import Blueprint
from flask import Flask, abort, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import json
from dbUtils import DbUtils, stat

from numpy.random import seed
from numpy.random import randn


api = Blueprint('api', __name__)
CORS(api)
parser = reqparse.RequestParser()


@api.route('/addfilm', methods=['POST'])
def addfilm():
    if not request.json:
        abort(400)

    filmData = json.dumps(request.json)
    filmObject = json.loads(filmData, object_hook=JSONObject)
    dbUtils = DbUtils()
    dbUtils.addNewFilm(filmObject.title, filmObject.director, filmObject.year)
    return json.dumps(filmData)


@api.route('/getfilm')
def getFilms():
    films = []
    dbUtils = DbUtils()
    filmData = dbUtils.getFilms()
    for r in filmData:
        a = {"title": r[0], "director": r[1], "year": r[2]}
        films.append(a)

    return jsonify(films)


@api.route('/create_film_table')
def createFilmTable():
    dbUtils = DbUtils()
    dbUtils.createTable()
    result = {"result": "Films Table Created"}
    return jsonify(result)


@api.route('/ttest', methods=['GET'])
def calStat():
    a = stat().ttest()
    result = {"result": a}
    return jsonify(result)


@api.route('/post')
def post(self):
    parser.add_argument('quote', type=str)
    args = parser.parse_args()
    return {
        'status': True,
        'quote': '{} added. Good'.format(args['quote'])
    }

# example get parameter via requrest.args
@api.route('/hello', methods=['GET'])
def api_hello():
    if 'name' in request.args:
        return 'Hello ' + request.args['name']
    else:
        return 'Hello John Doe'


@api.route('/da', methods=['POST'])
def api_message():

    if request.headers['Content-Type'] == 'text/plain':
        return "Text Message: " + request.data

    elif request.headers['Content-Type'] == 'application/json':
        return "JSON Message: " + json.dumps(request.json)

    elif request.headers['Content-Type'] == 'application/octet-stream':
        f = open('./binary', 'wb')
        f.write(request.data)
        f.close()
        return "Binary message written!"

    else:
        return "415 Unsupported Media Type ;)"


@api.route('/json', methods=['POST'])
def test_json():

    content = request.get_json()
    print(content)
    # print(jsonify(request.json))
    da = content['result']
    print(content['result'])

    result = {"result": da}
    return jsonify(result)

    # return 'da'


@api.route('/lin_regress', methods=['POST'])
def lin_regress():
    a = stat()
    b = request.get_json()
    x = b['data1']
    y = b['data2']
    slope, intercept, r_value, p_value, std_err = a.linregress(x, y)
    result = {
        "slope": slope,
        "intercept": intercept,
        "r_value": r_value,
        "p_value": p_value,
        "std_err": std_err
    }
    return jsonify(result)


@api.route('/ind_ttest', methods=['POST'])
def ind_ttest():
    a = stat()
    b = request.get_json()
    # generate two independent samples
    data1 = b['data1']
    data2 = b['data2']
    # calculate the t test
    alpha = 0.05
    t_stat, df, cv, p = a.independent_ttest(data1, data2, alpha)
    print('t=%.3f, df=%d, cv=%.3f, p=%.3f' % (t_stat, df, cv, p))
    if abs(t_stat) <= cv:
        cvTxt = 'ไม่แตกต่างกัน'
        print('Accept null hypothesis that the means are equal.')
    else:
        cvTxt = 'แตกต่างกันอย่างมีนัยสำคัญ'
        print('Reject the null hypothesis that the means are equal.')

    if p > alpha:
        pTxt = 'ไม่แตกต่างกัน'
        print('Accept null hypothesis that the means are equal.')
    else:
        pTxt = 'แตกต่างกันอย่างมีนัยสำคัญ'
        print('Reject the null hypothesis that the means are equal.')

    result = {
        "t_stat": t_stat,
        "df": df,
        "cv": cv,
        "p": p,
        "cvTxt": cvTxt,
        "pTxt": pTxt
    }
    return jsonify(result)


class JSONObject:
    def __init__(self, dict):
        vars(self).update(dict)
