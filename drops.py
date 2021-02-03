import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep

dir_path = os.path.dirname(os.path.realpath(__file__))
file = dir_path + r'\chromedriver.exe'

def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def wait_auth():
    while(True):
        if str(driver.current_url) == 'https://www.twitch.tv/?no-reload=true':
            break
        elif str(driver.current_url) == 'https://www.twitch.tv/':
            break
        else:
            sleep(2)
    return True

def check_online():
    offline = check_exists_by_xpath('//*[@id="root"]/div/div[2]/div/main/div[2]/div[3]/div/div/div[2]/div[1]/div[1]/div[2]/div/div/div/div[2]/div[1]/div[1]/div/div[1]/div/p')
    if offline == True:
        return False
    elif offline == False:
        return True

RETURN = 0
LAST_PERCENT = 0

def get_percent():
    global LAST_PERCENT
    global RETURN
    try:
        percent = driver.find_element_by_xpath("/html/body/div[5]/div/div/div/div/div/div/div/div/div/div/div/div[3]/div/div/div[1]/div[9]/a/div/div[2]/p[2]")
        percent = percent.text
        percent = percent[:4]
        percent = percent.replace('%', '')
        percent = percent.replace(' ', '')
        percent = int(percent)
    except:
        percent = 1
        button = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/nav/div/div[3]/div[6]/div/div/div/div/button')
        button.click()
        button.click()
    if LAST_PERCENT == percent:
        RETURN += 1
    else:
        RETURN = 0
    LAST_PERCENT = percent
    if RETURN == 11:
        percent = 100
        RETURN = 0
    return percent

Streamers = [
    'https://www.twitch.tv/juansguarnizo',
    'https://www.twitch.tv/Mizkif',
    'https://www.twitch.tv/IlloJuan',
    'https://www.twitch.tv/moistcr1tikal',
    'https://www.twitch.tv/sodapoppin',
    'https://www.twitch.tv/Alexby11',
    'https://www.twitch.tv/Rubius',
    'https://www.twitch.tv/aroyitt'
]

try:
    with open('streamers.txt', "r") as override_config:
        Streamers = []
        for line in override_config:
            line = line.replace('\n', '')
            Streamers.append(line)
            print(line)
        override_config.close()
    print(f"Config overrided by streamers.txt!")
    for streamer_url in Streamers:
            print(streamer_url)
except:
    pass

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36")
driver = webdriver.Chrome(file, chrome_options=chrome_options)

driver.get('https://www.twitch.tv/login')
driver.implicitly_wait(5)

wait_auth()



while(True):
    for element in Streamers:
        driver.get(element)
        online = check_online()
        if online:
            print(f"{element} is online")
            mature = check_exists_by_xpath('//*[@id="root"]/div/div[2]/div/main/div[2]/div[3]/div/div/div[3]/div/div[2]/div/div/div/div[5]/div/div[3]/button')
            if (mature):
                button = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/main/div[2]/div[3]/div/div/div[3]/div/div[2]/div/div/div/div[5]/div/div[3]/button')
                button.click()
            button = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/nav/div/div[3]/div[6]/div/div/div/div/button')
            button.click()
            if check_exists_by_xpath("//*[contains(text(), 'Drops Enabled')]"):
                pass
            else:
                continue
            while(True):
                percent = get_percent()
                print(percent)
                if percent < 99:
                    sleep(72)
                if (percent) >= 99:
                    sleep(130)
                    break
        elif online == False:
            print(f"{element} is offline")
