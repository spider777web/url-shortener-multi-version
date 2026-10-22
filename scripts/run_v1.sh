apiVersion: apps/v1
kind: Deployment
metadata:
  name: url-shortener-v3
spec:
  replicas: 1
  selector:
    matchLabels:
      app: url-shortener-v3
  template:
    metadata:
      labels:
        app: url-shortener-v3
    spec:
      containers:
        - name: url-shortener-v3
          image: spider777web/url-shortener:v3
          ports:
            - containerPort: 5000
---
apiVersion: v1
kind: Service
metadata:
  name: url-shortener-v3
spec:
  type: NodePort
  selector:
    app: url-shortener-v3
  ports:
    - protocol: TCP
      port: 5000
      targetPort: 5000
      nodePort: 30083
