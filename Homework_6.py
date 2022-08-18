import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import configparser
import json


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


def _select_publ_id(id_publ):
    """Запрашивает данные о издателе по id"""
    res = session.query(Publisher).join(Book.publisher).filter(Publisher.id == id_publ)
    return res


def _select_publ_name(name_publ):
    """Запрашивает данные о издателе по имени"""
    res = session.query(Publisher).join(Book.publisher).filter(Publisher.name == name_publ)
    return res


def search_publ():
    """Находит данные издателя в БД по id или name"""
    text = input('Введите id или название издателя:\n')
    if text.isalpha():
        res = _select_publ_name(text)
    else:
        res = _select_publ_id(text)
    _print_publ_book(res)


def _print_publ_book(q):
    """Распечатывает результаты запроса издатель_книги"""
    for s in q.all():
        print(f'{s.id}: {s.name}')
        for bk in s.books:
            if bk:
                print(f'\t{bk.id}: {bk.title}')


def load_data_json(file_json):
    """Загружает в БД данные из json в виде объектов"""
    with open(file_json, encoding="utf-8") as file:
        data = json.load(file)

    objects = []

    print('Созданы объекты:')
    for d in data:
        d_f = d["fields"]
        if d["model"] == "publisher":
            globals()["publisher" + str(d["pk"])] = Publisher(
                id=d["pk"],
                name=d_f["name"]
            )

        elif d["model"] == "book":
            globals()["book" + str(d["pk"])] = Book(
                id=d["pk"],
                title=d_f["title"],
                id_publisher=d_f["id_publisher"]
            )

        elif d["model"] == "shop":
            globals()["shop" + str(d["pk"])] = Shop(
                id=d["pk"],
                name=d_f["name"]
            )

        elif d["model"] == "stock":
            globals()["stock" + str(d["pk"])] = Stock(
                id=d["pk"],
                id_shop=d_f["id_shop"],
                id_book=d_f["id_book"],
                count=d_f["count"]
            )

        elif d["model"] == "sale":
            globals()["sale" + str(d["pk"])] = Sale(
                id=d["pk"],
                price=d_f["price"],
                date_sale=d_f["date_sale"],
                count=d_f["count"],
                id_stock=d_f["id_stock"]
            )

        objects.append(globals()[d["model"] + str(d["pk"])])
        print(f'{d["model"]}{d["pk"]}')
    session.add_all(objects)
    session.commit()


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")

    name_driver_sql = config["POSTGRESQL"]["driver_sql"]
    login = config["POSTGRESQL"]["login"]
    password = config["POSTGRESQL"]["password"]
    name_conn = config["POSTGRESQL"]["name_connection"]
    port_conn = config["POSTGRESQL"]["port_connection"]
    name_db = config["POSTGRESQL"]["name_db"]

    DSN = f"{name_driver_sql}://{login}:{password}@{name_conn}:{port_conn}/{name_db}"
    engine = sq.create_engine(DSN)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # shop1 = Shop(name="Читай-Город")
    # shop2 = Shop(name="Большой Книжный")
    # shop3 = Shop(name="Буквоед")
    #
    # session.add_all([shop1, shop2, shop3])
    # session.commit()
    #
    # publ1 = Publisher(name="АСТ")
    # publ2 = Publisher(name="Абсолютное оружие")
    # publ3 = Publisher(name="Мировая классика")
    #
    # session.add_all([publ1, publ2, publ3])
    # session.commit()
    #
    # book1 = Book(title="Есенин", id_publisher=3)
    # book2 = Book(title="Дюна",  id_publisher=2)
    # book3 = Book(title="Властелин колец",  id_publisher=1)
    # book4 = Book(title="Преступление и наказание",  id_publisher=3)
    # book5 = Book(title="Солярис",  id_publisher=1)
    # book6 = Book(title="Боевые роботы",  id_publisher=2)
    #
    # session.add_all([book1, book2, book3, book4, book5, book6])
    # session.commit()
    #
    # stock11 = Stock(id_book=1, id_shop=1, count=10)
    # stock21 = Stock(id_book=2, id_shop=1, count=8)
    # stock31 = Stock(id_book=3, id_shop=1, count=5)
    # stock41 = Stock(id_book=4, id_shop=1, count=15)
    # stock51 = Stock(id_book=5, id_shop=1, count=3)
    # stock61 = Stock(id_book=6, id_shop=1, count=6)
    #
    # stock12 = Stock(id_book=1, id_shop=2, count=4)
    # stock32 = Stock(id_book=3, id_shop=2, count=7)
    # stock42 = Stock(id_book=4, id_shop=2, count=6)
    # stock52 = Stock(id_book=5, id_shop=2, count=5)
    #
    # stock23 = Stock(id_book=2, id_shop=3, count=16)
    # stock43 = Stock(id_book=4, id_shop=3, count=2)
    # stock63 = Stock(id_book=6, id_shop=3, count=8)
    #
    # session.add_all([stock11, stock21, stock31, stock41, stock51, stock61,
    #                  stock12, stock32, stock42, stock52,
    #                  stock23, stock43, stock63])
    # session.commit()
    #
    # sale1 = Sale(price=600, date_sale="2022-08-10 13:40:00", id_stock=1, count=3)
    # sale2 = Sale(price=700, date_sale="2022-08-15 16:02:00", id_stock=6, count=2)
    # sale3 = Sale(price=850, date_sale="2022-08-01 09:58:00", id_stock=11, count=4)
    #
    # session.add_all([sale1, sale2, sale3])
    # session.commit()

    load_data_json("data.json")
    search_publ()

    session.close()
