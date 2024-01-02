FROM python:3.10.12

ENV PYTHONUNBUFFERED 1

COPY . /app

WORKDIR /app

COPY ./boot.sh /
RUN chmod 755 /boot.sh

RUN pip install pipenv

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
