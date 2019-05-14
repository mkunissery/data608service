import pandas as pd
from flask import Flask
from flask import request
from flask_cors import CORS
import json
from html.parser import HTMLParser
import requests
from bs4 import BeautifulSoup
import os
from flask import send_file
import re as re
import random
import string

class data_topcancer:
    name = ""
    data = []


class model_topcancer:
    cats = []
    data = []

    def tojson(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


app = Flask(__name__)
CORS(app)



@app.route('/getStatByYear/' , methods=['GET'])
def StatsByYear():
    state = request.args.get('state')
    df =  pd.read_csv("https://raw.githubusercontent.com/mkunissery/data608/master/Final/cancer2013-2017.csv")
    dfState = df[df['STATE'] == state]

    categories = json.dumps(dfState['YEAR'].tolist())
    cases = json.dumps(dfState['DEATHS'].tolist())

    result = model_topcancer()
    result.cats = categories

    resultcases = data_topcancer()
    resultcases.name = state
    resultcases.data = cases

    result.data = [resultcases]
    return result.tojson()



@app.route('/top10cancer/' , methods=['GET'])
def Top10Cancer():
    state = request.args.get('state')
    df = pd.read_csv("https://raw.githubusercontent.com/mkunissery/data608/master/Final/top10cancer.csv")

    categories = json.dumps(df['Cancer Type'].tolist())
    cases = json.dumps(df['New Cases'].tolist())
    deaths = json.dumps(df['Deaths'].tolist())

    data = [cases , deaths]
    result = model_topcancer()
    result.cats = categories

    resultcases = data_topcancer()
    resultcases.name = "New Cases"
    resultcases.data = cases

    resultdeaths = data_topcancer()
    resultdeaths.name = "Estimated"
    resultdeaths.data = deaths

    result.data = [resultcases,resultdeaths]
    return result.tojson()



@app.route('/top10cancer1/', methods=['GET'])
def Top10Cancer1():
    state = request.args.get('state')
    df =  pd.read_csv("https://raw.githubusercontent.com/mkunissery/data608/master/Final/top10cancer.csv")
    return json.dumps(df['Cancer Type'].tolist())


@app.route('/getTop10cancercausingfoods/', methods=['GET'])
def Top10CarcinogenicFoods():
    #https://facthacker.com/cancer-causing-foods/
    #use beautifulsoup here
    return True

@app.route('/getAllStateDetails/' , methods=['GET'])
def StatsByState():
    state = request.args.get('state')
    if(state == ''):
        state = 'All'
    df =  pd.read_csv("https://raw.githubusercontent.com/mkunissery/data608/master/Final/CancerByState.csv")
    dfState = df[df['STATE'] == state]
    return dfState[['YEAR','RATE','DEATHS']].to_json(orient='records')

@app.route('/genworldcloud/' , methods=['GET'])
def get_image():
    try:
        userurl = request.args.get('url')
        res = requests.get(userurl)
        page = res.content
        soup = BeautifulSoup(page, "lxml")
        body = soup.find('body')
        bodystripped = body.findChildren()
        contents = re.sub('<[^<]+?>', " ", str(bodystripped))
        file1 = open("dynamic.txt", "w")
        file1.writelines(contents)
        file1.close()
        imgname = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        os.system(
            "wordcloud_cli --text dynamic.txt --imagefile /Users/mkunissery/playground/data608finaljq/" + imgname + ".png" + "  --width 600 --height 400")

        return imgname + ".png"
    except:
        return "error.png"



if __name__ == "__main__":
    app.run(debug=True)