FROM python:3.12


RUN mkdir app
COPY requirements.txt ./app
RUN pip install --no-cache-dir -r ./app/requirements.txt

COPY app.py ./app/
WORKDIR /app

CMD ["python", "app.py"]