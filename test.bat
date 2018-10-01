docker build --tag kennethreitz/bruce-operator .
docker push kennethreitz/bruce-operator
kubectl delete --all pods -n bruce
