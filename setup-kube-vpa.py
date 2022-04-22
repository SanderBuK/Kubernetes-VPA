import os
import sys
import subprocess
import ruamel.yaml

name = sys.argv[1]

with open("jh-deployment.yaml") as f:
    newText=f.read().replace('jupyter-name', name)

with open("jh-deployment-tmp.yaml", "w") as f:
    f.write(newText)

subprocess.run(
    ["kubectl", "create", "-f", "jh-deployment-tmp.yaml"],
).stdout

os.remove("jh-deployment-tmp.yaml")

subprocess.run(
    ["kubectl", "create", "-f", "kube-vpa.yaml"],
).stdout
