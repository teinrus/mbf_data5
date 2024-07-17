from peewee import *
import datetime
from dotenv import load_dotenv
import os
# Настройка подключения к базе данных PostgreSQL
db = PostgresqlDatabase(
    'temruk',
    user=os.getenv("user"),
    password=os.getenv("password"),
    host=os.getenv("host"),
    port=os.getenv("port")  # стандартный порт для PostgreSQL
)

class BaseModel(Model):
    class Meta:
        database = db

class temruk_BottleExplosion5(BaseModel):
    data = DateField()
    time = TimeField()
    bottle = IntegerField()
    number = IntegerField(null=True, default=0)

def save_bottle_explosion(data, time, bottle, number=0):
    """
    Сохраняет данные о взрыве бутылки в базу данных.

    :param data: Дата взрыва (объект datetime.date)
    :param time: Время взрыва (объект datetime.time)
    :param bottle: Взрыв (целое число)
    :param number: Номер крана (целое число, по умолчанию 0)
    :return: Экземпляр модели BottleExplosion5
    """
    db.connect()
    explosion = temruk_BottleExplosion5.create(
        data=data,
        time=time,
        bottle=bottle,
        number=number
    )
    db.close()
    return explosion




    
