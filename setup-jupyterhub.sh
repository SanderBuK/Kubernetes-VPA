# Requirements: Google Cloud account with project that has Kubernetes Engine API enabled
helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
helm repo update

#install jupyterhub
helm upgrade --cleanup-on-fail --install release jupyterhub/jupyterhub   --namespace default   --create-namespace   --version=1   --values config.yaml

kubectl config set-context $(kubectl config current-context) --namespace default

#external ip for accessing JupyterHub
kubectl get service --namespace default