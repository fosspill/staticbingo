from flask import Flask, jsonify, render_template, request
from random import randint
import hashlib
import base64
import html


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
    return render_template('index.html')
    
@app.route("/edit", methods=['GET'])
def editpage():
    return render_template('editation.html')

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
def stamps():
    return jsonify(bingoboard)
    
@app.route("/saveimage", methods=['POST'])
def savimg():
    srvpasshash="fc240ae4ea4420bd54101eded2e19a44d16607e7e850a26c917637f8a7e6bc6f2cff4a71ee30a5ef9cfa150dabb29661ef8f1e01b53eeece09325f8225096f01"
    base64str = request.form.get("base64").replace("data:image/png;base64,","") 
    password = hashlib.sha512(request.form.get("password").encode('utf-8')).hexdigest()
    column = request.form.get("column")
    base64s = base64str.encode("utf-8")
    if (srvpasshash == password and int(column) > 0):
        try:
            print (base64str)
            imgdata = base64.b64decode(base64str)
            filename = "static/text{}.png".format(column)
            with open(filename, 'wb') as f:
                f.write(imgdata)
            return "Image Successfully Saved"
        except:
            return "Server Hurts Itself In Confusion"
    else:
        return "Invalid Data Sent To server"

application = app    
if __name__ == "__main__":
    application.run("0.0.0.0", 2344)
