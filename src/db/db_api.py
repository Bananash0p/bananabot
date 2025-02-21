from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, User, Order, Proxy


class DatabaseAPI:
    def __init__(self, db_url='sqlite:///db.sqlite3'):
        self.engine = create_engine(db_url, echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def create_user(self, telegram_user_id: int):
        """Create new user with the given tg user"""
        session = self.Session()
        try:
            user = User(telegram_user_id=telegram_user_id, balance=0)
            session.add(user)
            session.commit()
            return user
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def add_balance(self, telegram_user_id: int, amount: float):
        """Adds balance (in dollars) to the specified user"""
        session = self.Session()
        try:
            user = session.query(User).filter_by(telegram_user_id=telegram_user_id).first()
            if not user:
                raise ValueError("User not found")
            user.balance += amount
            session.commit()
            return user.balance
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def add_proxy(self, proxy_data):
        """
        Adds one or many proxies.
        Accepts a dict for a single proxy or a list of dicts.
        Each dict should have keys: ip, port, protocol, and price.
        """
        session = self.Session()
        try:
            if isinstance(proxy_data, dict):
                proxy_data = [proxy_data]
            proxies = []
            for data in proxy_data:
                proxy = Proxy(
                    ip=data['ip'],
                    port=data['port'],
                    protocol=data['protocol'],
                    price=data['price'],
                    is_assigned=data.get('is_assigned', False)
                )
                session.add(proxy)
                proxies.append(proxy)
            session.commit()
            return proxies
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def buy_proxies(self, telegram_user_id: int, proxy_ids: list):
        """
        Buys proxies for the given user.
        Checks if the user exists, verifies that the requested proxies are available,
        ensures the user has sufficient balance, creates an order,
        and marks the proxies as assigned with a validity period of one month.
        """
        session = self.Session()
        try:
            user = session.query(User).filter_by(telegram_user_id=telegram_user_id).first()
            if not user:
                raise ValueError("User not found")
            
            proxies = session.query(Proxy).filter(
                Proxy.id.in_(proxy_ids),
                Proxy.is_assigned == False
            ).with_for_update().all()
            
            if len(proxies) != len(proxy_ids):
                raise ValueError("Some proxies are not available")
            
            total_price = sum(proxy.price for proxy in proxies)
            if user.balance < total_price:
                raise ValueError("Insufficient balance")
            
            user.balance -= total_price

            order = Order(user_id=user.telegram_user_id, order_date=datetime.utcnow(), total_amount=total_price)
            session.add(order)
            session.flush()  

            valid_until = datetime.utcnow() + timedelta(days=30)
            for proxy in proxies:
                proxy.is_assigned = True
                order_item = OrderItem(order_id=order.id, proxy_id=proxy.id, valid_until=valid_until)
                session.add(order_item)

            session.commit()
            return order
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
