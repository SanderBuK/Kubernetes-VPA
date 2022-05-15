# Kubernetes-VPA

## Prerequisites
### Getting started
You'll need a Google Cloud account. With the account, create a new Project, with the Kubernetes Engine API enabled.

Having `gcloud` ensure that it points to your account and the correct project.

### Command-line Interfaces
You'll need to have installed the following programs, for the scripts to work:
- `kubectl` ([Kubernetes CLI](https://kubernetes.io/docs/tasks/tools/))
- `gcloud` ([Google Cloud CLI](https://cloud.google.com/sdk/docs/install-sdk))
- `helm` ([Kubernetes package manager](https://helm.sh/docs/intro/install/))

### Programs
You'll need to have installed the following programs, for the scripts to work:
- `python3` which needs a functioning `pip` installation

### Running the Selenium scripts
In order to run the Selenium script, you will need a webdriver installed. We use the Chrome webdriver, which can be found here: https://chromedriver.chromium.org/downloads

NB: The Selenium script creates a notebook called "Untitled" and will not start inputting the code in the kernel before the page has loaded. However if you run the script again the next notebook will be called "Untitled1" which does not match what the script is searching for. Therefore you have to delete the old "Untitled" notebook before running the same test again

## Run the experiment
Running the experiment is done by running the `setup-experiment.sh` script. Answer the three prompts, and the experiment will begin.

You can terminate the experiment anytime, by inputting `Ctrl + C`. After stopping, a graph is displayed showing the results. The graph, along with a `.csv` file, is saved under the folder `results/`.
