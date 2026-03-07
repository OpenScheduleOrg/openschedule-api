FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY . .

RUN pip install -e .

CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app" ]
