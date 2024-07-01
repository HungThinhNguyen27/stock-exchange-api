
# Stock Exchange APIs

## Table of Contents
1. [Introduction](#1-introduction)
2. [Technologies Used](#2-technologiesUsed)
3. [Features](#3-features)
4. [Installation](#4-installation)
5. [Usage](#5-usage)
6. [Configuration](#6-configuration)
7. [Contact](#7-contact)

## 1. Introduction
The Stock Exchange APIs project is designed to facilitate the retrieval and management of stock data from the Tiki-Exchange website, offering a comprehensive set of APIs for real-time stock information and transaction execution in the stock market. This endeavor aims to provide a robust and adaptable system capable of handling diverse stock trading needs efficiently.

This project not only aims to streamline stock data management but also offers robust transaction capabilities adhering to ACID principles for data consistency and reliability. Users can interact with the system through well-documented APIs, facilitating smooth integration into various applications and environments.

## 2. Technologies Used

- **Programming Language:** Python ![Python](https://img.shields.io/badge/python-3.12.0-blue)
- **Web Framework:** Flask ![Flask](https://img.shields.io/badge/Flask-v2.0-green)
- **Authentication:** JWT ![JWT](https://img.shields.io/badge/JWT-v2.2.0-blue)
- **ORM:** SQLAlchemy ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-v1.4-blue)
- **Database:** MySQL ![MySQL](https://img.shields.io/badge/MySQL-v8.0-orange)
- **Caching:** Redis ![Redis](https://img.shields.io/badge/Redis-v6.0-red)
- **API Documentation:** Swagger ![Swagger](https://img.shields.io/badge/Swagger-v3.0-lightgrey)
- **Containerization:** Docker ![Docker](https://img.shields.io/badge/Docker-v20.10-blue)
- **Task Scheduler:** Airflow ![Airflow](https://img.shields.io/badge/Airflow-v2.0-yellow)
- **Testing Framework:** Unit Testing ![Unit Testing](https://img.shields.io/badge/Unit%20Testing-pytest-green)
- **Continuous Integration:** Jenkins ![Jenkins](https://img.shields.io/badge/Jenkins-v2.303.1-red)


## 3. Features
1. **Crawl Data:**

    - The system automatically collects stock data from the Tiki-Exchange website every minute. 

    - We build this job on docker so that every time we start collecting, the system will load a record from the database with the most recent time and we add one minute to that record. it will be called start_date and current_date is the current time. at location(Asia/Ho_Chi_Minh).

    - When crawling data from Tiki-Exchange, we need to have three parameters:
        - period: The number of minutes.
        - time_from: The start time.
        - time_to: The end time.
    - Example: 
        -  The record from the database has the most recent time is '2024-07-02 01:23' .
        - We add one minute to that record '2024-07-02 01:24'. it will be called Start_date
        - Current_date is the end time like '2024-07-02 01:25'




2. **APIs for stock data:**

    - Provides stock indices with data collected from charts on the Tiki-Exchange site.

    - Users enter parameters to view stock charts for each period. Data is collected in real-time, so we have tried to improve the candlestick chart display function in the best and fastest way.

    - Includes endpoints for:
        - order books
        - Market transactions
        - Candlestick chart display enhancement for optimal performance.


3. **APIs transactions Buy/Sell**

    - Provides robust APIs for executing buy and sell transactions in the stock market. 
    - The system implements ACID (Atomicity, Consistency, Isolation, Durability) principles to ensure transactional integrity and data consistency throughout the process. In case of any transactional failures, the system automatically rolls back to maintain data integrity.

4. **Login & Authentication**

    - Login APIs use JWT (JSON Web Token) to authenticate users.

5. **Stock-exchange-api Services Send Errors to Slack**

   - **Slack Integration:** Set up a Slack App or use a Slack Webhook URL to enable error notifications to a specific Slack channel.
   
   - **Configure Slack Token:** Integrate the Slack Token into the Docker environment variables. This can be done via Docker Compose or directly in the Dockerfile.
   
   - **Implement Error Handling:** Enhance the `stock-exchange-api` codebase to include error handling mechanisms. Implement a function or middleware to catch and log desired errors.
   
   - **Send Notifications:** Utilize the configured Slack Token to send notifications to the designated Slack channel when errors occur. Ensure the notifications provide sufficient information for prompt troubleshooting.


## 4. Installation
- Prerequisites
    - Python >= 3.8
    - Flask >= 2.0

    ### Setup
- Clone the repository and move into it:

        git clone https://github.com/HungThinhNguyen27/stock-exchange-api.git

        cd stock-exchange-api

- Set up virtual environment for stock-exchange-apis services : 

        python3.12 -m venv src/env #I'm using python version 3.12

        source src/env/bin/activate

- Set up virtual environment for crawl-data services : 

        python3.12 -m venv cron_jobs/env #I'm using python version 3.12

        source cron_jobs/env/bin/activate

        
- Install the library into the virtual environment : 

        pip install -r src/requirements.txt

        pip install -r cron_jobs/requirements.txt         

### **Documentation Swagger on Docker** 

- **http://127.0.0.1:5010/api/docs**

## 5. Usage



- Run server on Localhost:

        python3 src/app.py

- Crawl-data on Localhost:

        python3 cron_jobs/crawl_data.py

- Build all services on docker:

        docker-compose --env-file src/config.yaml up --detach
    
## 6. Configuration

- Create src/config.yaml file, Then configure according to the following instructions:

        # src/config.yaml, it is the configuration file of services stock-exchange-apis 

        KEY: "this is SECRET_KEY" # Secret key used for securing sessions and cryptographic operations

        # MySQL Database Configuration
        MYSQL_HOST: "mysql"        # Hostname of the MySQL container within Docker network
        MYSQL_PORT: 3306           # Port number of MySQL server (default is 3306)
        MYSQL_USER: "root"         # Username for accessing MySQL database
        MYSQL_PASSWORD: "password" # Password for the MySQL user
        MYSQL_DB: "database_name"  # Name of the MySQL database to connect

        # Port for Stock Exchange Service
        STOCK_EXCHANGE_PORT: 5000  # Port number on which the stock exchange service will run

        # Redis Configuration
        REDIS_HOST: "redis"        # Hostname of the Redis container within Docker network
        REDIS_PORT: 6379           # Port number of Redis server (default is 6379)

        # Slack Integration Token
        SLACK_TOKEN: "your_slack_token_here"  # Token for integrating with Slack API

- Create cron_jobs/config.yaml file , Then configure according to the following instructions:

        # cron_jobs/config.yaml, it is the configuration file of the data crawl function

        MYSQL_HOST: "mysql"        # Hostname of the MySQL container within Docker network
        MYSQL_PORT: 3306           # Port number of MySQL server (default is 3306)
        MYSQL_USER: "root"         # Username for accessing MySQL database
        MYSQL_PASSWORD: "password" # Password for the MySQL user
        MYSQL_DB: "database_name"  # Name of the MySQL database to connect

## 7. Contact

- **Author**: Nguyen Hung Thinh

- **Email**: thinhung4199@gmail.com


