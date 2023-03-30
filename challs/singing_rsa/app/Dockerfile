FROM python:3.9

WORKDIR /app

ARG FLAG
ENV FLAG=$FLAG

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]