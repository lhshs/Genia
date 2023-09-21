# Setup MLOps 

## 0. CI/CD Setting

### 0.1. Make Dockerfile
* jenkins.Dockerfile
	```Dockerfile
	FROM jenkins/jenkins:lts

	USER root

	RUN apt-get update

	RUN curl https://get.docker.com/ > dockerinstall && chmod 777 dockerinstall && ./dockerinstall
	```

* Build image
	```sh
	docker build -t jenkins-docker-img .
	```

### 0.2. Run jenkins-container
* Run command
	```sh
	docker run -d -u root \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-v $(pwd)/jenkins_home:/var/jenkins_home \
		-p 8080:8080 \
		--name jenkins-container \
		-t jenkins-docker-img
	```

* execute command
	```sh
	docker exec -it jenkins-container bash
	
	# in the container terminal
	docker ps -a
	```

* Get password
	```sh
	docker exec -it jenkins-container cat /var/jenkins_home/secrets/initialAdminPassword
	```

### 0.3. Run Elyra-container
* Run command
	```sh
	docker run -d \
		-p 8081:8888 \
		-v $(pwd)/jenkins_home:/var/jenkins_home \
		--name elyra-container -t elyra/elyra:3.15.0 \
		/usr/local/bin/start-elyra.sh --NotebookApp.token=''
	```

### 0.4. Ngrok Forwarding
* Setting Ngrok Container
  ```sh
  export NGROK_AUTHTOKEN={YOUR_NGROK_AUTHOKEN}
  docker run --rm --net=host -it \
    -e NGROK_AUTHTOKEN=${NGROK_AUTHTOKEN} \
    --name ngrok-container \
    ngrok/ngrok:latest http 8080
  ```

## 1. Install KFP
* Install Kubeflow Pipelines
  ```sh
  export PIPELINE_VERSION=2.0.1

  kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
  kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
  kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/dev?ref=$PIPELINE_VERSION"
  ```

* Delete unnecessary Resource `proxy-agent`
  ```sh
  kubectl delete deploy proxy-agent -n kubeflow
  ```
    
* Deploy `Minio`, `Kubeflow Pipelines` UI Interface
  ```yaml
  apiVersion: v1
  kind: Service
  metadata:
    name: minio-interface
    namespace: kubeflow
  spec:
    type: LoadBalancer
    selector:
      app: minio
    ports:
    - protocol: TCP
      port: 9000
      targetPort: 9000
  ---
  apiVersion: v1
  kind: Service
  metadata:
    name: kfp-ui-interface
    namespace: kubeflow
  spec:
    type: LoadBalancer
    selector:
      app: ml-pipeline-ui
    ports:
    - protocol: TCP
      port: 3000
      targetPort: 3000
  ---
  apiVersion: v1
  kind: Service
  metadata:
    name: kfp-external-interface
    namespace: kubeflow
  spec:
    type: LoadBalancer
    selector:
      app: ml-pipeline
    ports:
    - protocol: TCP
      port: 3001
      targetPort: 8888
  ---
  ```

## 3. Install Katib Experiment
* Install Katib Stand alone
  ```sh
  kubectl apply -k "github.com/kubeflow/katib.git/manifests/v1beta1/installs/katib-standalone?ref=master"
  ```

* Add RoleBinding
  ```sh
  export NAMESPACE=kubeflow
  kubectl -n ${NAMESPACE} create rolebinding katib-editor --clusterrole=katib-controller --serviceaccount=${NAMESPACE}:default
  ```

* Deploy `katib` UI Interface
  ```yaml
  apiVersion: v1
  kind: Service
  metadata:
    name: katib-interface
    namespace: kubeflow
  spec:
    type: LoadBalancer
    selector:
      katib.kubeflow.org/component: ui
    ports:
    - protocol: TCP
      port: 4000
      targetPort: 8080
  ```