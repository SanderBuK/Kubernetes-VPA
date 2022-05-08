import sys
import subprocess

subprocess.run(
    ["kubectl", "delete", "vpa", "vpa"],
).stdout

subprocess.run(
    ["kubectl", "delete", "deployment", "vpa-deployment"],
).stdout

subprocess.run(
    ["kubectl", "create", "-f", "vpa-deployment.yaml"],
).stdout

subprocess.run(
    ["kubectl", "create", "-f", "kube-vpa.yaml"],
).stdout
