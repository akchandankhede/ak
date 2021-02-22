# pull official base image
FROM python:3.8

# set work directory
EXPOSE 8002
WORKDIR /app/

# set environment variables
ENV PYTHONUNBUFFERED 1

ENV DJANGO_SETTINGS_MODULE=WebForm.settings

# copy project
COPY app/requirements.txt /requirements.txt
COPY app/ /app/

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN chmod +x /app/*

CMD [ "/bin/bash", "-c", "python manage.py runserver 0.0.0.0:8002" ]
