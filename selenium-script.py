from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import sys

# Set up the driver and go to the jupyterhub page
url = f'http://{sys.argv[1]}'
loadname = sys.argv[2]
driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(10)
driver.get(url)

# Create a new user
usrname = driver.find_element(By.NAME, 'username')
usrname.send_keys(loadname + Keys.RETURN)

# Wait for the url to change to url/user/admin/tree?
wait = WebDriverWait(driver, 100)
wait.until(lambda browser: browser.current_url == f'{url}/user/{loadname}/tree?')


# Click the new button and create a new notebook
upload_btn = driver.find_element(By.ID, 'new-buttons')
upload_btn.click()
driver.find_element(By.ID, 'kernel-python3').click()

# Switch to the new notebook
driver.switch_to.window(driver.window_handles[1])
wait = WebDriverWait(driver, 100)
wait.until(lambda browser: browser.current_url == f'{url}/user/{loadname}/notebooks/Untitled.ipynb?kernel_name=python3')

# Wait until the kernel is ready
wait.until(lambda browser: browser.find_element(By.ID, 'notification_notebook').is_displayed() == False)

# Enter and run the code
actions = ActionChains(driver)
actions.send_keys(open(f'workloads/{loadname}.py').read())
actions.send_keys(Keys.END + Keys.HOME)
if loadname == 'bursty':
    actions.send_keys((Keys.BACKSPACE*5) + Keys.UP + (Keys.HOME*2) + (Keys.BACKSPACE*3) + Keys.UP + Keys.BACKSPACE)
elif loadname == 'ramping':
    actions.send_keys((Keys.BACKSPACE*4) + Keys.UP + (Keys.RIGHT*4) + (Keys.BACKSPACE*2) + Keys.UP + Keys.BACKSPACE)
elif loadname == 'constant':
    actions.send_keys(Keys.BACKSPACE)
actions.key_down(Keys.CONTROL).key_down("s").key_up(Keys.CONTROL).key_up("s").perform()
actions.perform()
actions.key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).perform()
actions.perform()
