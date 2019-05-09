import pandas as pd
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/getStatByYear/' , methods=['GET'])
def StatsByYear():
    state = request.args.get('state')
    df =  pd.read_csv("https://raw.githubusercontent.com/mkunissery/data608/master/Final/cancer2013-2017.csv")
    dfState = df[df['STATE'] == state]
    return dfState[['YEAR','RATE','DEATHS']].to_json(orient='records')

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



if __name__ == "__main__":
    app.run(debug=True)
