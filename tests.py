from app import client
from models import Parseritem


def test_simple():
    mylist = [1, 2, 3, 4, 5]
    assert 1 in mylist


def test_get():
    res = client.get('/api/v1/items')

    assert res.status_code == 200
    assert len(res.get_json()) == len(Parseritem.query.all())
    assert res.get_json()[0]['id'] == 0


def test_post():
    data = {
        'title': 'Unit Tests',
        'usd_price': '500',
        'city': 'home_test',
        'description': 'Milk, Cheese, Pizza, Fruit, Tylenol'
    }

    res = client.post('/api/v1/items', json=data)

    assert res.status_code == 200



def test_put():
    res = client.put('/api/v1/items/1', json={'title': 'UPD'})

#    assert res.status_code == 200
    assert Parseritem.query.get(1).title == 'UPD'


def test_delete():
    res = client.delete('/api/v1/items/1')

    assert res.status_code == 204
    assert Parseritem.query.get(1) is None
