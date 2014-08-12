__author__ = 'Administrator'

from faker import Faker
import pymongo, hashlib, time, uuid

db = pymongo.MongoClient().test_mycontacts
db.contacts.remove({})
f = Faker()

for i in range(10):
    _email = f.email()
    db.contacts.insert({
        'cid':str(uuid.uuid4()),
        'name':f.name(),
        'address': f.address(),
        'phone': f.phone_number(),
        'location': str(f.latitude()) + ',' + str(f.longitude()),
        'email': _email,
        'img': 'https://secure.gravatar.com/avatar/' + hashlib.md5(_email).hexdigest() + '?s=100&d=identicon&r=g',
        'time': f.date_time()
    })


