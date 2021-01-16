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

Streamers = [
    'https://www.twitch.tv/auronplay',
    'https://www.twitch.tv/juansguarnizo',
    'https://www.twitch.tv/Mizkif',
    'https://www.twitch.tv/IlloJuan',
    'https://www.twitch.tv/moistcr1tikal',
    'https://www.twitch.tv/sodapoppin',
    'https://www.twitch.tv/Alexby11',
    'https://www.twitch.tv/Rubius',
    'https://www.twitch.tv/aroyitt'
]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36")
driver = webdriver.Chrome(file, chrome_options=chrome_options)

driver.get('https://www.twitch.tv/login')
driver.implicitly_wait(15)

wait_auth()

while(True):
    for element in Streamers:
        driver.get(element)
        online = check_online()
        if online:
            print(f"{element} is online")
            mature = check_exists_by_xpath('//*[@id="root"]/div/div[2]/div/main/div[2]/div[3]/div/div/div[3]/div/div[2]/div/div/div/div[5]/div/div[3]/button')
            if (mature):
                button = driver.find_element_by_xpath(xpath)
                button.click()
        elif online == False:
            print(f"{element} is offline")
