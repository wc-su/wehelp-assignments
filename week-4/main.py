from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def index():
    if "login" in session:
        return redirect("/member")
    else:
        return render_template("index.html")

@app.route("/signin", methods=["POST"])
def signin():
    account = request.form["account"]
    password = request.form["password"]
    if account == "" or password == "":
        return redirect("/error/?message=請輸入帳號、密碼")
    elif account == "test" and password == "test":
        session["login"] = "login"
        return redirect("/member")
    else:
        return redirect("/error/?message=帳號、或密碼輸入錯誤")

@app.route("/signout")
def signout():
    session.pop("login")
    return redirect("/")

@app.route("/member")
def member():
    if "login" in session:
        return render_template("member.html")
    else:
        return redirect("/")

@app.route("/error/")
def error():
    if "login" in session:
        return redirect("/member")
    errMsg = request.args.get("message", "")
    return render_template("error.html", message = errMsg)

app.run(port=3000)