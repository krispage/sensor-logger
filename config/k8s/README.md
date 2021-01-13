## Configuring kubernetes deployment
* Replace certs/tls.key and certs/tls.crt with valid SSL certificate
* Edit sl-config.yaml config map to match your database setup
* Change the host to match your domain sl-ing.yaml

Apply Kustomization using kubectl
```bash
kubectl apply -k .
```

