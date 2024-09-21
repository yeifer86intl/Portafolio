FROM python:3.8.13 as base

ENV PYTHONPATH=$PYTHONPATH:/src/

COPY ./requirements.txt /src/requirements.txt

WORKDIR /src

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./ /src/

FROM base as test
RUN ["python", "-m", "pytest", "-v", "/src/tests"]

FROM base as build

CMD gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:5000 main:app