FROM python:3.8

WORKDIR /api
COPY . . 

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["delivery-api.py"]