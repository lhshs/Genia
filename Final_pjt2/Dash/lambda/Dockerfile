FROM python:3.10

COPY ./ ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python", "Video_To_RDS.py"]