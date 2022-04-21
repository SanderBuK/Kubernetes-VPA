from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import sys

# Set up the driver and go to the jupyterhub page
url = sys.argv[1]
driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(10)
driver.get(url)

# Create a new user
usrname = driver.find_element(By.NAME, 'username')  
usrname.send_keys('admin' + Keys.RETURN) 

# Wait for the url to change to url/user/admin/tree?
wait = WebDriverWait(driver, 100)
wait.until(lambda browser: browser.current_url == f'{url}/user/admin/tree?')

#wait until upload button is clickable
#WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "new-buttons")))



# Click the new button and create a new notebook
upload_btn = driver.find_element(By.ID, 'new-buttons')
upload_btn.click()
driver.find_element(By.ID, 'kernel-python3').click()

# Switch to the new notebook
driver.switch_to.window(driver.window_handles[1])
wait = WebDriverWait(driver, 100)
wait.until(lambda browser: browser.current_url == f'{url}/user/admin/notebooks/Untitled.ipynb?kernel_name=python3')

# Wait until the kernel is ready
wait.until(lambda browser: browser.find_element(By.ID, 'notification_notebook').is_displayed() == False)

# Enter and run the bursty code
actions = ActionChains(driver)
actions.send_keys('import time\n# Run for 5 minutes\nstart = time.time()\nwhile (time.time() - start) < 300:\n    for i in range(30000):\n        print(i)\ntime.sleep(20)')
actions.key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).perform()
actions.perform()
