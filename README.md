# Kubernetes-VPA

## Prerequisites
You'll need to have installed the following programs installed, for this to work:
- `kubectl` ([Kubernetes CLI](https://kubernetes.io/docs/tasks/tools/))
- `gcloud` ([Google Cloud CLI](https://cloud.google.com/sdk/docs/install-sdk))
- `helm` ([Kubernetes package manager](https://helm.sh/docs/intro/install/))

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

NB: Right now it creates a notebook called "untitled" and will not start inputting the code in the kernel before the page has loaded. However if you run the script again the next notebook will be called "untitled1" which does not match what the script is searching for. Therefore you have to delete the old "untitled" notebook before running the same test again
