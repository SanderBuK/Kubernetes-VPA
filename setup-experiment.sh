#!/bin/bash
read -p "Setup Cluster and JupyterHub (Y/n): " setup
setup=${setup:-Y}

read -p "Input VPA type (homemade/kube) [homemade]: " vpatype
vpatype=${vpatype:-homemade}

read -p "Input workload type (bursty/ramping/constant) [bursty]: " workloadtype
workloadtype=${workloadtype:-bursty}

if [[ $workloadtype == "bursty" ]]
then
        clustername="burstycluster"
elif [[ $workloadtype == "ramping" ]]
then
        clustername="rampingcluster"
elif [[ $workloadtype == "constant" ]]
then
        clustername="constantcluster"
fi

if [[ $setup == "Y" ]]
then
    pip install -r requirements.txt

    read -p "Input zone (Available zones: https://cloud.google.com/compute/docs/regions-zones/#available) [europe-west-3-a]: " zone
    zone=${zone:-europe-west3-a}

    ./setup-cluster.sh $clustername $zone
    ./setup-jupyterhub.sh
    sleep 10
fi

if [[ $vpatype == "kube" ]]
then
    if [ ! -d "/autoscaler" ] 
    then
        git clone https://github.com/kubernetes/autoscaler.git
    fi
    ./autoscaler/vertical-pod-autoscaler/hack/vpa-down.sh
    ./autoscaler/vertical-pod-autoscaler/hack/vpa-up.sh
    python3 ./setup-kube-vpa.py $workloadtype & python3 collect-vpa-data.py placeholder kube
elif [[ $vpatype == "homemade" ]]
then
    IN=$(kubectl get service --namespace default | tail -1)
    arrIN=($IN)
    while [[ ${arrIN[3]} == "<pending>" ]]
    do 
        IN=$(kubectl get service --namespace default | tail -1)
        arrIN=($IN)
        echo ${arrIN[3]}
        sleep 2
    done
    echo ${arrIN[3]} Url ready
    sleep 2
    python3 ./selenium-script.py ${arrIN[3]} $workloadtype
    jupyteruser=jupyter-$workloadtype
    sleep 2
    python3 ./vpa.py $jupyteruser & python3 collect-vpa-data.py $jupyteruser homemade
fi
