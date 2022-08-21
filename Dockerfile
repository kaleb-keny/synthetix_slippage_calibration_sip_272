FROM synthetixio/docker-node:16.14-ubuntu

WORKDIR /app
COPY . .

RUN pip install -r env/requirements.txt

CMD ["./main.py"]