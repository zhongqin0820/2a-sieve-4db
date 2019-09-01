FROM python:3
VOLUME /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./run.py" ]
