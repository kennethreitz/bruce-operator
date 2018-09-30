docker build --tag kennethreitz/bruce-operator .
docker push kennethreitz/bruce-operator
kubectl delete -f .\deploy\operator.yml
kubectl create -f .\deploy\operator.yml --validate=false -n bruce
