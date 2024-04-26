from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

# 設定 SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key = "my_secret_key")

app.mount("/static",StaticFiles(directory="static"),name="static")

templates = Jinja2Templates(directory="templates")

#首頁
@app.get("/", response_class = HTMLResponse)
async def login(request: Request):
    if "SIGNED-IN" in request.session and request.session["SIGNED-IN"] == True:  # 第一次打開時必須檢查session是否存在，不然會500錯誤；只要成功登入一次後，就算登出，這錯誤也不會出現，因為SIGNED-IN 已經存在，只是值變False
        return RedirectResponse(url = "/member")  #一般成功登入後，不會讓使用者去登入頁再登入一次，邏輯上有點奇怪
    else:  
        return templates.TemplateResponse("login.html", {"request": request})

# Vertification Endpoint
@app.post("/signin")
async def login(request:Request, username: str = Form(None), password: str = Form(None)):
    # form()內必須要有None，預設值為None表示允許空值送出；若沒有加None會報錯422
    if not username or not password:
        return RedirectResponse(url = "/error?error_type=請輸入帳號和密碼", status_code = 303)
    #帳密都是test，轉向成功頁面
    elif username == "test" and  password == "test": 
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
async def member(request: Request):
    request.session["SIGNED-IN"] = False 
    return RedirectResponse(url = "/")

# 計算的API
@app.post("/calculate")
async def calculate(request:Request, number: int = Form(None)):
   return RedirectResponse(url = f"/square/{number}", status_code = 303) #f-string 的 f 表示 "formatted"，它告訴 Python 解釋器將字串格式化為 f-string。 

# Squared Number Page,顯示結果的Api 
@app.get("/square/{number}", response_class = HTMLResponse)
async def squared(request:Request, number: int):
    result = number ** 2
    return templates.TemplateResponse("squared.html", {"request": request, "number": result})

