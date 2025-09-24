# Guestbook Helm Chart

This Helm chart deploys a simple guestbook application consisting of:
- **Redis** (for storing guestbook entries)
- **Backend** (FastAPI service with Redis integration)
- **Frontend** (Nginx serving a simple UI that proxies to backend)

---

## Prerequisites

- AKS cluster provisioned via Terraform
- ACR with images pushed:
  - `guestbook-backend:v1`
  - `guestbook-frontend:v1`
- `helm` installed and connected to the cluster (`kubectl config current-context` must point to AKS)

---

## Installation

1. Push images to ACR (only needed once):

   ```sh
   az acr login --name acrpidevopstfweu01
   docker tag guestbook-backend:local acrpidevopstfweu01.azurecr.io/guestbook-backend:v1
   docker push acrpidevopstfweu01.azurecr.io/guestbook-backend:v1

   docker tag guestbook-frontend:local acrpidevopstfweu01.azurecr.io/guestbook-frontend:v1
   docker push acrpidevopstfweu01.azurecr.io/guestbook-frontend:v1

2. Deploy Helm chart:

   ```sh
   helm install guestbook ./helm/guestbook -n guestbook --create-namespace
   ```

3. Verify:

   ```sh
   kubectl get pods -n guestbook
   kubectl get svc -n guestbook
   ```

---

## Access the App

* The **frontend service** is of type `LoadBalancer`.

* Run:

  ```sh
  kubectl get svc guestbook-frontend -n guestbook
  ```

* Note the `EXTERNAL-IP` and `PORT` (default 8080).

* Open in browser:

  ```
  http://<EXTERNAL-IP>:8080
  ```

---

## Customization

Edit `values.yaml` to change:

* Replica count (`replicaCount`)
* Image names/tags (`images.backend`, `images.frontend`, `images.redis`)
* Service type (`ClusterIP`, `NodePort`, `LoadBalancer`)
* Service port (`service.port`)

Apply changes with:

```sh
helm upgrade guestbook ./helm/guestbook -n guestbook
```

---

## Uninstall

```sh
helm uninstall guestbook -n guestbook
kubectl delete namespace guestbook
```