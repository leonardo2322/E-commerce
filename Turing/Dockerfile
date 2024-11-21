FROM python:3.13-alpine

WORKDIR /app

COPY E-commerce/Turing/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . . 

EXPOSE 8000

CMD ["python", "/app/Qrgenerator/manage.py", "runserver", "0.0.0.0:8000"]