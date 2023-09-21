# Tensorflow Serving Tutorial

## 1. Run Tensorflow Serving Container
* Run container
	```sh
	docker run -d \
		-p 8501:8501 \
		-v $(pwd)/saved_model_half_plus_two:/models/half_plus_two \
		-e MODEL_NAME=half_plus_two \
		--name tf-serving-container \
		-t tensorflow/serving
	```

## 2. Test Prediction
* send Prediction API
	```sh
	curl -d '{"instances": [1.0, 2.0, 5.0]}' \
		-X POST http://localhost:8501/v1/models/half_plus_two:predict
	```

* expeted response data
	```json
	{
		"predictions": [2.5, 3.0, 4.5]
	}
	```
