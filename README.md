
# Stock Exchange APIs

This project aims to collect stock data from the Tiki-Exchange website and provide APIs to display stock information as well as perform buy/sell transactions on the stock market. The main goal of the project is to create a flexible and powerful system for managing stock data and executing transactions efficiently.


## features: 
1. Crawl Data:
the system automatically crawls stock data from the Tiki-Exchange website every day.
Automated planning to ensure data updates over time.

2. Restful APIs for stock data:
Provide Restful APIs to display stock information collected from Tiki-Exchange.
Includes endpoints for stock prices, buy/sell order books, and market transactions for stocks


3. APIs transactions Buy/Sell
Provides trading APIs so users can make stock buy/sell transactions.
Ensuring safety and authenticity during transactions.

4. Login & Authentication 
Login APIs use JWT (JSON Web Token) to authenticate users.

## Setup
Clone the repository and move into it:

    git clone https://github.com/HungThinhNguyen27/stock-exchange-api.git

    cd stock-exchange-api

Setup Python environment: 

    pip install -r requirements.txt

Run server on Localhost:

    python3 app.py

Run server on Docker:

    docker-compose --file ./docker-compose.yaml up --detach
    
## Usage

1. The server on localhost has the URL:
    http://127.0.0.1:5001

2. The server on docker has the URL:
    http://127.0.0.1:5010

## APIs Endpoints

The following API endpoints are available:

    - GET /stock-candles: Retrieve a paginated list of stock price.
    - GET /book-orders-buy: Get a paged list of book order buys in ascending order.
    - GET /book-orders-sell: Get a paged list of book order sell in descending order.
    - GET /market_trans_bought: Get a paged list of market transactions by most recent purchase.
    - GET /market_trans_sold: Get a paged list of market transactions by most recent purchase.

    - POST /account: Create account.
    - POST /login: Use account to receive jwt token.
    - PUT /buy-now": Use coins to buy asa quickly at the lowest price.
    - PUT /sell-now": Use astra to sell asa quickly at the highest price.
    - PUT /buy-limit": Use coins to buy astra at the desired price.
    - PUT /sell-limit": Use astra to sell astra at the desired price.




