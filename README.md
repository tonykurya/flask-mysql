# Deploying a Flask API and MySQL server on Kubernetes

This repo contains code that 
1) Deploys a MySQL server on a Kubernetes cluster
2) Deploys a Flask API to add, delete and modify users in the MySQL database

## Prerequisites
1. Have `Docker` and the `Kubernetes CLI` (`kubectl`) installed together with `Minikube` (https://kubernetes.io/docs/tasks/tools/)

## Getting started
1. Clone the repository
2. Configure `Docker` to use the `Docker daemon` in your kubernetes cluster via your terminal: `eval $(minikube docker-env)`
3. Build a kubernetes-api image with the Dockerfile in this repo: `Docker build . -t flask-api`
4. Install the Atlas Kubernetes Operator: `helm install atlas-operator oci://ghcr.io/ariga/charts/atlas-operator`

## Deployments
Apply the deployments for the `MySQL` database and `Flask API`: 

`kubectl apply -k kustomize`

You can check the status of the pods, services and deployments.

`kubectl -n default get deployments,services`

## Check that the database and schemas are set
 
`kubectl exec -it $(kubectl get pods -l app=mysql -o jsonpath='{.items[0].metadata.name}') -- mysql -uroot -ppass -e "describe mydb.users"`

Result:

+-----------+--------------+------+-----+---------+----------------+
| Field     | Type         | Null | Key | Default | Extra          |
+-----------+--------------+------+-----+---------+----------------+
| id        | int          | NO   | PRI | NULL    | auto_increment |
| name      | varchar(255) | NO   |     | NULL    |                |
| email     | varchar(255) | NO   | UNI | NULL    |                |
| short_bio | varchar(255) | NO   |     | NULL    |                |
+-----------+--------------+------+-----+---------+----------------+
    
## Expose the API
The API can be accessed by exposing it using minikube: `minikube service flask-service`. This will return a `URL`. If you paste this to your browser you will see the `Flask API` message. You can use this `service_URL` to make requests to the `API`

## Start making requests
Now you can use the `API` to `CRUD` your database
1. add a user: `curl -H "Content-Type: application/json" -d '{"name": "<user_name>", "email": "<user_email>", "pwd": "<user_password>"}' <service_URL>/create`
2. get all users: `curl <service_URL>/users`
3. get information of a specific user: `curl <service_URL>/user/<user_id>`
4. delete a user by user_id: `curl -H "Content-Type: application/json" <service_URL>/delete/<user_id>`
5. update a user's information: `curl -H "Content-Type: application/json" -d {"name": "<user_name>", "email": "<user_email>", "pwd": "<user_password>", "user_id": <user_id>} <service_URL>/update`
