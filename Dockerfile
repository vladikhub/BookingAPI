FROM python:3.11

WORKDIR /app
RUN pip install requirements.txt

COPY . .

CMD ["python", "src/main.py"]