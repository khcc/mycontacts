from flask import Flask, jsonify, render_template, request, redirect, flash, session, get_flashed_messages
from mailer import Message, Mailer
from flask.ext.moment import Moment
import pymongo, re, uuid, time, hashlib, datetime, os

app = Flask(__name__)
moment = Moment(app)
db = pymongo.MongoClient().test_mycontacts

sender = Mailer(
    host = "smtp.gmail.com",
    port = 587,
    use_tls=True,
    usr = 'test-pycademy.workshop@gmail.com',
    pwd = '123456789',
)


@app.route('/')
def index():
    return render_template('index.html', contacts=db.contacts.find().sort([('time', -1)]))


@app.route('/contacts/', methods=['GET'])
def get_contacts():
    q = request.args.get('q', '')
    regex = re.compile(q.strip(), re.IGNORECASE)
    return render_template('index.html', contacts=db.contacts.find({
        '$or': [
            {'name':regex},
            {'address':regex},
            {'phone':regex},
            {'email':regex}
        ]}
    ))


@app.route('/contacts/<cid>', methods=['GET'])
def get_contact(cid):
    return jsonify(**db.contacts.find_one({'cid':cid}))


@app.route('/contacts/', methods=['POST'])
def add_contact():
    new_contact = request.form.to_dict()
    new_contact.setdefault('cid', str(uuid.uuid4()))
    new_contact['time'] = datetime.datetime.now()
    new_contact['img'] = 'https://secure.gravatar.com/avatar/' + hashlib.md5(new_contact['email']).hexdigest() + '?s=100&d=identicon&r=g'

    db.contacts.update(
        {'cid':new_contact['cid']},
        {'$set': new_contact},
        upsert = True
    )
    flash('You have created a new contact successfully')

    return redirect('/')


@app.route('/contacts/remove/<cid>')
def remove_contact(cid):
    name = db.contacts.find_one({'cid':cid})['name'].title()
    db.contacts.remove({'cid':cid})
    flash('You have removed %s successfully' % (name))
    return redirect('/')


@app.route('/email/<cid>')
def send_email(cid):
    contact = db.contacts.find_one({'cid':cid})
    if contact:
        msg = Message(
            To = contact['email'],
            Subject = "Hey " + contact['name'].title(),
            From = "MyContact",
            Html = """
                <h1>Hey Buddy</h1>
                I am happy now!
            """,
            Body = "Hey buddy\nI am happy now"
        )
        sender.send(msg)
        flash('You have poked ' + contact['name'] + ' successfully')
    else:
        flash('There is no contact with the given id')
    return redirect('/')


if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True)
