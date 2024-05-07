from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

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

# sql_search = "SELECT username FROM member"
# mycursor.execute(sql_search)
# result = mycursor.fetchall()
# print(('test1234',) in result)

# sql = "insert into member (name, username, password) values (%s, %s, %s)"
# val = ("測試塞資料","test012","1234")

# def mytest():
#     if (val[1],) in result:
#         print("帳號已存在")
#     else:
#         mycursor.execute(sql,val)
#         mydb.commit()

# mytest()



# sql_delete = "delete from member where username ='test123'"
# mycursor.execute(sql_delete)
# mydb.commit()



sql_search2 = "SELECT * FROM member"
mycursor.execute(sql_search2)
myresult = mycursor.fetchall()
for x in myresult:
   print(x)


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
    sql_search_username = "SELECT username FROM member"
    mycursor.execute(sql_search_username)
    result_username = mycursor.fetchall()
    if (username_signup,) in result_username:
        return "帳號已存在"
    else:
        sql = "insert into member (name, username, password) values (%s, %s, %s)"
        val = (name,username_signup,password_signup)
        mycursor.execute(sql,val)
        mydb.commit()
        return "註冊成功"

# Vertification Endpoint
@app.post("/signin")
async def login(request:Request, username_signin: str = Form(None), password_signin: str = Form(None)):
    # form()內必須要有None，預設值為None表示允許空值送出；若沒有加None會報錯422
    if not username_signin or not password_signin:
        return RedirectResponse(url = "/error?error_type=請輸入帳號和密碼", status_code = 303)
    #帳密都是test，轉向成功頁面
    elif username_signin == "test" and  password_signin == "test": 
        request.session["SIGNED-IN"] = True 
        return RedirectResponse(url = "/member", status_code = 303) #RedirectResponse會用post的方式取資料，但/member 是get，需加上303狀態才不會出現505錯誤。
    else:
        return RedirectResponse(url = "/error?error_type=帳號或密碼錯誤", status_code = 303)

# Success Page
@app.get("/member", response_class = HTMLResponse)
async def login(request: Request):
    if "SIGNED-IN" not in request.session or request.session["SIGNED-IN"] == False :
        return RedirectResponse(url = "/")
    else:  
        return templates.TemplateResponse("member.html", {"request": request})

# Error Page
@app.get("/error", response_class = HTMLResponse)
async def member(request: Request, error_type):
    return templates.TemplateResponse("error.html", {"request": request, "error_type":error_type})

# Signout Endpoint
@app.get("/signout", response_class = HTMLResponse)
async def signout(request: Request):
    request.session["SIGNED-IN"] = False 
    return RedirectResponse(url = "/")



