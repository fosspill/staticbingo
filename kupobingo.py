from flask import Flask, jsonify, render_template, request
from random import randint
from collections import OrderedDict



app = Flask(__name__)

bingoboard = {
    "bingo1": None,  "bingo2": None,  "bingo3": None,  "bingo4": None,  "bingo5": None,
    "bingo6": None,  "bingo7": None,  "bingo8": None,  "bingo9": None,  "bingo10": None, 
    "bingo11": None, "bingo12": None, "bingo13": None, "bingo14": None, "bingo15": None, 
    "bingo16": None, "bingo17": None, "bingo18": None, "bingo19": None, "bingo20": None, 
    "bingo21": None, "bingo22": None, "bingo23": None, "bingo24": None, "bingo25": None, 
}

@app.route("/", methods=['GET'])
def home():
    search = request.args.get("user")
    return render_template('index.html')
    
@app.route("/stamp", methods=['GET'])
def stamp():
    column = request.args.get("column")
    print(column)
    if(column):
        if bingoboard[column]:
            stampnum = None
        else:
            stampnum = "stamp" + str(randint(1, 16)) + ".png"
        bingoboard[column] = stampnum
        return "Success"
    return "Something went wrong"
    
@app.route("/stamps", methods=['GET'])
def rolls():
    return jsonify(bingoboard)
    
application = app    
if __name__ == "__main__":
    application.run("0.0.0.0", 2344)
