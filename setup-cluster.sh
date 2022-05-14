#create cluster
gcloud container clusters create \
  --machine-type n1-standard-2 \
  --num-nodes 1 \
  --zone $2 \
  --cluster-version latest \
  $1

#set admin privileges
kubectl create clusterrolebinding cluster-admin-binding \
  --clusterrole=cluster-admin \
  --user=$GOOGLE_ACCOUNT_EMAIL
