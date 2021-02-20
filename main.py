from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time
import os.path

def load_comment_section(link):  # 載入留言區並寫入分店名稱
    global store, number
    driver.get(link)  # 連線至指定的網頁
    time.sleep(5)
    try:
        store = driver.find_element_by_tag_name("h1").text+'.json'
        number_str = driver.find_element(By.CSS_SELECTOR, ".reviews-tap-area > span > .widget-pane-link").text

        number = int(number_str.split(" ")[0].replace(',','')) # 修改留言總數
        driver.find_element(By.CSS_SELECTOR, ".reviews-tap-area > span > .widget-pane-link").click()
    except Exception as e:
        print(e)
        print(store[:-5]+" 沒有評論")

def get_comment():
    time.sleep(3)
    comment_list = driver.find_elements_by_class_name("section-review-content")
    print(store[:-5]+" 完成度："+str(len(comment_list))+","+str(number)+"   "+str(len(comment_list)/number))
    return comment_list


def parsing(dataset):
    comment_dict = {}
    for i in comment_list:
        comment = []
        comment_id = i.find_element_by_class_name("section-review-title").text
        star = i.find_element_by_class_name("section-review-stars").get_attribute("aria-label")
        text = i.find_element_by_class_name("section-review-text").text
        comment.append(int(star[1]))
        comment.append(text)
        comment_dict[comment_id] = comment
    return comment_dict

options = webdriver.ChromeOptions()
#options.add_argument("--headless")
options.add_argument("--window-size=%s" % "1920,1080")
driver = webdriver.Chrome(r'C:\Users\alex9\PycharmProjects\pythonProject\fb_hw_helper\fb_login\chromedriver.exe', options =options)
driver.implicitly_wait(15)  #隱性等待，至多15秒
store_list = open("store_list.txt", "r+").read().split("\n")


for url in store_list:
    store = ''  #店名(json檔名)
    number = 0
    load_comment_section(url)
    if number>0:
        comment_list = []
        pre_number = 0
        time_stamp = time.time()
        while len(comment_list)<number:
            comment_list = get_comment()
            if len(comment_list)!=pre_number:
                pre_number=len(comment_list)
                time_stamp = time.time()
            elif time.time()-time_stamp>90:
                print("time_out")
                break
            try:
                driver.find_element_by_class_name('section-loading').click()  # 向下滾動
            except:
                print("沒有更多留言")
                break
        with open(os.path.join(os.getcwd(),'data',store), 'w', encoding='utf-8') as f:
            json.dump(parsing(comment_list),f,ensure_ascii=False)