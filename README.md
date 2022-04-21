# Kubernetes-VPA

## Running the Selenium scripts
Before you can run the Selenium scripts you need to have Selenium installed.
We used pip to run the command:

`pip install -U selenium`

Depending on what browser you prefer you have to download a webdriver from one of the following:
| Browser | Link |
| --- | --- |
| Chrome: | https://chromedriver.chromium.org/downloads  |
| Edge: | https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/ |
|Firefox: | https://github.com/mozilla/geckodriver/releases | 
| Safari: | https://webkit.org/blog/6900/webdriver-support-in-safari-10/ | 

After following the guide and installing the webdriver while also having it in the correct folder the scripts can be run using python3 by writing 

`python3 selenium_script.py YourJupyterHubUrl [workloadtype]`

The script will create a new user and open a create a notebook where it will run some python code depending on which workload you chose either bursty or ramping
