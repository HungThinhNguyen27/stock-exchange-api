FROM python:3.12

EXPOSE 5000

WORKDIR /src

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --force-reinstall -r requirements.txt
COPY . .

CMD ["python3", "app.py"]
 
