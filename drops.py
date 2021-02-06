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

def delete_streamer(streamer):
    Streamers.remove(streamer)
    try:
        with open("streamers.txt", "r") as f:
            lines = f.readlines()
        with open("streamers.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != streamer:
                    f.write(line)
    except:
        pass


RETURN = 0
LAST_PERCENT = 0

def claim_reward(streamer):
    driver.get('https://www.twitch.tv/drops/inventory')
    if check_exists_by_xpath("//*[contains(text(), 'Claim Now')]") == False:
        return
    button = driver.find_element_by_xpath("//*[contains(text(), 'Claim Now')]")
    button.click()
    driver.get(streamer)
    return

    
    

def get_percent():
    global LAST_PERCENT
    global RETURN
    try:
        percent = driver.find_element_by_xpath("/html/body/div[5]/div/div/div/div/div/div/div/div/div/div/div/div[3]/div/div/div[1]/div[9]/a/div/div[2]/p[2]")
        percent = percent.text
        percent = percent[:3]
        try:
            percent = percent.replace('%', '')
            percent = percent.replace(' ', '')
        except:
            pass
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
    if RETURN == 5:
        percent = 100
    return percent

Streamers = []

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
    print("streamers.txt not found. Create streamers.txt and fill urls to watch")
    os._exit(0)

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
        if online == False:
            print(f"{element} is offline")
            continue

        print(f"{element} is online")
        if check_exists_by_xpath("//*[contains(text(), 'Drops Enabled')]") == False:
            print("Streaming but drops not enabled!")
            continue

        mature = check_exists_by_xpath('//*[@id="root"]/div/div[2]/div/main/div[2]/div[3]/div/div/div[3]/div/div[2]/div/div/div/div[5]/div/div[3]/button')
        if (mature):
            button = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/main/div[2]/div[3]/div/div/div[3]/div/div[2]/div/div/div/div[5]/div/div[3]/button')
            button.click()

        current_url = str(driver.current_url)
        if current_url.find('?referrer=raid') != -1:
            continue

        button = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/nav/div/div[3]/div[6]/div/div/div/div/button')
        button.click()
        while(True):
            percent = get_percent()
            print(percent)
            if percent < 99:
                sleep(72)
            if (percent) >= 99:
                sleep(130)
                if RETURN == 0:
                    delete_streamer(element)
                    claim_reward(element)
                RETURN = 0
                break
            
