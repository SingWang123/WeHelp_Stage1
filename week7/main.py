from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# 連接上資料庫
import mysql.connector
mydb = mysql.connector.connect(
  host = "localhost",
  user ="root",
  password = "12345678",
  database = "website"
)

mycursor = mydb.cursor()

# 設定 SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key = "my_secret_key")

# Jinja2 Templates
app.mount("/static",StaticFiles(directory="static"),name="static")

templates = Jinja2Templates(directory="templates")

#Home
@app.get("/", response_class = HTMLResponse)
async def login(request: Request):
    if "SIGNED-IN" in request.session and request.session["SIGNED-IN"] == True:  # 第一次打開時必須檢查session是否存在，不然會500錯誤；只要成功登入一次後，就算登出，這錯誤也不會出現，因為SIGNED-IN 已經存在，只是值變False
        return RedirectResponse(url = "/member")  #一般成功登入後，不會讓使用者去登入頁再登入一次，邏輯上有點奇怪
    else:  
        return templates.TemplateResponse("home.html", {"request": request})

# Signup Endpoint
@app.post("/signup")
async def signup(request:Request, name: str = Form(None), username_signup: str = Form(None), password_signup: str = Form(None)):
    # 檢查username是否有重複    
    sql_search_username = "SELECT username FROM member WHERE username = %s"
    val_search_username = (username_signup,)
    mycursor.execute(sql_search_username,val_search_username)
    result_username = mycursor.fetchall()
    if len(result_username) == 0:
        sql = "INSERT INTO member (name, username, password) VALUES (%s, %s, %s)"
        val = (name,username_signup,password_signup)
        mycursor.execute(sql,val)
        mydb.commit()
        return RedirectResponse(url = "/", status_code = 303)
    else:
        return RedirectResponse(url = "/error?error_type=帳號已存在", status_code = 303)

# Vertification Endpoint
@app.post("/signin")
async def login(request:Request, username_signin: str = Form(None), password_signin: str = Form(None)):
    # form()內必須要有None，預設值為None表示允許空值送出；若沒有加None會報錯422
    # 檢查帳號和密碼是否和資料庫一致
    sql_login = "SELECT username, password FROM member WHERE username = %s AND password = %s"
    val_login = (username_signin,password_signin)
    mycursor.execute(sql_login,val_login)
    result_login = mycursor.fetchall()
    if len(result_login) == 0:
        #帳密不正確，轉到錯誤頁
        return RedirectResponse(url = "/error?error_type=帳號或密碼輸入錯誤", status_code = 303)
    else:
        #撈取資料庫該位用戶id,name,username加入session
        sql_memberdata = "SELECT id, username, name FROM member WHERE username = %s"
        val_memberdata = (username_signin,)
        mycursor.execute(sql_memberdata,val_memberdata)
        memberdata = mycursor.fetchall()
        request.session["USER-STATE"] = [memberdata[0][0],memberdata[0][1],memberdata[0][2]]
        request.session["SIGNED-IN"] = True
        return RedirectResponse(url = "/member", status_code = 303) #RedirectResponse會用post的方式取資料，但/member 是get，需加上303狀態才不會出現505錯誤。    

# Success Page
@app.get("/member", response_class = HTMLResponse)
async def login(request: Request):
    if "SIGNED-IN" not in request.session or request.session["SIGNED-IN"] == False :
        return RedirectResponse(url = "/")
    else:  
        # 從session中獲取使用者名稱 / ID(比對留言者時使用)
        user_state = request.session.get("USER-STATE")
        login_name = user_state[2]
        user_id = user_state[0]
        # 撈取留言內容
        sql_search_message = "SELECT member.name, message.content, message.id, message.member_id, message.time FROM message INNER JOIN member ON message.member_id = member.id ORDER BY time DESC"
        mycursor.execute(sql_search_message)
        messages = mycursor.fetchall()
        return templates.TemplateResponse("member.html", {"request": request, "login_name":login_name, "user_id":user_id, "messages":messages })

# Error Page
@app.get("/error", response_class = HTMLResponse)
async def member(request: Request, error_type):
    return templates.TemplateResponse("error.html", {"request": request, "error_type":error_type})

# Signout Endpoint
@app.get("/signout", response_class = HTMLResponse)
async def signout(request: Request):
    request.session["SIGNED-IN"] = False
    del request.session["USER-STATE"] 
    return RedirectResponse(url = "/")

# CreateMessage Endpoint
@app.post("/createMessage")
async def createMessage(request:Request, message_content: str = Form(None)):
    # 將留言訊息寫入資料庫，根據session資料取得留言者id
    user_state = request.session.get("USER-STATE")
    sql = "INSERT INTO message (member_id, content) VALUES (%s, %s)"
    val = (user_state[0],message_content)
    mycursor.execute(sql,val)
    mydb.commit()
    return RedirectResponse(url = "/member", status_code = 303) #RedirectResponse會用post的方式取資料，但/member 是get，需加上303狀態才不會出現505錯誤。

# DeleteMessage Endpoint
@app.post("/deleteMessage")
async def deleteMessage(request:Request, message_id: str = Form(None)):
    #檢查傳送刪除請求的是不是該留言id的帳號
    user_state = request.session.get("USER-STATE")
    user_id = user_state[0]
    sql = "SELECT member_id FROM message WHERE id = %s"
    val = (message_id,)
    mycursor.execute(sql,val)
    user = mycursor.fetchall()
    if user[0][0] == user_id:
        sql_delete = "delete from message where id = %s"
        val_delete = (message_id,)
        mycursor.execute(sql_delete,val_delete)
        mydb.commit()
        return RedirectResponse(url = "/member", status_code = 303) #RedirectResponse會用post的方式取資料，但/member 是get，需加上303狀態才不會出現505錯誤。 
    else:
        return {"error": "您沒有權限刪除留言"}  
    
# Member Query API (用query param方式帶參數)
@app.get("/api/member")
async def querymember(request:Request, query_username = str):
    sql = "SELECT id, name, username From member WHERE username = %s"
    val = (query_username,)
    mycursor.execute(sql,val)
    memberdata = mycursor.fetchall()
    # 如果找不到用戶帳號，回傳"data":null
    if request.session["SIGNED-IN"] == False or len(memberdata) == 0:
        return JSONResponse(content = {"data":None})
    else:
        return JSONResponse(content= {
            "data":{
                "id" : memberdata[0][0],
                "name" : memberdata[0][1],
                "username" : memberdata[0][2]
            }
        })

#Name Update API
@app.patch("/api/member")
async def updatename(request:Request):
    # 檢查使用者是否有登入
    if  "SIGNED-IN" not in request.session or request.session["SIGNED-IN"] == False :
        return JSONResponse(content = {"error":True})
    else:
        #用request.json() 來解析request傳來的json資料
        data = await request.json()
        update_name = data.get("name")

        # 從session 取得該用戶的原本名稱
        user_state = request.session.get("USER-STATE")
        user_name = user_state[2]
        
        # 依據session取得請求的用戶名稱，並進行更換
        sql_update = "UPDATE member SET name = %s WHERE name = %s"
        val_update = (update_name,user_name)
        mycursor.execute(sql_update,val_update)
        mydb.commit()
        # session內的用戶名稱也要修改
        request.session["USER-STATE"][2] = update_name
        return JSONResponse(content = {"ok":True})