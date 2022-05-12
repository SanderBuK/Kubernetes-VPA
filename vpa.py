import os
import sys
import subprocess
import time
import ruamel.yaml

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


def kill_pod(name: str):
    subprocess.run(
        ["kubectl", "delete", "pod", name],
    )


def recreate_pod(name: str):
    data = yaml.load(get_pod_yaml(name))

    specs = data["spec"]["containers"][0]
    for env in specs["env"]:
        if env["name"] == "CPU_GUARANTEE" or env["name"] == "CPU_LIMIT":
            env["value"] = str(float(env["value"]) * 2)
    for resource in specs["resources"]:
        res = specs["resources"][resource]
        res["cpu"] = str(int(res["cpu"][:-1]) * 2) + "m"

    with open("pod-scaled.yaml", "w") as file:
        yaml.dump(data, file)
        file.close()

    kill_pod(name)

    subprocess.run(
        ["kubectl", "apply", "-f", "pod-scaled.yaml"],
    )
    os.remove("pod-scaled.yaml")

def vpa(name, resources, threshold=.85, freq=15):
    no_scaling = True
    while no_scaling:
        usage = get_pod_usage(name)
        print("Usage:\t\t" + str(usage))
        print("Resources:\t" + str(resources))
        if usage["cpu"] > resources["limits"]["cpu"] * threshold:
            print("CPU usage is too high, commence scaling")
            recreate_pod(name)
            no_scaling = False
        elif usage["memory"] > resources["limits"]["memory"]:
            print("Memory usage is too high, commence scaling")
            no_scaling = False
        else:
            print("Usage is below threshold")
        print()
        time.sleep(freq)

name = sys.argv[1]
resources = get_pod_resources(name)
vpa(name, resources)