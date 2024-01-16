
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
# Assuming you have defined your ORM models
from your_application.model import ASA, OrderBookEntry

# Replace 'your_database_url' with your actual database URL
engine = create_engine('your_database_url')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def purchase_asa(user_id: int, xu_amount: int):
    with SessionLocal() as session:
        try:
            # Begin the transaction
            session.begin()

            # Check the order book for the lowest price (sổ lệnh)
            lowest_price_entry = session.query(OrderBookEntry).order_by(
                OrderBookEntry.price.asc()).first()

            if not lowest_price_entry or xu_amount < lowest_price_entry.price:
                raise ValueError(
                    'Not enough Xu to buy ASA at the lowest market price.')

            # Calculate how many ASA can be bought at the lowest price
            asa_quantity = xu_amount // lowest_price_entry.price
            xu_spent = asa_quantity * lowest_price_entry.price
            xu_remaining = xu_amount - xu_spent

            # Update the order book entry
            lowest_price_entry.quantity -= asa_quantity
            if lowest_price_entry.quantity == 0:
                session.delete(lowest_price_entry)
            else:
                session.merge(lowest_price_entry)

            # Record the ASA purchase for the user
            user_asa = ASA(user_id=user_id, quantity=asa_quantity,
                           price=lowest_price_entry.price)
            session.add(user_asa)

            # Commit the transaction
            session.commit()

            # Return the result of the transaction
            return {
                "asa_purchased": asa_quantity,
                "xu_spent": xu_spent,
                "xu_remaining": xu_remaining
            }
        except IntegrityError as e:
            # Rollback the transaction in case of an integrity error
            session.rollback()
            raise e
        except Exception as e:
            # Rollback the transaction for any other exception
            session.rollback()
            raise e

# Example usage:
# result = purchase_asa(user_id=123, xu_amount=10000)
# print(result)
