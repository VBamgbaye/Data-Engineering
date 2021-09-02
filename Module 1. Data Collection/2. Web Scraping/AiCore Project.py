from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

options = Options()
options.add_argument("start-maximized")
options.add_argument("--no-sandbox")
options.add_argument("--disable-setuid-sandbox")
driver = webdriver.Chrome(executable_path=r'C:\Users\vbamgbay\Downloads\chromedriver.exe', options=options)
URL = "https://www.youtube.com/c/aljazeeraenglish/videos"
driver.get(URL)

time.sleep(2)

# Consent
consent_div = driver.find_element_by_xpath(
    '//button[@class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc IIdkle"]')
consent_span = consent_div.find_element_by_xpath('.//span')
consent_span.click()

time.sleep(3)

settings = driver.find_element_by_xpath('//div[@class="VP4fnf"]')
settings_list = driver.find_elements_by_xpath('//button')

for button in settings_list:
    if button.text == "On":
        button.click()

time.sleep(3)

cookies_div = driver.find_element_by_xpath(
    '//button[@class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc tVK8Qc"]')
cookies_span = cookies_div.find_element_by_xpath('.//span')
cookies_span.click()

time.sleep(3)

# def pgscroll(z):
#   """
#  Function to scroll down the page
# """
a = 0
for x in range(a):
    html = driver.find_element_by_tag_name('html')
    time.sleep(3)
    html.send_keys(Keys.PAGE_DOWN)

time.sleep(3)

videos = driver.find_element_by_xpath('//div[@id="items"]')
vid_list = videos.find_elements_by_xpath("//ytd-grid-video-renderer")
# vid_list = wait(driver, 30).until(EC.presence_of_all_elements_located(
# (By.XPATH, "//ytd-grid-video-renderer[@class='style-scope ytd-grid-renderer']")))
num_vids = len(vid_list)
print("No of videos is:", num_vids)

yt_data = []
count = 0

time.sleep(3)

for i in range(num_vids):
    data = {"title": [], "description": [], "hash_tags": [], "views": [], "comments": []}
    try:

        wait(driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//ytd-grid-renderer[@class='style-scope ytd-item-section-renderer']")))
    except:
        driver.forward()

        a = 0
        for x in range(a):
            html = driver.find_element_by_tag_name('html')
            time.sleep(3)
            html.send_keys(Keys.PAGE_DOWN)

    videos = driver.find_element_by_xpath('//div[@id="items"]')
    vids = wait(driver, 30).until(EC.presence_of_all_elements_located(
        (By.XPATH, "//ytd-grid-video-renderer[@class='style-scope ytd-grid-renderer']")))
    # headline = videos.find_elements_by_xpath('.//ytd-grid-video-renderer')[i]
    headlines = vids[i]
    time.sleep(3)
    print(len(vids))
    ActionChains(driver).move_to_element(headlines).click().perform()
    print("iteration:", i)

    time.sleep(2)

    # Title of Video
    try:
        title = driver.find_element_by_xpath(
            '//yt-formatted-string[@class="style-scope ytd-video-primary-info-renderer"]').text
        data['title'].append(title)
        # print(title)
    except NoSuchElementException:
        data['title'].append(None)
        # print(None)

    time.sleep(3)

    # Video Description
    try:
        desc = driver.find_element_by_xpath(
            '//yt-formatted-string[@class="content style-scope ytd-video-secondary-info-renderer"]')
        descriptions = desc.find_elements_by_xpath('.//span')
        for description in descriptions:
            if description.text:
                data['description'].append(description.text)
                # print(description.text)
    except NoSuchElementException:
        data['description'].append(None)
        # print(None)

    time.sleep(2)

    # Video_tags
    try:
        v_tag = driver.find_element_by_xpath(
            '//yt-formatted-string[@class="super-title style-scope ytd-video-primary-info-renderer"]')
        tags = v_tag.find_elements_by_xpath('.//a')
        for tag in tags:
            if tag.text:
                data['hash_tags'].append(tag.text)
                # print("hash_tags:", tag.text)
    except NoSuchElementException:
        data['hash_tags'].append(None)
        # print(None)
    time.sleep(2)

    # Number of views
    try:
        views = driver.find_element_by_xpath(
            '//span[@class="view-count style-scope ytd-video-view-count-renderer"]').text
        # print(views)
        data['views'].append(views)
    except NoSuchElementException:
        # print(None)
        data['views'].append(None)
    time.sleep(2)

    # Comments
    try:
        div_tag = driver.find_element_by_xpath('//div[@class="style-scope ytd-expander"]')
        yt_tag = div_tag.find_elements_by_xpath('.//yt-formatted-string')
        for comment in yt_tag:
            if comment.text:
                data['comments'].append(comment.text)
                #print(div_tag.text)
    except NoSuchElementException:
        data['comments'].append(None)

    time.sleep(2)

    print(data)
    yt_data.append(data)
    count += 1
    driver.back()

df = pd.DataFrame.from_dict(yt_data, orient='columns')
df.to_json(r'C:\Users\vbamgbay\Documents\git\Data-Engineering\Web_Scraping_Project\youtube_data.json', orient='records')

