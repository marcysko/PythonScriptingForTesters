from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time

driver = webdriver.Chrome()

url = 'http://automationpractice.com/index.php?id_category=3&controller=category'
driver.get(url)
