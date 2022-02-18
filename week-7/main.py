from flask import Flask, render_template, request, redirect, url_for, session
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

def connectDB():
    try:
        # 建立Connection物件
        conn = mysql.connector.connect(pool_name = "mypool",
                                       pool_size = 3,
                                       **db_settings)
        return conn
    except Exception as ex:
        print("*** mysql connect error", ex)
        return None

def insertDB(conn, data):
    reponse = { "status": "err", "count": 0 }

    try:
        # 建立Cursor物件
        with conn.cursor() as cursor:
            command = "INSERT INTO member(name, username, password, follower_count) VALUES(%(name)s, %(username)s, %(password)s, %(follower_count)s)"
            cursor.execute(command, data)
            
            reponse["status"] = "ok"
            reponse["count"] = cursor.rowcount

            conn.commit()
    except Exception as ex:
        conn.rollback()
        print("*** mysql insert error", ex)
    finally:
        cursor.close()

    return reponse

def queryDB(conn, data):
    reponse = { "status": "err", "count": 0, "data": None }

    try:
        with conn.cursor() as cursor:
            command = "SELECT * FROM member WHERE " + " AND ".join([k + ' = %(' + k + ')s' for k in data.keys()])
            cursor.execute(command, data)
            result = cursor.fetchone()
            count = cursor.rowcount

            reponse["status"] = "ok"
            reponse["data"] = result
            reponse["count"] = count

            conn.commit()
    except Exception as ex:
        print("*** mysql query error", ex)
    finally:
        cursor.close()

    return reponse

def updateDB(conn, data):
    reponse = { "status": "err", "count": 0 }

    try:
        with conn.cursor() as cursor:
            command = "UPDATE member SET name = %(name)s WHERE id = %(id)s"
            cursor.execute(command, data)

            reponse["status"] = "ok"
            reponse["count"] = cursor.rowcount

            conn.commit()
    except Exception as ex:
        conn.rollback()
        print("*** mysql update error", ex)
    finally:
        cursor.close()

    return reponse

# 連線資料庫
conn = connectDB()

@app.route("/api/members", methods = ["GET"])
def getMemberName():
    reponse = { "data": None }

    username = request.args.get("username", None)
    if username:
        result = queryDB(conn, {
            "username": username
        })
        # if result["status"] == "err":
        #     return redirect(url_for("error", message="系統錯誤"))
        if result["status"] == "ok" and int(result["count"]) > 0:
            query_data = result["data"]
            reponse["data"] = {
                "id": query_data[0],
                "name": query_data[1],
                "username": query_data[2]
            }

    return reponse

@app.route("/api/member", methods = ["POST"])
def updateMemberName():
    reponse = { "data": None }

    name = request.json["name"]

    result = updateDB(conn, {
        "name": name,
        "id": session["login_info"]["id"]
    })
    # if result["status"] == "err":
    #     return redirect(url_for("error", message="系統錯誤"))
    if result["status"] == "ok":
        reponse = { "ok": True }

    return reponse

# 首頁網址
@app.route("/", methods=["GET"])
def index():
    if(conn == None):
        return redirect(url_for("error", message="系統錯誤"))
    if "login_info" in session:
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
        result = queryDB(conn, {
            "username": username,
            "password": password
        })
        if result["status"] == "err":
            return redirect(url_for("error", message="系統錯誤"))
        if result["status"] == "ok" and int(result["count"]) > 0:
            # 使用者狀態改為「已登入」，導向【成功頁面網址】
            query_data = result["data"]
            session["login_info"] = {
                "id": query_data[0],
                "name": query_data[1]
            }
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
        result = queryDB(conn, {
            "username": username
        })
        if result["status"] == "err":
            return redirect(url_for("error", message="系統錯誤"))
        if result["status"] == "ok" and int(result["count"]) > 0:
            return redirect(url_for("error", message = "【註冊帳號】帳號已經被註冊"))
        # 新增至資料庫
        result = insertDB(conn, {
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
    session.pop("login_info")
    return redirect(url_for("index"))

# 成功頁面網址
@app.route("/member/", methods=["GET"])
def member():
    if "login_info" in session:
        # 使用者狀態為「已登入」，顯示【成功頁面】
        return render_template("member.html", name = session["login_info"]["name"])
    else:
        # 使用者狀態為未登入，導向【首頁網址】
        return redirect(url_for("index"))

# 失敗頁面網址
@app.route("/error/", methods=["GET"])
def error():
    if "login_info" in session:
        # 使用者狀態為已登入，導向【成功頁面網址】
        return redirect(url_for("member"))
    
    # 動態取得錯誤訊息，顯示【失敗頁面】
    err_msg = request.args.get("message", "您尚未登入")
    return render_template("error.html", message = err_msg)

app.run(port=3000)