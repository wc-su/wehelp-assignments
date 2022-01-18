from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# 首頁網址
@app.route("/")
def index():
    if "login_status" in session:
        # 使用者狀態為「已登入」，導向【成功頁面網址】
        return redirect("/member")
    else:
        # 使用者狀態為「未登入」，顯示【首頁】
        return render_template("index.html")

# 驗證功能網址
@app.route("/signin", methods=["POST"])
def signin():
    account = request.form["account"]
    password = request.form["password"]
    if account == "" or password == "":
        # 導向【失敗頁面網址】，並帶入錯誤訊息
        return redirect("/error/?message=請輸入帳號、密碼")
    elif account == "test" and password == "test":
        # 使用者狀態改為「已登入」，導向【成功頁面網址】
        session["login_status"] = "login"
        return redirect("/member")
    else:
        # 導向【失敗頁面網址】，並帶入錯誤訊息
        return redirect("/error/?message=帳號、或密碼輸入錯誤")

# 登出功能網址
@app.route("/signout")
def signout():
    # 使用者狀態改為「未登入」，導向【首頁網址】
    session.pop("login_status")
    return redirect("/")

# 成功頁面網址
@app.route("/member")
def member():
    if "login_status" in session:
        # 使用者狀態為「已登入」，顯示【成功頁面】
        return render_template("member.html")
    else:
        # 使用者狀態為未登入，導向【首頁網址】
        return redirect("/")

# 失敗頁面網址
@app.route("/error/")
def error():
    if "login_status" in session:
        # 使用者狀態為已登入，導向【成功頁面網址】
        return redirect("/member")
    
    # 動態取得錯誤訊息，顯示【失敗頁面】
    err_msg = request.args.get("message", "您尚未登入")
    return render_template("error.html", message = err_msg)

app.run(port=3000)