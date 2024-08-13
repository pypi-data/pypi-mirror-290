FROM python:3.12 as base

WORKDIR /app
COPY requirements-test.txt .
RUN python -m pip install -r requirements-test.txt

COPY . .

CMD ["./test.sh"]
