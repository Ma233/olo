# coding=utf-8
from datetime import datetime, date
from uuid import uuid4

from tests.fixture import (  # noqa pylint:disable=W
    TestCase, mc, beansdb,
    init_tables,
    MYSQL_HOST, MYSQL_PORT,
    MYSQL_USER, MYSQL_PASSWORD,
    MYSQL_DB, MYSQL_CHARSET,
)

from olo import MySQLDataBase, Model, Field, DbField
from olo.debug import set_debug


init_tables()
set_debug(True)
db = MySQLDataBase(
    MYSQL_HOST, MYSQL_PORT,
    MYSQL_USER, MYSQL_PASSWORD,
    MYSQL_DB,
    charset=MYSQL_CHARSET,
    beansdb=beansdb
)


class _BaseModel(Model):
    class Options:
        db = db
        cache_client = mc
        enable_log = True


class BaseModel(_BaseModel):
    class Options:
        reason = 'test inherit'

    def __eq__(self, other):
        pk_name = self.get_singleness_pk_name()
        return (
            self.__class__ is other.__class__ and
            getattr(self, pk_name) == getattr(other, pk_name)
        )


class Dummy(BaseModel):
    id = Field(int, primary_key=True)
    name = Field(str, noneable=True, default='dummy')
    age = Field(int, default=12, on_update=lambda x: x.__class__.age + 1)
    password = Field(str, noneable=True, encrypt=True)
    flag = Field(int, noneable=True, choices=[0, 1, 2])
    tags = Field([str], default=[])
    payload = Field({str: [int]}, noneable=True, default={})
    foo = Field(int, noneable=True,)
    dynasty = Field(str, default='现代')
    dynasty1 = Field(str, noneable=True)
    created_at = Field(
        datetime,
        default=datetime.now
    )
    updated_at = Field(
        datetime,
        default=datetime.now,
        on_update=datetime.now
    )
    created_date = Field(
        date,
        default=date.today
    )
    prop1 = DbField([str], noneable=True)
    count = DbField(int, default=0, choices=range(30),
                    on_update=lambda x: x.count + 3)
    db_dt = DbField(datetime, noneable=True)
    count1 = DbField(int, noneable=True)

    def get_uuid(self):
        return '/dummy/{}'.format(self.id)

    def after_update(self):
        after_update()

    def before_update(self, **attrs):
        before_update()

    @classmethod
    def before_create(cls, **attrs):
        before_create()

    @classmethod
    def after_create(cls, inst):
        after_create()


class Foo(BaseModel):
    id = Field(int, primary_key=True)
    name = Field(str, noneable=True, default='foo')
    age = Field(int, noneable=True, default=1)
    age_str = Field(int, noneable=True, default=1, output=str)
    key = Field(str, noneable=True, default=lambda: str(uuid4()))
    prop1 = DbField(list, noneable=True)

    __unique_keys__ = (
        ('name', 'age'),
        ('key',)
    )

    __index_keys__ = (
        'age',
    )

    def get_uuid(self):
        return '/foo/{}'.format(self.id)


class Bar(BaseModel):
    name = Field(str, primary_key=True)
    age = Field(int, default=1)
    xixi = Field(str, name='key', default=lambda: str(uuid4()))
    word = Field(str, noneable=True)
    prop1 = DbField(list, noneable=True)

    __index_keys__ = (
        (),
        ('xixi', 'age'),
        'age'
    )

    __order_bys__ = (
        'xixi',
        ('xixi', 'age'),
        ('-age', 'xixi'),
    )

    def get_uuid(self):
        return '/foo/{}'.format(self.id)


class Ttt(BaseModel):
    id = Field(int, primary_key=True, output=str)
    time = Field(
        datetime,
        name='created_at',
        default=datetime.now
    )


class Lala(BaseModel):
    id = Field(int, primary_key=True, output=str)
    name = Field(str)
    age = Field(int)


def after_update():
    pass


def before_update():
    pass


def after_create():
    pass


def before_create():
    pass
