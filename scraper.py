from selenium import webdriver
from time import sleep

chrome = webdriver.Chrome()

chrome.get('https://www.brainscape.com/l/dashboard/mc-dermato-amp-oftalmo-etc-12545034/decks')

chrome.maximize_window()

chrome.find_element_by_class_name('login-link').click()

chrome.find_element_by_id('email').send_keys('thiago76ers@gmail.com')

chrome.find_element_by_id('password').send_keys('senha')

chrome.find_element_by_xpath("//span[contains(@class, 'label') and text() = 'Log In']").click()

sleep(2)

chrome.find_element_by_xpath("//div[@title='MC - Dermato & Oftalmo etc.']").click()

sleep(2)

parent_element_glasses = chrome.find_element_by_id("6688020")

parent_element_glasses.find_element_by_class_name('ion-ios-glasses-outline').click()

sleep(2)

parent_element_cards = chrome.find_element_by_class_name('dashboard-preview-card-table')

parent_element_cards.find_elements_by_tag_name('section')
