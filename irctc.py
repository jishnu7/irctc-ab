from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep, strftime
import configparser
import json

# Config
config = configparser.ConfigParser()
config.read('config')

def login():
    driver.get('https://www.irctc.co.in/eticketing/loginHome.jsf')
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.NAME, 'j_username'))
        ).send_keys(config.get('account', 'username'))
    driver.find_element_by_name('j_password').send_keys(config.get('account', 'password'))
    driver.find_element_by_name('j_captcha').send_keys('')

def planjourney():
    clas = config.get('train', 'class')

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'jpform:fromStation'))
        ).send_keys(config.get('train', 'from'))
    driver.find_element_by_id('jpform:toStation').send_keys(config.get('train', 'to'))
    driver.find_element_by_id('jpform:journeyDateInputDate').send_keys(config.get('train', 'date'))
    driver.find_element_by_id('jpform:jpsubmit').click()

    WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.NAME, 'quota'))
        )[-1].click()
    driver.find_element_by_link_text(clas).click()

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'Book Now'))
        ).click()

def filldetails():
    names = json.loads(config.get('passenger', 'name'))
    ages = json.loads(config.get('passenger', 'age'))
    genders = json.loads(config.get('passenger', 'gender'))
    berths = json.loads(config.get('passenger', 'berth'))
    mobile = str(config.get('passenger', 'mobile'))

    WebDriverWait(driver, 60).until(EC.title_contains('Book Ticket'))
    for name, el in zip(names, driver.find_elements_by_class_name('psgn-name')):
        el.send_keys(name)
    for age, el in zip(ages, driver.find_elements_by_class_name('psgn-age')):
        el.send_keys(age)
    for gender, el in zip(genders, driver.find_elements_by_class_name('psgn-gender')):
        Select(el).select_by_value(gender)
    for berth, el in zip(berths, driver.find_elements_by_class_name('psgn-berth-choice')):
        Select(el).select_by_value(berth)

    driver.find_element_by_id('addPassengerForm:mobileNo').clear()
    driver.find_element_by_id('addPassengerForm:mobileNo').send_keys(mobile)
    driver.find_element_by_id('addPassengerForm:autoUpgrade').click()

def sbi():
    WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.ID, 'PREFERRED'))
        )[-1].click()
    driver.find_element_by_id('validate').click()

    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.ID, 'username'))
        ).send_keys(config.get('sbi', 'username'))
    driver.find_element_by_id('label2').send_keys(config.get('sbi', 'password'))
    driver.find_element_by_id('Button2').click()

if __name__ == '__main__':
    driver = webdriver.Chrome()
    login()
    planjourney()
    filldetails()
    sbi()
