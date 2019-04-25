ARG PYTHON_BASE_IMG=python:3
FROM ${PYTHON_BASE_IMG}

WORKDIR /usr/src/app

COPY Pipfile ./
RUN pip install pipenv
RUN pipenv lock -r > requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
