from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

def load_and_accept_cookies():
        driver = webdriver.Chrome()
        URL = "https://www.zoopla.co.uk/new-homes/property/london/?q=London&results_sort=newest_listings&search_source=new-homes&page_size=25&pn=1&view_type=list"
        driver.get(URL)
        accept_cookies = driver.find_elements_by_xpath('//button[@data-responsibility="acceptAll"]')
        for button in accept_cookies:
            if button.text == "Accept all cookies":
                relevant_button = button
                relevant_button.click()
        return driver
    
def get_properties(num_to_get=2):

    driver = load_and_accept_cookies()
    
    data = {"sale_price": [], "num_bedrooms": [], "sqft": [], "description": [], "address": []}    
    prop_container = driver.find_element_by_xpath('//*[@id="__next"]/div[5]/div[2]/main/div[2]/div[2]')
    properties = prop_container.find_elements_by_xpath('./div')
    num_props = len(properties)
    
    time.sleep(3)
    
    for i in range(num_props):
        prop_container = driver.find_element_by_xpath('//*[@id="__next"]/div[5]/div[2]/main/div[2]/div[2]')
        house = prop_container.find_elements_by_xpath('./div')[i]
        house.click()
        
        time.sleep(3)
        

        try:
            ## Find the price and append it to the dictionary
            price_elem = driver.find_elements_by_xpath('//*[@id="main-content"]/div[1]/div[1]/section[1]/div[1]/div[2]/span')
            data["sale_price"].append(price_elem.text)
        except:
            data["sale_price"].append(None)
        
        time.sleep(3)
        
        ## Find a link to click on
        house_page = driver.find_elements_by_xpath('//*[@id="__next"]/div[5]/div[2]/main/div[2]/div[3]/ul/li[2]/a')
        
        time.sleep(3)
        
        ## Find the number of bedrooms and append it to the dictionary
        ## HINT: https://lmgtfy.com/?q=xpath+svg+tag
        ## HINT: https://stackoverflow.com/questions/11657223/xpath-get-following-sibling
        try:
            bedrooms_elem = driver.find_element_by_xpath('//*[@id="main-content"]/div[1]/div[1]/section[1]/div[2]/div/div[1]/span')
            num_beds = bedrooms_elem.text[:-4] # " bedrooms" is 9 chars
        except:
            data["num_bedrooms"].append(num_beds)

        time.sleep(3)
            
        try:
            ## Find the number of square footage and append it to the dictionary
            sqft_elem = driver.find_element_by_xpath('//*[@id="main-content"]/div[1]/div[1]/section[1]/div[2]/div/div[4]/span')
            data["sqft"].append(sqft_elem.text)
        except:
            data["sqft"].append("None")

        time.sleep(3)
            
        ## Find the description and append it to the dictionary
        try:
            description_elem = driver.find_element_by_xpath('//*[@id="main-content"]/div[1]/section[3]/div[2]/div/div[1]/div/span')
            data["description"].append(description_elem.text)
        except:
            data["description"].append("None")
            
        time.sleep(3)
            
        ## Find the address
        try:
            address_elem = driver.find_element_by_xpath('//*[@id="listing-summary-details-heading"]/span[2]')
            data["address"].append(address_elem.text)
        except:
            data["address"].append("None")

        driver.execute_script("window.history.go(-1)")

    return data

#properties = get_properties()
