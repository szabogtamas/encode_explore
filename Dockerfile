FROM python:3-alpine

RUN apk --no-cache add curl
RUN apk --no-cache add zlib-dev

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./your-daemon-or-script.py" ]