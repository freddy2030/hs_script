import requests
import json
import cv2 as cv
import threading

class saveCardsThread(threading.Thread):
    def __init__(self, threadName, **payload):
        threading.Thread.__init__(self)
        self.name = threadName
        self.payload = payload

    def run(self):
        # thread_lock.acquire()
        # print("@12",self.name, self.payload)
        # thread_lock.release()
        data = get_card_from_url(url, **self.payload)
        
        if not data:
            thread_lock.acquire()
            print("can not download cards", self.name) 
            thread_lock.release()
        else:    
            cards = data["cards"]
            for card in cards:
                save_img_from_url(card["imageUrl"], card["id"])
                
                thread_lock.acquire()
                id2Name = read_name_from_file()
                id2Name[card["id"]] = card["name"]
                write_name2file( id2Name )
                print("download:", card["id"])
                thread_lock.release()

def get_card_from_url(url, **payload):
    try:
        r = requests.post(url, params = payload)
        data = r.json()
        return data
    except requests.exceptions.RequestException as e:
        print("network error")
    return None
    # imageUrl = data["cards"][0]["imageUrl"]
    # js = json.dumps(r.json(), sort_keys = True, indent = 4, separators = (",", ":"))

def save_img_from_url(imgUrl, fileName):
    imgData = requests.get(imgUrl)
    img = imgData.content
    # with open("./hs_script/hs_card_data/"+"test_img.png", "wb") as file:
    with open("./hs_script/hs_card_data/cards/" + str(fileName) + ".png", "wb") as file:
        file.write(img)
        file.close()

def write_name2file(json_data):
    # test_json = {"111":"霸王枪"}
    json_str = json.dumps(json_data)
    with open("./hs_script/hs_card_data/cardId2Name.json", "w", encoding = "utf-8") as file:
        json.dump(json_data, file, ensure_ascii=False)
        file.close()

def read_name_from_file():
    with open("./hs_script/hs_card_data/cardId2Name.json", "r", encoding="utf-8") as file:
        json_str = json.load(file)
        file.close()
        return json_str


        

url = "https://hs.blizzard.cn/action/cards/query"
card_classes = ["druid", "hunter", "mage", "paladin", "priest", "rogue", "shaman", "warlock", "warrior", "neutral"]
payload = {
    "cardClass": "druid",
    "p": 1,
    "standard": 1,
}

threads = []
thread_lock = threading.Lock()

for cardClass in card_classes:
    payload['cardClass'] = cardClass
    data = get_card_from_url(url, **payload)
   
    if not data:
        continue
   
    pageNum = data["totalPage"]
    for i in range(1, pageNum + 1 ):
        payload["p"] = i
        threadName = cardClass + "-" + str(i)
        threads.append(saveCardsThread(threadName, **payload))  

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print("------end------")
# for cardClass in card_classes:
#     payload["cardClass"] = cardClass
#     data = get_card_from_url(url, payload)
#     pageNum = data["totalPage"]
#     for i in range(1, pageNum + 1 ):
#         payload["p"] = i
#         try:
#             thread.start_new_thread( print_time, ("Thread-1", 2, ) )
#         except:
#             print "Error: unable to start thread"
#     print("@15",pageNum)
#     print("------------------------------------------------")
    # print(json.dumps(data, indent = 4, separators=(',', ': '), ensure_ascii=False))



    