FROM python:3.10-alpine

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt --index-url=https://pypi.org/simple/

COPY . . 

EXPOSE 8000

CMD ["python", "/app/Qrgenerator/manage.py", "runserver", "0.0.0.0:8000"]