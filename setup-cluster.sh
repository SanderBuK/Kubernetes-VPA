#create cluster
gcloud container clusters create \
  --machine-type n1-standard-2 \
  --num-nodes 2 \
  --zone europe-west3-a \
  --cluster-version latest \
  maincluster

#set admin privileges
kubectl create clusterrolebinding cluster-admin-binding \
  --clusterrole=cluster-admin \
  --user=$GOOGLE_ACCOUNT_EMAIL