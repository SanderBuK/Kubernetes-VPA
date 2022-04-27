import os
import sys
import subprocess
import time
import ruamel.yaml
import matplotlib.pyplot as plt

yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True

def get_pod_yaml(name: str, file = None):
    return subprocess.run(
        ["kubectl", "get", "pod", name, "--output", "yaml"],
        stdout=(subprocess.PIPE if file is None else file)
    ).stdout


def get_pod_resources(name: str):
    resources = subprocess.run(
        ["grep", "limits:", "-A", "5"],
        input=get_pod_yaml(name),
        stdout=subprocess.PIPE,
    )
    resources_obj = resources.stdout.decode("utf-8").split()
    return {
        "limits": {
            "cpu": int(resources_obj[2].replace("m", "")),
            "memory": int(resources_obj[4].replace("\"", ""))
        },
        "requests": {
            "cpu": int(resources_obj[7].replace("m", "")),
            "memory": int(resources_obj[9].replace("\"", ""))
        }
    }


def get_pod_usage(name: str):
    usage_output = subprocess.run(
        ["kubectl", "top", "pod", name, "--use-protocol-buffers"],
        stdout=subprocess.PIPE
    ).stdout

    usage = subprocess.run(
        ["grep", name],
        input=usage_output,
        stdout=subprocess.PIPE,
    )
    usage_obj = usage.stdout.decode("utf-8").split()
    return {
        "cpu": int(usage_obj[1].replace("m", "")),
        "memory": int(usage_obj[2].replace("\"", "")[:-2]) * 1048576
    }


def get_vpa_recommendations(name: str):
    usage_output = subprocess.run(
        ["kubectl", "get", "vpa", "vpa", "--output", "yaml"],
        stdout=subprocess.PIPE
    ).stdout
    data = yaml.load(usage_output.decode("utf-8"))

    recommendation = data["status"]["recommendation"]["containerRecommendations"][0]
    upperBound = recommendation["upperBound"]
    return {
        "upperBound": {
            "cpu": upperBound["cpu"][:-1]
        }
    }


name = sys.argv[1]
vpa_type = sys.argv[2]
resources = get_pod_resources(name)
usages = []
limits = []
requests = []
vpa_recommendation = []
time_list = []
current_time = 0

get_vpa_recommendations(name)

start = time.time()

while (time.time() - start) < 180:
    if vpa_type == "kube":
        recommendation = get_vpa_recommendations(name)
        vpa_recommendation.append(recommendation["upperBound"]["cpu"])
    time_list.append(current_time)
    requests.append(resources["requests"]["cpu"])
    limits.append(resources["limits"]["cpu"])
    usage = get_pod_usage(name)
    usages.append(usage["cpu"])
    time.sleep(5)
    current_time += 5

plt.plot(time_list, limits, label = "Limits")
plt.plot(time_list, requests, label = "Requests")
if vpa_type == "kube":
    plt.plot(time_list, vpa_recommendation, label = "Recommendation")
plt.plot(time_list, usages, label = "Usage")
plt.xlabel("Time (s)")
plt.ylabel("CPU (m)")
plt.title("Pod - Usage, limits and requests")
plt.legend()
plt.show()
