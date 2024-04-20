# 安裝BeautifulSoup
# 抓PTT 樂透版資料

lottery_data=[]
import urllib.request as req
#寫一個函式找文章內文的時間
def getTime(url):
    request=req.Request(url,headers={
    "cookie":"over18=1",
    "User-Agent":"Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.109 Safari/537.36 CrKey/1.54.248666"
    })
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")

    #用BS4解析資料
    import bs4
    root=bs4.BeautifulSoup(data,"html.parser")

    #回傳文章的時間
    publish_time = root.find_all("span",class_="article-meta-value")

    if len(publish_time)==0:
        return("本篇文章沒有顯示時間")
    else: return(publish_time[3].string)


#找出各看板頁面文章的標題、推文數、時間，並存到lottery_data陣列中
def getData(url): #建立一個函式，抓取各頁面資料
    #建立一個request附件，附加headers
    request=req.Request(url,headers={
        "cookie":"over18=1",
        "User-Agent":"Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.109 Safari/537.36 CrKey/1.54.248666"
    })
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")

    #用BS4解析資料
    import bs4
    root=bs4.BeautifulSoup(data,"html.parser")

    #找尋網頁標題和推文,存入陣列
    titles=root.find_all("div",class_="title") #尋找所有 class=title的 div標籤
    likes=root.find_all("div",class_="nrec")   

    i=0
    while i<len(titles):
        #找文章的網頁網址
        if titles[i].a != None: #如果標題並非沒a = 有a = 未刪除的文章
            articleLink=titles[i].find("a")
            articleLink="https://www.ptt.cc/"+articleLink["href"]
            if likes[i].string != None:
                lottery_data.append(titles[i].a.string+","+likes[i].string+","+getTime(articleLink)+"\n")
            else: 
                lottery_data.append(titles[i].a.string+","+"0"+","+getTime(articleLink)+"\n")
        else:
            if likes[i].string != None:
                lottery_data.append("已刪除的文章"+","+likes[i].string+",文章已刪除無連結"+"\n")
            else: 
                lottery_data.append("已刪除的文章"+","+"0"+",文章已刪除無連結"+"\n")
        i+=1



    #回傳前一頁的資料
    nextLink=root.find("a",string="‹ 上頁")
    return(nextLink["href"])
    

#抓前三頁的資料
page_url="https://www.ptt.cc/bbs/Lottery/index.html"
i=0
while i<3:
    page_url="https://www.ptt.cc/"+getData(page_url) #呼叫時就已經寫入首頁資料了
    i+=1

#將lottery_data存成文字檔
with open("article.csv",mode="w",encoding="utf-8") as file:
    file.writelines(lottery_data)




