import sqlalchemy as sq
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class Publisher(Base):
    """Класс таблицы publisher"""
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(40), unique=True, nullable=False)

    def __str__(self):
        """Возвращает данные таблицы для print()"""
        return f'{self.id}: {self.name}'


class Book(Base):
    """Класс таблицы book"""
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(60), unique=True, nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(Publisher, backref="books")

    def __str__(self):
        """Возвращает данные таблицы для print()"""
        return f'{self.id}: {self.title} ({self.id_publisher})'


class Shop(Base):
    """Класс таблицы shop"""
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(40), nullable=False)

    def __str__(self):
        """Возвращает данные таблицы для print()"""
        return f'{self.id}: {self.name}'


class Stock(Base):
    """Класс таблицы stock"""
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    book = relationship(Book, backref="stocks")
    shop = relationship(Shop, backref="stocks")

    def __str__(self):
        """Возвращает данные таблицы для print()"""
        return f'{self.id}: {self.count}'


class Sale(Base):
    """Класс таблицы sale"""
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.REAL, nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship(Stock, backref="sales")

    def __str__(self):
        """Возвращает данные таблицы для print()"""
        return f'{self.id}: {self.date_sale} - {self.price} руб. ({self.count} шт.)'
