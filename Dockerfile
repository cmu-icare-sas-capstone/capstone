# app/Dockerfile

FROM python:3.9-slim

EXPOSE 8081

WORKDIR /

RUN mkdir -p data
RUN mkdir -p data/pickles

COPY . .

RUN pip3 install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8081", "--server.address=0.0.0.0"]
