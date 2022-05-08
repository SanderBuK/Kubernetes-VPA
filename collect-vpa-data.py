import os
import sys
import subprocess
import time
import ruamel.yaml
import matplotlib.pyplot as plt
import csv
import numpy

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
        },
        "requests": {
            "cpu": int(resources_obj[7].replace("m", "")),
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
    }


def get_kube_vpa_name():
    name_output = subprocess.run(
        ["kubectl", "get", "pods", "-l", "app=vpa-container"],
        stdout=subprocess.PIPE
    ).stdout

    name_output_split = subprocess.run(
        ["grep", "vpa-deployment"],
        input=name_output,
        stdout=subprocess.PIPE,
    )

    name_split = name_output_split.stdout.decode("utf-8").split()
    return name_split[0]


def get_vpa_recommendations(name: str):
    usage_output = subprocess.run(
        ["kubectl", "get", "vpa", "vpa", "--output", "yaml"],
        stdout=subprocess.PIPE
    ).stdout
    data = yaml.load(usage_output.decode("utf-8"))

    upper_cpu = 0
    lower_cpu = 0
    target_cpu = 0
    recommendation = data["status"]["recommendation"]["containerRecommendations"]
    for pod in recommendation:
        if pod["containerName"] == "vpa-container":
            upper_cpu = pod["upperBound"]["cpu"][:-1]
            lower_cpu = pod["lowerBound"]["cpu"][:-1]
            target_cpu = pod["target"]["cpu"][:-1]

    return {
        "upperBound": {
            "cpu": upper_cpu
        },
        "lowerBound": {
            "cpu": lower_cpu
        },
        "target": {
            "cpu": target_cpu
        },
    }


def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1

    return path


name = sys.argv[1]
vpa_type = sys.argv[2]
if vpa_type == "kube":
    name = get_kube_vpa_name()
usages = []
limits = []
requests = []
vpa_upper_bound = []
vpa_lower_bound = []
vpa_target = []
time_list = []
current_time = 0

start = time.time()

while True:
    try:
        if vpa_type == "kube":
            recommendation = get_vpa_recommendations(name)
            vpa_upper_bound.append(int(recommendation["upperBound"]["cpu"]))
            vpa_lower_bound.append(int(recommendation["lowerBound"]["cpu"]))
            vpa_target.append(int(recommendation["target"]["cpu"]))
        resources = get_pod_resources(name)
        usage = get_pod_usage(name)
        usages.append(usage["cpu"])
        time_list.append(current_time)
        requests.append(resources["requests"]["cpu"])
        limits.append(resources["limits"]["cpu"])
        time.sleep(5)
        current_time += 5
    except KeyboardInterrupt:
        print("Stopped Data collector")
        break
    except:
        while True:
            is_created = subprocess.run(
                ["kubectl", "get", "pod", name],
                stdout=subprocess.PIPE
            ).stdout.decode("utf-8")
            if "NotFound" not in is_created:
                break
            usages.append(0)
            vpa_upper_bound.append(0)
            vpa_lower_bound.append(0)
            vpa_target.append(0)
            time_list.append(current_time)
            requests.append(0)
            limits.append(0)
            time.sleep(5)
            current_time += 5

with open(uniquify(f"results/{name}{vpa_type}graph.csv"), "w") as f:
    writer = csv.writer(f)
    writer.writerows([
        limits, requests, usages, time_list, vpa_upper_bound, vpa_lower_bound, vpa_target
    ])

plt.plot(time_list, limits, label = "Limits")
plt.plot(time_list, requests, label = "Requests")
if vpa_type == "kube":
    plt.plot(time_list, vpa_lower_bound, label = "Lower Bound")
    plt.plot(time_list, vpa_target, label = "Target")
plt.plot(time_list, usages, label = "Usage")
plt.xlabel("Time (s)")
plt.ylabel("CPU (m)")
plt.title("Pod - Usage, limits and requests")
plt.legend()
plt.savefig(uniquify(f"results/{name}{vpa_type}graph.png"))

plt.show()
