from data_layer.transaction import PurchaseTransaction
from data_layer.mysql_connect import MySqlConnect

c = MySqlConnect()
a = PurchaseTransaction(c.session)

# Example usage
b = a.buy_now_trans(1, 100, 100)
print(b)
