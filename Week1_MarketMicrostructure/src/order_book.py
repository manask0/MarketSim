"""
Changes to be made :
Store in a data base to use with sql
implement heap for more efficiency.
"""




import math
from collections import deque

class Order:
    def __init__(self, idNum, ticker, side, order_type, price, qty, timestamp):
        self.id = idNum
        self.ticker = ticker
        self.side = side          # 'bid' or 'ask'
        self.type = order_type    # 'limit' or 'market'
        self.price = price
        self.qty = qty
        self.timestamp = timestamp

    def __repr__(self):
        return f"Order(id={self.id}, {self.side}, {self.qty}@{self.price})"

class OrderBook:
    valid_sides = ('bid', 'ask')
    valid_types = ('limit', 'market')
    def __init__(self, tickSize = 0.01):
        self.tickSize = tickSize
        self.rounder = int(math.log10(1 / tickSize))
        self.time = 0
        self.nextQuoteID = 0
        self.lastPrice = {}  # ticker -> last traded price

    # Implementing without heaps for simplicity
        self.bids = {}  # ticker -> { price: deque[Order] }
        self.asks = {}  # ticker -> { price: deque[Order] }
    
    def clipPrice(self, price):
        return round(price, self.rounder)
    
    def updateTime(self):
        self.time +=1

    def processOrder(self, quote):
        self.updateTime()
        self.nextQuoteID += 1
        quote['timestamp'] = self.time
        quote['id'] = self.nextQuoteID
        if quote['qty'] <= 0:
            raise ValueError("Quantity must be positive")

        if quote['side'] not in self.valid_sides:
            raise ValueError("Invalid side")

        if quote['type'] not in self.valid_types:
            raise ValueError("Invalid order type")
        
        if quote['type'] == 'limit':
            quote['price'] = self.clipPrice(quote['price'])
        else:
            quote['price'] = None
        
        # Creating Order Object

        order = Order(
        idNum=quote['id'],
        ticker=quote['ticker'],
        side=quote['side'],
        order_type=quote['type'],
        price=quote['price'],
        qty=quote['qty'],
        timestamp=quote['timestamp']
        )

        trades = self.match(order)
        #Store remaining order
        if order.qty > 0 and order.type == 'limit':
            self.addToBook(order)
        return trades
    
    def match(self, order):
        trades = []
        if order.side == 'bid':
            book = self.asks
            price_cmp = lambda p: order.price is None or p <= order.price #cmp is compare, returns a bool.
        else:
            book = self.bids
            price_cmp = lambda p: order.price is None or p >= order.price
        
        ticker = order.ticker

        if ticker not in book:
            return trades  # No orders to match against
        
        # Get sorted prices
        prices = sorted(book[ticker].keys())
        if order.side == 'ask':
            prices = prices[::-1]  # highest bid first
        
        # Walk through prices
        for price in prices:
            if order.qty <= 0:
                break  # Order fully filled
            if not price_cmp(price):
                break  # Price not acceptable

            queue = book[ticker][price]

            # Walk FIFO queue

            # Walk FIFO queue
            while queue and order.qty > 0: #ie queue is not empty and incoming orders qty >0
                resting = queue[0] #fetches oldest order without removing it

                traded_qty = min(order.qty, resting.qty)
                order.qty -= traded_qty
                resting.qty -= traded_qty

                self.lastPrice[ticker] = price

                trades.append(
                    (order.id, resting.id, price, traded_qty)
                )


                print(f"TRADE {ticker} : {traded_qty} units @ Rs. {price}")

                if resting.qty == 0:
                    queue.popleft()

            # Remove empty price level
            if not queue:
                del book[ticker][price]

        return trades




    def addToBook(self, order):
        book = self.bids if order.side == 'bid' else self.asks

        book.setdefault(order.ticker, {})
        book[order.ticker].setdefault(order.price, deque())
        book[order.ticker][order.price].append(order)

    def printBook(self, ticker):
        print("---- BIDS ----")
        for p in sorted(self.bids.get(ticker, {}), reverse=True):
            print(p, list(self.bids[ticker][p]))

        print("---- ASKS ----")
        for p in sorted(self.asks.get(ticker, {})):
            print(p, list(self.asks[ticker][p]))
    
if __name__ == "__main__":
    ob = OrderBook(tickSize=0.01)

    ob.processOrder({
        'ticker': 'AAPL',
        'side': 'bid',
        'type': 'limit',
        'price': 100.03,
        'qty': 10
    })

    ob.processOrder({
        'ticker': 'AAPL',
        'side': 'bid',
        'type': 'limit',
        'price': 100.00,
        'qty': 5
    })
    ob.processOrder({
        'ticker': 'AAPL',
        'side': 'bid',
        'type': 'limit',
        'price': 100.01,
        'qty': 5
    })

    ob.printBook('AAPL')
    





