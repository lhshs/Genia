FROM tensorflow/tensorflow:2.13.0

WORKDIR /workspace

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python"]
