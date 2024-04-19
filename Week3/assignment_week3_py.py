#倒進第一份來源資料
import urllib.request as request
import json
src="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
with request.urlopen(src) as response:
    data=json.load(response)

# 倒進第二份來源資料
import urllib.request as request2
import json
src2="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"
with request.urlopen(src2) as response2:
    data2=json.load(response2)


# 抓出第一份資料內，景點的key值
key=[]
for i in data["data"]["results"][0].keys():
    key.append(i)

# 抓出第二份資料內，景點的key值
key2=[]
for i in data2["data"][0].keys():
    key2.append(i)

#找出檔案1和2的交集，看要用哪個值為基準合併檔案
a = set(key)
b = set(key2) 
print(a&b)  #得到'SERIAL_NO'是兩筆資料的共同鍵

# 使用'SERIAL_NO' 將data2資料對應合併到data

i=0
while i<len(data["data"]["results"]):
    j=0
    while j<len(data2["data"]):
        if data["data"]["results"][i]["SERIAL_NO"] == data2["data"][j]["SERIAL_NO"]:
            data["data"]["results"][i]["MRT"]=data2["data"][j]["MRT"]
            data["data"]["results"][i]["address"]=data2["data"][j]["address"]
        j+=1
    i+=1

# 先把data內景點需要的資料一個一個整理好
# 整理景點行政區
district_list=["中正區","萬華區","中山區","大同區","大安區","松山區","信義區","士林區","文山區","北投區","內湖區","南港區"]

address_list={}
for i in data["data"]["results"]:
    for j in district_list:
        if j in i["address"]:
            address_list[i["stitle"]]=j

# 把景點的照片網址列出來，取出第一張（用https://切割字串後再加回去），因為用https切割，產出的List[0]會是空字串
photofile_list={}
for i in data["data"]["results"]:
    photo=i["filelist"]
    photo_first=photo.split("https://")
    photofile_list[i["stitle"]]="https://"+ photo_first[1]+"\n"
    

# 列出景點:["longitude"]+["latitude"]
# 依據景點名稱合併景點資訊
longitude_list={}
for i in data["data"]["results"]:
    longitude_list[i["stitle"]]=i["longitude"]+","+i["latitude"]

spot=[]
for i in longitude_list:
    spot.append(i+","+address_list[i]+","+longitude_list[i]+","+photofile_list[i])

#存成文字檔
with open("spot.csv",mode="w",encoding="utf-8") as file:
    file.writelines(spot)


# 把data裡面的MRT都拉出來（data是以景點為主，拉出data的MRT會依照景點位置有重複）
MRT=[]
i=0
while i<len(data["data"]["results"]):
    MRT.append(data["data"]["results"][i]["MRT"])
    i+=1

# 把MRT的List轉為字典，以對應景點
MRT_spot={}
for i in MRT:
    MRT_spot[i]=""

# 把各站的景點名稱列出來
j=0
while j<len(data["data"]["results"]):
    for i in MRT_spot:
        if i == data["data"]["results"][j]["MRT"]:
            MRT_spot[i]+=data["data"]["results"][j]["stitle"]+","
    j+=1

# 把MRT_spot變成一個List，方便輸出
MRT_spot_list=[]
for i in MRT_spot:
    MRT_spot_list.append(i+","+MRT_spot[i][:-1]+"\n")

# 存成一個文件 mar.csv
with open("mrt.csv",mode="w",encoding="utf-8") as file:
     file.writelines(MRT_spot_list)




