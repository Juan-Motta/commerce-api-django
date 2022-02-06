FROM python:3
WORKDIR /app
ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app