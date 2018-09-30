docker build --tag bruceproject/operator .
docker push bruceproject/operator
kubectl delete -f .\deploy\operator.yml -n bruce
kubectl create -f .\deploy\operator.yml -n bruce
