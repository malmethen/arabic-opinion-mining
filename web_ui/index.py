import json
import joblib
from flask import Flask, render_template, request, url_for
from predict import data_pipeline

app = Flask(__name__)

model1 = joblib.load('stars_model.sav')
vect1 = joblib.load('vect2.pkl')

model2 = joblib.load('sentiment_model.sav')
vect2 = joblib.load('vect.pkl')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/stars")
def stars():
    return render_template('index.html')

@app.route("/sentiment")
def sentiment():
    return render_template('index.html')

@app.route("/query", methods=["POST"])
def query0():
    data = request.json
    answer = "اختر احد الخيارات على اليمين اولًا"
    
    return json.dumps(answer)

@app.route("/stars/query", methods=["POST"])
def query1():
    data = request.json

    # returns cleaned and preprocessed data
    procssed_data = data_pipeline(data['question'])

    test_review = vect1.transform([procssed_data])
    pr = model1.predict(test_review) 
    if pr == [1] :
        answer = "☆☆☆☆★"
    elif pr == [2] :
        answer = "☆☆☆★★"
    elif pr == [3] :
        answer = "☆☆★★★"
    elif pr == [4] :
        answer = "☆★★★★"
    else:
        answer = "★★★★★"
    
    return json.dumps(answer)

@app.route("/sentiment/query", methods=["POST"])
def query2():
    data = request.json

    # returns cleaned and preprocessed data
    processed_data = data_pipeline(data['question'])

    test_review = vect2.transform([processed_data])
    pr = model2.predict(test_review) 
    if pr == ['neutral'] :
        answer = "تعليق معتدل"
    elif pr == ['positive'] :
        answer = "تعليق ايجابي"
    else:
        answer = "تعليق سلبي"
    
    return json.dumps(answer)






    



