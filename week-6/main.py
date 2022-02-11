from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
import mysql.connector

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# 資料庫參數設定
db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "db": "website",
    "charset": "utf8"
}

def insertDB(data):
    try:
        # 建立Connection物件
        conn = mysql.connector.connect(**db_settings)
        # 建立Cursor物件
        with conn.cursor() as cursor:
            command = "INSERT INTO member(name, username, password, follower_count) VALUES(%(name)s, %(username)s, %(password)s, %(follower_count)s)"
            cursor.execute(command, data)
            # 儲存變更
            conn.commit()
            return {
                "status": "ok",
                "count": cursor.rowcount,
                "result": ()
            }
    except Exception as ex:
        print("*** mysql insert error", ex)
        conn.rollback()
        return {
            "status": "err",
            "count": 0,
            "result": ()
        }

def queryDB(data):
    try:
        # 建立Connection物件
        conn = mysql.connector.connect(**db_settings)
        # 建立Cursor物件
        with conn.cursor() as cursor:
            command = "SELECT name FROM member WHERE " + " AND ".join([k + ' = %(' + k + ')s' for k in data.keys()])
            cursor.execute(command, data)
            result = cursor.fetchone()
            return {
                "status": "ok",
                "count": cursor.rowcount,
                "result": result
            }
    except Exception as ex:
        print("*** mysql query error", ex)
        return {
            "status": "err",
            "count": 0,
            "result": ()
        }

# 首頁網址
@app.route("/", methods=["GET"])
def index():
    if "login_name" in session:
        # 使用者狀態為「已登入」，導向【成功頁面網址】
        return redirect(url_for("member"))
    else:
        # 使用者狀態為「未登入」，顯示【首頁】
        message = ""
        if "signup-msg" in session:
            message = session["signup-msg"]
            session.pop("signup-msg")
        return render_template("index.html", message = message)

# 驗證功能網址
@app.route("/signin/", methods=["POST"])
def signin():
    username = request.form["username"].rstrip()
    password = request.form["password"].rstrip()
    if username and password:
        result = queryDB({
            "username": username,
            "password": password
        })
        if result["status"] == "err":
            return redirect(url_for("error", message="系統錯誤"))
        if result["status"] == "ok" and int(result["count"]) > 0:
            # 使用者狀態改為「已登入」，導向【成功頁面網址】
            session["login_name"] = result["result"][0]
            return redirect(url_for("member"))
    elif username == "" and password == "":
        # 導向【失敗頁面網址】，並帶入錯誤訊息
        return redirect(url_for("error", message="【登入系統】請輸入帳號、密碼"))
    # 導向【失敗頁面網址】，並帶入錯誤訊息
    return redirect(url_for("error", message="【登入系統】帳號或密碼輸入錯誤"))

# 註冊功能網址
@app.route("/signup/", methods=["POST"])
def signup():
    name = request.form["name"]
    username = request.form["username"]
    password = request.form["password"]
    if name == "" or username == "" or password == "":
        return redirect(url_for("error", message = "【註冊帳號】請輸入姓名、帳號、密碼"))
    else:
        # 查詢資料庫
        result = queryDB({
            "username": username
        })
        if result["status"] == "err":
            return redirect(url_for("error", message="系統錯誤"))
        if result["status"] == "ok" and int(result["count"]) > 0:
            return redirect(url_for("error", message = "【註冊帳號】帳號已經被註冊"))
        # 新增至資料庫
        result = insertDB({
            "name": name,
            "username": username,
            "password": password,
            "follower_count": 0
        })
        if result["status"] == "err":
            return redirect(url_for("error", message="系統錯誤"))
        session["signup-msg"] = "↓↓↓ 帳號註冊成功，請登入系統 ↓↓↓"
        return redirect(url_for("index"))

# 登出功能網址
@app.route("/signout/", methods=["GET"])
def signout():
    # 使用者狀態改為「未登入」，導向【首頁網址】
    session.pop("login_name")
    return redirect(url_for("index"))

# 成功頁面網址
@app.route("/member/", methods=["GET"])
def member():
    if "login_name" in session:
        # 使用者狀態為「已登入」，顯示【成功頁面】
        return render_template("member.html", name = session["login_name"])
    else:
        # 使用者狀態為未登入，導向【首頁網址】
        return redirect(url_for("index"))

# 失敗頁面網址
@app.route("/error/", methods=["GET"])
def error():
    if "login_name" in session:
        # 使用者狀態為已登入，導向【成功頁面網址】
        return redirect(url_for("member"))
    
    # 動態取得錯誤訊息，顯示【失敗頁面】
    err_msg = request.args.get("message", "您尚未登入")
    return render_template("error.html", message = err_msg)

app.run(port=3000)