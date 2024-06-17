FROM python:3.11

WORKDIR /app

COPY /requirements.txt .
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN ls -la
ENTRYPOINT [ "python", "app.py" ]