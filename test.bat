docker build --tag kennethreitz/bruce-operator .
docker push kennethreitz/bruce-operator
kubectl delete -f .\deploy\operator.yml -n bruce
kubectl create -f .\deploy\operator.yml -n bruce --validate=false
