# Jenkins Image with built docker setting

## 1. Make Dockerfile
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

## 2. Run jenkins-container
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

## 3. Run Elyra-container
* Run command
	```sh
	docker run -d \
		-p 8081:8888 \
		-v $(pwd)/jenkins_home:/var/jenkins_home \
		--name elyra-container -t elyra/elyra:3.15.0 \
		/usr/local/bin/start-elyra.sh --NotebookApp.token=''
	```