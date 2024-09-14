from python:3.8.13 as base

ENV PYTHONPATH=$PYTHONPATH:/src/

COPY ./requirements.txt /src/requirements.txt

WORKDIR /src

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./ /src/

FROM base as test
RUN ["python", "-m", "pytest", "-v", "tests"]

FROM base as build
CMD streamlit run --server.port 9090 app/image_classifier_app.py