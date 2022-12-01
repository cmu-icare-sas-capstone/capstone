# app/Dockerfile

FROM python:3.9-slim

EXPOSE 8081

WORKDIR /app

RUN mkdir -p /app/data
RUN mkdir -p /app/data/pickles

COPY . .

RUN pip3 install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8081", "--server.address=0.0.0.0", "--server.maxUploadSize 2000"]
