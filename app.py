import json
import os
from flask import Flask, jsonify,request
from flask_cors import CORS
import predictor
from predictor import my_ml_predictor


app = Flask(__name__)
CORS(app)

@app.route("/",methods=['GET'])
def return_result():
    #age_ ,gen_, hei_,wei_,aph_,apl_,cho_,glu_,smo_,alc_,act_
    if request.args.get('var1') == "var1value":
        result = {
                'info' : ' the information is based on var1 ',
                'score' : ' 100 % ' 
        }
    else:
        result = {
                'info' : ' the information ',
                'score' : ' 100 % '
        }

    return jsonify(result)

@app.route("/predict/",methods=['GET'])
def return_model_result():
    #date = request.args.get('date')
  #month = request.args.get('month')
    #myFeatures = [age_ ,gen_, hei_,wei_,aph_,apl_,cho_,glu_,smo_,alc_,act_]
    age_ = int(request.args.get('age'))
    gen_ = int(request.args.get('gen'))
    hei_ = int(request.args.get('hei'))
    wei_ = int(request.args.get('wei'))
    aph_ = int(request.args.get('aph'))
    apl_ = int(request.args.get('apl'))
    cho_ = int(request.args.get('cho'))
    glu_ = int(request.args.get('glu'))
    smo_ = int(request.args.get('smo'))
    alc_ = int(request.args.get('alc'))
    act_ = int(request.args.get('act'))

    result = my_ml_predictor.predict(age_ ,gen_, hei_,wei_,aph_,apl_,cho_,glu_,smo_,alc_,act_)
    result_dict = {
                'Answer': result,
                'msg':'Please refer to your doctor for a more detailed diagnosis',
                }
    return jsonify(result_dict)



if __name__ == "__main__":
    app.run()
    #return_model_result()
