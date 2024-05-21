FROM python:3.9

EXPOSE 5000

WORKDIR /Users/macos/Downloads/WORKSPACE/stock_project

COPY requirements.txt .


RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "app.py"]
 
