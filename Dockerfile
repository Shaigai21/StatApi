FROM python:latest
COPY . .
RUN pip install -r modules.txt
CMD uvicorn main:app
