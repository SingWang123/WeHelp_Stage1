
# task 1
def find_and_print(messages, current_station):
    # 建立一個綠線的dic，有站名和站的順序
    green_line = {
    "Songshan":1,
    "Nanjing Sanmin":2,
    "Taipei Arena":3,
    "Nanjing Fuxing":4,
    "Soogjiang Nanjin":5,
    "Zhongshan":6,
    "Beimen":7,
    "Ximen":8,
    "Xiaonanmen":9,
    "Chiang Kai-Shek Memorial Hall":10,
    "Guting":11,
    "Taipower Building":12,
    "Gongguan":13,
    "Wanlong":14,
    "Jingmei":15,
    "Dapinglin":16,
    "Qizhang":17,
    "Xiaobitan":17.5,
    "Xindian City Hall":18,
    "Xindian":19,
    }

    #建立一個只有站名的List
    green_line_name = list(green_line.keys())

    #把messages的名稱抓出來
    messages_name = list(messages.keys())

    #創建一個誰在哪裡的物件
    messages_station ={}
    j=0
    while j<len(messages_name):
        i=0
        while i<len(green_line_name):
            if green_line_name[i] in messages[messages_name[j]]:
                messages_station[messages_name[j]]=green_line[green_line_name[i]] 
            i+=1
        j+=1

    #將所在位置編號-相關人員編號，找出最小的數字，存成一個 人：差距站數的物件
    messages_distance = {}
    i=0
    while i<len(messages_name):
        if messages_station[messages_name[i]] == 17.5:  #如果這個人在小碧潭，要特別處理
            messages_distance[messages_name[i]]= abs(green_line[current_station]-17)+1
        else: messages_distance[messages_name[i]]= abs(green_line[current_station]- messages_station[messages_name[i]])         
        i+=1 

    #找出差距最小的數字
    messages_distance_arr=list(messages_distance.values())
    messages_distance_min=min(messages_distance_arr)

    #用迴圈，反查有差距最小數字的人是誰
    i=0
    while i<len(messages_name):
        if messages_distance[messages_name[i]] == messages_distance_min:
            print(messages_name[i])
        i+=1



messages={
"Leslie":"I'm at home near Xiaobitan station.",
"Bob":"I'm at Ximen MRT station.",
"Mary":"I have a drink near Jingmei MRT station.",
"Copper":"I just saw a concert at Taipei Arena.",
"Vivian":"I'm at Xindian station waiting for you."
}

print("Task 1")

find_and_print(messages, "Wanlong") # print Mary
find_and_print(messages, "Songshan") # print Copper
find_and_print(messages, "Qizhang") # print Leslie
find_and_print(messages, "Ximen") # print Bob
find_and_print(messages, "Xindian City Hall") # print Vivian

# task 2

# 建立一個預約時間表，在function外

appointment={}

def book(consultants, hour, duration, criteria):
    
    #拉出所有諮商師的名字
    consultants_name=[]
    i=0
    while i<len(consultants):
        consultants_name.append(consultants[i]["name"])
        i+=1

     #一開始預約表為空字典，用諮商師的名字建立預約表
     #python中，字典為空是false，所以可以用if not判斷
    if not appointment:
        i=0
        while i<len(consultants_name):
            appointment[consultants_name[i]]=[]
            i+=1

    # 過濾出有時間的諮商師
    # 先建一個判斷式，判斷諮商師是否有時間
    def is_empty(n):
        i=0
        while i < duration:        
            if hour+i in appointment[n]:    #如果預約時間諮商師在預約表已有預約
             return False       #回傳 False
            i+=1
        return True #都沒有出現False，才傳Ture
    
    available_consultants = list(filter(is_empty,consultants_name))

    # 如果沒有可預約的諮商師，回傳No Service
    if not available_consultants:   #list為空，可以用if not判斷
        print("No Service")
        return "No Service"  #中斷函式，不然空值繼續進行下去會出錯

    # 拉出有空檔的諮商師和價格
    available_consultants_price={}
    for consultant in consultants:
        if consultant["name"] in available_consultants:
            available_consultants_price[consultant["name"]] = consultant["price"]
    
    # 拉出有空檔的諮商師的評價
    available_consultants_rate={}
    for consultant in consultants:
        if consultant["name"] in available_consultants:
            available_consultants_rate[consultant["name"]] = consultant["rate"]

    # 依據使用者的偏好，在有時間的諮商師中找到人選後，再將時段加入預約表
    if criteria=="price":
        i=0
        while i< len(available_consultants):
            if available_consultants_price[available_consultants[i]]==min(list(available_consultants_price.values())):
                print(available_consultants[i])
                j=0
                while j<duration:
                    appointment[available_consultants[i]].append(hour+j)
                    j+=1
            i+=1
           
    if criteria=="rate":
        i=0
        while i< len(available_consultants):
            if available_consultants_rate[available_consultants[i]]==max(list(available_consultants_rate.values())):
                print(available_consultants[i])
                j=0
                while j<duration:
                    appointment[available_consultants[i]].append(hour+j)
                    j+=1
            i+=1


consultants=[
{"name":"John", "rate":4.5, "price":1000},
{"name":"Bob", "rate":3, "price":1200},
{"name":"Jenny", "rate":3.8, "price":800}
]

print("Task 2")

book(consultants, 15, 1, "price") # Jenny
book(consultants, 11, 2, "price") # Jenny
book(consultants, 10, 2, "price") # John
book(consultants, 20, 2, "rate") # John
book(consultants, 11, 1, "rate") # Bob
book(consultants, 11, 2, "rate") # No Service
book(consultants, 14, 3, "price") # John




# task 3 
def func(*data):
# your code here
    middle_name=[] #設定middle_name變數，蒐集字串的中間字
    i=0
    while i<len(data):
        if len(data[i])==2:
            middle_name.append(data[i][len(data[i])-1])
        elif len(data[i])==5:
            middle_name.append(data[i][len(data[i])-3])
        else: 
            middle_name.append(data[i][len(data[i])-2])  
        i+=1

    # 統計所有中間字的數量，產生一個字典檔
    import collections
    middle_name_count=collections.Counter(middle_name)

    #將字典檔轉換成list
    middle_name_count_list=middle_name_count.items()
    middle_name_count_list=list(middle_name_count_list)

    #找出值為1的字
    middle_name_diff=[]
    i=0
    while i<len(middle_name_count_list):
        if middle_name_count_list[i][1] == 1:
            middle_name_diff.append(middle_name_count_list[i][0])
        i+=1       

    #依照值為1的字去找出名字，並處理差集為空格的狀態
    Ans=""
    i=0
    while i<len(data):
        if len(middle_name_diff) == 0:
            Ans="沒有"
        elif middle_name_diff[0] in data[i]:
            Ans+=data[i]
        elif len(middle_name_diff)>1 and middle_name_diff[1] in data[i]:
            Ans+="," + data[i]
        i+=1

    print(Ans)

print("Task 3")

func("彭大牆", "陳王明雅", "吳明") # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆") # print 夏曼藍波安

#func("郭宣雅", "夏曼藍波安", "郭宣恆","吳依寧","吳宣宣") # 測試有奇數相同字、差集兩個


# task 4：0,4,8,7,11,15,14....
def get_number(index):
    numseq=[]    
    i=0
    while i<100:
        if i%7==1:
            numseq.append(i)
            i-=1
        numseq.append(i)
        i+=4
    print(numseq[index])
    
# your code here
print("Task 4")

get_number(1) # print 4
get_number(5) # print 15
get_number(10) # print 25
get_number(30) # print 70
