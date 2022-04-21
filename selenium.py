from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = 'http://34.159.63.137/'
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(url)

usrname = driver.find_element(By.NAME, 'username')  # Find the username box
usrname.send_keys('admin' + Keys.RETURN) # Send the username

# wait for the url to change to url/user/admin/tree?
wait = WebDriverWait(driver, 10)
wait.until(lambda browser: browser.current_url == f'{url}user/admin/tree?')

#find element by xpath
driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div[1]/button').click()

#driver.find_element(By.ID, 'new-dropdown-button').click()
driver.get('https://www.google.com/')
#driver.find_element(By.ID, 'kernel-python3').click()


