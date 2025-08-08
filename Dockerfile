FROM python:3.12

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

ENV DB_PORT=5432

COPY . .

CMD ["python", "app.py"]