import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from time import sleep
import datetime

def getchromedriver(root_path = "./asset"):
    try:
        ChromeDriverPath = str(ChromeDriverManager(log_level=0).install())
        with open(root_path + "/ChromeDriverPath.txt", "w") as file:
            file.write(ChromeDriverPath)
            file.close()
        return ChromeDriverPath
    except:
        print("Report_Tool_log : 인터넷이 연결되어 있지 않습니다!")
        return


def init_chrome_driver(root_path = "./asset"):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('window-size=955,831')
    # chrome_options.headless = True

    try:
        with open(root_path + "/ChromeDriverPath.txt", "r") as file:
            ChromeDriverPath = file.readline()
            file.close()
        svc = Service(ChromeDriverPath)
        # svc.creationflags = CREATE_NO_WINDOW
        browser = webdriver.Chrome(service=svc, options=chrome_options)
    except:
        ChromeDriverPath = getchromedriver(root_path)
        if ChromeDriverPath == None: return
        svc = Service(ChromeDriverPath)
        # svc.creationflags = CREATE_NO_WINDOW
        browser = webdriver.Chrome(service=svc, options=chrome_options)

    return browser

def crawling_chungyak():
    getchromedriver()
    browser = init_chrome_driver()
    browser.get("https://www.applyhome.co.kr/ai/aib/selectSubscrptCalenderView.do")
    sleep(1)

    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    notices = soup.select('tbody > tr')
    df = pd.DataFrame(columns=['time', 'content'])
    for week in notices:
        for w in week:
            if len(w.select('b.blind')) == 0:
                continue
            time = w.select('b.blind')[0]
            content = w.select('span.cal_lb')
            for c in content:
                print(time.text)
                print(c.text)
                new_one = pd.DataFrame([[time.text, c.text]], columns=['time', 'content'])
                df = pd.concat([df, new_one], ignore_index=True)

    now = datetime.datetime.now()
    df.to_csv(f"./{now.strftime('%Y-%m-%d')}.csv", encoding='utf-8', index=False)

    popup = browser.find_element_by_tag_name('iframe')
    browser.switch_to.frame(popup)
    soup = browser.page_source


# crawling_chungyak()