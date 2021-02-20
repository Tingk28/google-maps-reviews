from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time
import os.path
import sys
'''
readme:python main.py file_name data_name sort_index fliter
sort_index: 1-4 相關/新/高/低
e.g. python main.py store_list.txt 億進寢具.json 3 4

'''


def load_comment_section(link):  # 載入留言區並寫入分店名稱
    global store, number
    driver.get(link)  # 連線至指定的網頁
    time.sleep(5)
    try:
        store = driver.find_element_by_tag_name("h1").text+'.json'
        number_str = driver.find_element(By.CSS_SELECTOR, ".reviews-tap-area > span > .widget-pane-link").text
        number = int(number_str.split(" ")[0].replace(',','')) # 修改留言總數
        driver.find_element(By.CSS_SELECTOR, ".reviews-tap-area > span > .widget-pane-link").click()
        if int(sys.argv[3]) > 0:  # sort index
            #sys.argv[3] = int(sys.argv[3])+25738
            #element = "[vet='" + str(sys.argv[3]) + "']"
            try:
                driver.find_element_by_css_selector("[aria-label='排序評論']").click()
                print("click0")
                driver.find_element_by_css_selector("[vet='25740']").click()
                #driver.find_element_by_css_selector("[aria-label='排序評論']").click()
                #driver.find_element_by_css_selector(element).click()
                time.sleep(4)
            except Exception as e:
                print(e)
                print("無法排序")
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
    for i in dataset:
        comment = []
        comment_id = i.find_element_by_class_name("section-review-title").text
        star = i.find_element_by_class_name("section-review-stars").get_attribute("aria-label")
        text = i.find_element_by_class_name("section-review-text").text
        date = i.find_element_by_class_name("section-review-publish-date").text
        comment.append(int(star[1]))
        comment.append(text)
        comment.append(date)
        comment_dict[comment_id] = comment
    return comment_dict
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
options.add_argument("--window-size=%s" % "720,780")
driver = webdriver.Chrome(r'C:\Users\alex9\PycharmProjects\pythonProject\fb_hw_helper\fb_login\chromedriver.exe', options =options)
driver.implicitly_wait(15)  #隱性等待，至多15秒
store_list = open(sys.argv[1], "r+").read().split("\n")
comment_list = []

for url in store_list:
    store = ''  #店名(json檔名)
    number = 0
    load_comment_section(url)
    print(store)
    print(number)
    if number > 0:
        pre_number = 0
        time_stamp = time.time()
        temp_comment_list = []
        while len(temp_comment_list) < number:
            temp_comment_list = get_comment()
            if len(temp_comment_list) != pre_number:
                pre_number = len(temp_comment_list)
                time_stamp = time.time()
                if int(sys.argv[3]) > 0:
                    if sys.argv[3] == 2: # 新
                        print("opppppppps")
                    elif sys.argv[3] == 3 and int(comment_list[-1].find_element_by_class_name("section-review-stars").get_attribute("aria-label")[1])<sys.argv[4]: # 高
                        break
                    elif sys.argv[3] == 4 and int(comment_list[-1].find_element_by_class_name("section-review-stars").get_attribute("aria-label")[1])>sys.argv[4]: # 低
                        break
            elif time.time()-time_stamp > 90:
                print("time_out")
                break
            try:
                driver.find_element_by_class_name('section-loading').click()  # 向下滾動
            except Exception as e:
                print(e)
                break
        print("沒有更多留言")
        comment_list += temp_comment_list


# if ".json" not in sys.argv[2]:
    sys.argv[2] = store[:12].replace("/","")+".json"
with open(os.path.join(os.getcwd(),'data',sys.argv[2]), 'w', encoding='utf-8') as f:
    json.dump(parsing(comment_list),f,ensure_ascii=False)