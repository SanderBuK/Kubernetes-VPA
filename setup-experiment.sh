#!/bin/bash
read -p "Input workload type (bursty/ramping/constant) [bursty]: " workloadtype
workloadtype=${workloadtype:-bursty}

read -p "Input zone (Available zones: https://cloud.google.com/compute/docs/regions-zones/#available) [europe-west-3-a]: " zone
zone=${zone:-europe-west3-a}

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


./setup-cluster.sh $clustername $zone
./setup-jupyterhub.sh
sleep 10
IN=$(kubectl get service --namespace default | tail -1)
arrIN=($IN)
python3 ./selenium-script.py ${arrIN[3]} $workloadtype
jupyteruser=jupyter-$workloadtype
./vpa.py $jupyteruser
