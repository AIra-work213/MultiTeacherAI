FROM python:3.12

RUN mkdir server

COPY requirements.txt ./server
RUN pip install --no-cache-dir -r ./server/requirements.txt


COPY models/russian_trusted_root_ca_pem.crt /server/models/russian_trusted_root_ca_pem.crt
COPY . ./server/
WORKDIR /server

CMD ["python", "server.py"]
