import sys
import subprocess
import os

workload = sys.argv[1]

subprocess.run(
    ["kubectl", "delete", "vpa", "vpa"],
).stdout

subprocess.run(
    ["kubectl", "delete", "deployment", "vpa-deployment"],
).stdout

with open("vpa-deployment.yaml") as f:
    newText=f.read().replace('WORKLOAD_NAME', workload)

with open("vpa-deployment-tmp.yaml", "w") as f:
    f.write(newText)

subprocess.run(
    ["kubectl", "create", "-f", "vpa-deployment-tmp.yaml"],
).stdout

subprocess.run(
    ["kubectl", "create", "-f", "kube-vpa.yaml"],
).stdout

os.remove("vpa-deployment-tmp.yaml")
