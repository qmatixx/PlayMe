FROM python:3-alpine3.15
WORKDIR /playme
COPY . /playme/
RUN pip install -r requirements.txt
EXPOSE 3000
CMD python ./run.py