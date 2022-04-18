#!/bin/bash

kubectl get vpa vpa --output yaml | grep recommendation: -A 14
echo ""
kubectl describe pod jupyter-vpa | grep Limits: -A 5
echo ""
echo "Current use"
kubectl top pod jupyter-vpa --use-protocol-buffers | grep NAME -A 1
