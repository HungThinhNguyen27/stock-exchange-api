FROM python:3.9

EXPOSE 5000

WORKDIR /Users/macos/Downloads/WORKSPACE/stock_project

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "app.py"]
 

 # docker build -t thinh27/stock-exchange-apis 
 # docker container rm example02
 # docker run --name example03 -p 8888:5000 --network stock-exchange-apis-networks thinh27/stock-exchange-apis 

 # docker run --name mysql-container  -p 3307:3306 --network stock-exchange-apis-networks -e MYSQL_ROOT_PASSWORD=thinh123 -d mysql:8.0

# docker network create stock-exchange-apis-networks

# docker exec -it mysql-container bash
# mysql -u root -p 
# update mysql.user set host ='%' where user ='root';
# GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
# ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'password';
# flush privileges;
# docker network inspect stock-exchange-apis-networks | jq '.[0].Containers ' 

