
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os


from bs4 import BeautifulSoup, Comment

def followerScraper():
    dont_follow_back = []
    follower_Usernames = {}
    following_Usernames = []

    #the user's username
    received_userName = input('What is your instagram username? ')

    # 1. Get the absolute path to the directory where this script (scraper.py) is located.
    #    '__file__' is a special variable that holds the path to the current file.
    #    os.path.dirname() gets the directory part of that path.
    script_dir = os.path.dirname(os.path.abspath(__file__))

    parent_dir = os.path.dirname(script_dir)

    # 2. Use os.path.join() to build the full, OS-independent path to chromedriver.exe.
    #    This will correctly use backslashes (\) on Windows and forward slashes (/) on Mac/Linux.
    webdriver_path = os.path.join(parent_dir, 'chromedriver-win64', 'chromedriver.exe')

    print(f"The constructed path to the webdriver is:\n{webdriver_path}\n")

    service = Service(executable_path=webdriver_path)
    driver = webdriver.Chrome(service=service)
    driver.get('https://www.instagram.com/')

    input("Log in to Instagram in the opened browser. Then press Enter here to continue...")


    preURL = 'https://www.instagram.com/'
    profileURL = preURL + received_userName + '/'
    driver.get(profileURL)
    print("At profile page")
    time.sleep(3)

    # Click the followers link to open the popup
    try:
        followers_button = driver.find_element(By.PARTIAL_LINK_TEXT, "followers")
    except:
        followers_button = driver.find_element(By.XPATH, "//a[contains(@href, '/followers/')]")
    followers_button.click()
    print("Clicked followers link")
    

    time.sleep(2)
    scroll_box = driver.find_element(
    By.CSS_SELECTOR,
    "div.x6nl9eh.x1a5l9x9.x7vuprf.x1mg3h75.x1lliihq.x1iyjqo2.xs83m0k.xz65tgg.x1rife3k.x1n2onr6"
    )
    #This is the part where we actually scroll through the followers so all of our divs load
    last_height, curr_height = 0, 1
    while last_height != curr_height:
        last_height = curr_height
        time.sleep(0.5)
        curr_height = driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollHeight; return arguments[0].scrollHeight;",
            scroll_box
    )

    #Lets actually scrape the followers here
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    divOfFollowers = soup.find('div', {'class': 'x6nl9eh x1a5l9x9 x7vuprf x1mg3h75 x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6'})

    all_follower_divs = divOfFollowers.find_all('div', {'class': 'x1qnrgzn x1cek8b2 xb10e19 x19rwo8q x1lliihq x193iq5w xh8yej3'})

    #Adding all the followers into a hashmap/dictionary
    for div in all_follower_divs:
        span_with_name = div.find('span', {'class': '_ap3a _aaco _aacw _aacx _aad7 _aade'}).text.strip()
        follower_Usernames[span_with_name] = 'hi'


#Exit out of that first popup
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    time.sleep(2)



#Now We get the list of people that the user follows:
    try:
        following_button = driver.find_element(By.PARTIAL_LINK_TEXT, "following")
    except:
        following_button = driver.find_element(By.XPATH, "//a[contains(@href, '/following/')]")
    following_button.click()
    print("Clicked following link")
    time.sleep(2)

    scroll_box = driver.find_element(
    By.CSS_SELECTOR,
    "div.x6nl9eh.x1a5l9x9.x7vuprf.x1mg3h75.x1lliihq.x1iyjqo2.xs83m0k.xz65tgg.x1rife3k.x1n2onr6"
    )
     #This is the part where we actually scroll through the following so all of our divs load
    last_height, curr_height = 0, 1
    while last_height != curr_height:
        last_height = curr_height
        time.sleep(0.5)
        curr_height = driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollHeight; return arguments[0].scrollHeight;",
            scroll_box
    )
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    divOfFollowing = soup.find('div', {'class': 'x6nl9eh x1a5l9x9 x7vuprf x1mg3h75 x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6'})

    all_following_divs = soup.find_all('div', {'class': 'x1qnrgzn x1cek8b2 xb10e19 x19rwo8q x1lliihq x193iq5w xh8yej3'})
    for div in all_following_divs:
        span_with_name = div.find('span', {'class': '_ap3a _aaco _aacw _aacx _aad7 _aade'}).text.strip()
        following_Usernames.append(span_with_name)
    

    for user in following_Usernames:
        if user not in follower_Usernames:
            dont_follow_back.append(user)

    
    
    print("\nPeople you follow who DON'T follow you back:")
    for user in dont_follow_back:
        print(user)

    with open('not_following_back.txt', 'w', encoding='utf-8') as f:
        for user in dont_follow_back:
            f.write(user + '\n')

    driver.quit()

if __name__ == "__main__":
    followerScraper()




