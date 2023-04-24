from flask import Flask , render_template ,request , send_file
import os

from Authentificate import Authentication
from Directory import GsDirectory
from Authentificate import Account

authentification : Authentication
currentPath : str = ""
fixUsername : str = ""
gsDF = GsDirectory()
account = Account()
app = Flask(__name__,template_folder="templates",static_folder = 'static')

@app.route("/")
def Login():
    return render_template("login.html")

@app.route('/logout')
def lougout():
    return render_template("login.html")

@app.route("/authentification",methods =["GET","POST"])
def home():
    global fixUsername
    global currentPath
    username : str = request.form['username']
    password : str = request.form['password']
    authentification = Authentication(username,password)
    if username != "" :
        if authentification.authentification() == True:   
            fixUsername = username
            currentPath = "/home/"+username
            return render_template("index.html", directory = gsDF.chemin("/home/"+username))
    return render_template("login.html",erreur = "username or password incorrect")

@app.route('/addAccount',methods =["GET","POST"])
def createAccount():
    if request.method == 'GET':
        return render_template("createAccount.html")
    else :
        username : str = request.form['username']
        password : str = request.form['password']
        password2 : str = request.form['password2']
        if password != password2 : 
            return render_template("createAccount.html",erreur = "password incorrect")
        if account.addAccount(username,password) == False :
            return render_template("createAccount.html",erreur = "username already exists")
        return render_template("index.html",directory = gsDF.chemin("/home/"+username))



@app.route('/nbrfiles')
def nbrfiles():
    return render_template("index.html",directory = gsDF.chemin(currentPath),fil = str(gsDF.getnbrFichier(currentPath)))

@app.route('/nbrdir')
def nbrdirs():
    return render_template("index.html",directory = gsDF.chemin(currentPath),dir = str(gsDF.getnbrDirectory(currentPath)))

@app.route('/space')
def space():
    return render_template("index.html",directory = gsDF.chemin(currentPath),spa = str(gsDF.getsize(currentPath)))

@app.route('/search',methods =["GET","POST"])
def Search():
    filename : str = request.form['search']
    return render_template("index.html",directory = gsDF.rechercheFilesName(currentPath,filename))

@app.route("/download")
def download():
    gsDF.download(fixUsername)
    return send_file("/home/"+fixUsername+"/"+fixUsername+".zip", as_attachment=True)

@app.route('/<path:path>/',methods =["GET"])
def routefolders(path):
    try :
        global currentPath
        currentPath = "/"+path
        if os.path.isdir(currentPath):
            return render_template("index.html",directory = gsDF.chemin(currentPath))
        elif os.path.isfile(currentPath):
            f = open(currentPath)
            return render_template("index.html",text = f.read())
    except :
        return "erreur"


if __name__ == '__main__':
    app.run()