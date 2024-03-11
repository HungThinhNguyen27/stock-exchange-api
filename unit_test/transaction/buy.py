import unittest
from unittest.mock import Mock, patch
from data_layer.transaction.buy import BuyTransaction


class TestBuyTransaction(unittest.TestCase):

    def setUp(self):
        self.mock_session = Mock()
        self.buy_transaction = BuyTransaction()
        self.buy_transaction.session = self.mock_session

    @patch('data_layer.transaction.buy.BuyTransaction.check_balance_coins')
    @patch('data_layer.transaction.buy.BuyTransaction.get_by_name')
    @patch('data_layer.transaction.buy.BuyTransaction.get_lowest_price_sell')
    def test_buy_now_trans(self, mock_get_lowest_price_sell, mock_get_by_name, mock_check_balance_coins):
        mock_check_balance_coins.return_value = True
        mock_get_by_name.return_value = 1  # Mocked user ID
        # mock_get_lowest_price_sell.return_value = [(20, [2, 3], 100)]
        current_user_name = "thinh123"
        result = self.buy_transaction.buy_now_trans(current_user_name,
                                                    1000)
        print("result", result)

        self.assertEqual(result, 50, 1000)

    @patch('data_layer.transaction.buy.BuyTransaction.check_balance_coins')
    @patch('data_layer.transaction.buy.BuyTransaction.get_by_name')
    def test_buy_limit_trans(self, mock_get_by_name, mock_check_balance):
        mock_check_balance.return_value = True
        mock_get_by_name.return_value = 1

        current_user_name = "thinh123"
        astra_price = 10
        coins_quantity = 100

        result = self.buy_transaction.buy_limit_trans(
            current_user_name, astra_price, coins_quantity)

        # Assertions
        self.assertEqual(result, (astra_price, coins_quantity,
                         coins_quantity // astra_price))


if __name__ == '__main__':
    unittest.main()
