apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app
spec:
  selector:
    matchLabels:
      app: flask-app
  replicas: 1
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
        - name: flask-app
          image: your-flask-app-image
          env:
            - name: DB_URL
              valueFrom:
                secretKeyRef:
                  name: mysql-credentials
                  key: url
          ports:
            - containerPort: 5000
              name: flask-app
---
apiVersion: v1
kind: Service
metadata:
  name: flask-app
spec:
  selector:
    app: flask-app
  ports:
    - name: flask-app
      port: 5000
      targetPort: flask-app
  type: ClusterIP
