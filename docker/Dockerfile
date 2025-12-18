FROM python:3.11.12-slim 

RUN apt-get update

RUN mkdir /be_spa

WORKDIR /be_spa 

COPY req.txt .

RUN pip install -r req.txt

COPY . .

RUN chmod a+x /be_spa/docker/*.sh

CMD ["gunicorn", "src.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]