# Dockerfile & Build

## 1. nginx container build
* build image
    ```sh
    docker build -t nginx-img .
    ```

* run nginx container
    ```sh
    docker run -d -p 8080:80 --name nginx-container nginx-img
    ```

## 2. Visit Website
* on web browser `http://localhost:8080`

## 3. Remove nginx container
* execute docker command
    ```sh
    docker stop nginx-container
    docker rm nginx-container
    ```