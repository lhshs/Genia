# Elyra Server

## 1. Create `namespace` resource
* creare namespace(ns)
    ```sh
    k create ns kubeflow
    ```

## 2. Deployment & PVC
* Apply `deployment` and `pvc` resource
    ```sh
    k apply -f elyra-deploy.yaml
    ```

## 3. Service
* Apply `service`
    ```sh
    k apply -f nodeport.yaml
    ```

* Check `service` status
    ```sh
    # k get svc
    k get services -n kubeflow
    ```

* Visit the website `localhost:8888`