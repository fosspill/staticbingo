from flask import Flask, jsonify, render_template, request
import hashlib
import base64
import html
import time
import os
import random
import shutil

app = Flask(__name__)

bingoboardtemplate = {
    "bingo1": None,  "bingo2": None,  "bingo3": None,  "bingo4": None,  "bingo5": None,
    "bingo6": None,  "bingo7": None,  "bingo8": None,  "bingo9": None,  "bingo10": None, 
    "bingo11": None, "bingo12": None, "bingo13": None, "bingo14": None, "bingo15": None, 
    "bingo16": None, "bingo17": None, "bingo18": None, "bingo19": None, "bingo20": None, 
    "bingo21": None, "bingo22": None, "bingo23": None, "bingo24": None, "bingo25": None
}
bingoboard = bingoboardtemplate.copy()

def reset_stamps():
    global bingoboard
    bingoboard = bingoboardtemplate.copy()

@app.route("/", methods=['GET'])
def home():
    return render_template('index.html', randvar=int(time.time()))
    
@app.route("/edit", methods=['GET'])
def editpage():
    return render_template('editation.html')

@app.route("/stamp", methods=['GET'])
def stamp():
    column = request.args.get("column")
    if(column):
        if bingoboard[column]:
            stampnum = None
        else:
            stampnum = "stamp" + str(random.randint(1, 16)) + ".png"
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
            filename = "static/texts/text{}.png".format(column)
            with open(filename, 'wb') as f:
                f.write(imgdata)
            return "Image Successfully Saved"
        except:
            return "Server Hurts Itself In Confusion"
    else:
        return "Invalid Data Sent To server"

@app.route("/shuffle", methods=['POST'])
def shuffle():
    srvpasshash="fc240ae4ea4420bd54101eded2e19a44d16607e7e850a26c917637f8a7e6bc6f2cff4a71ee30a5ef9cfa150dabb29661ef8f1e01b53eeece09325f8225096f01"
    password = hashlib.sha512(request.form.get("password").encode('utf-8')).hexdigest()
    
    if (srvpasshash == password):
        try:
            dirprefix="static/texts/"
            filelist = os.listdir(dirprefix)
            shuffled = filelist.copy()
            random.shuffle(shuffled)
            zipped = dict(zip(filelist, shuffled))

            #move files to a temp place and then rename to fit new list
            for x in filelist:
                fn = "{}{}".format(dirprefix, x)
                shutil.move(fn, fn + ".shuf")
            for i, (k, v) in enumerate(zipped.items()):
                oldfile = "{}{}".format(dirprefix, k)
                newfile = "{}{}".format(dirprefix, v)
                shutil.move(oldfile + ".shuf", newfile)
            reset_stamps()
            return "Shuffled! Hard-Refresh may be needed because this code is dirtier than your mom. (CTRL+R on the bingoboard)."
        except:
            return "Something that shouldn't go wrong went wrong!"
    else:
        return "Invalid Data Sent To server"


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

application = app    
if __name__ == "__main__":
    application.run("0.0.0.0", 2344)
