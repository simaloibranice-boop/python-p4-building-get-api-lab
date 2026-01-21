#!/usr/bin/env python3

from flask import Flask, make_response, jsonify

try:
    from flask_migrate import Migrate
except ModuleNotFoundError:
    Migrate = None

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

if Migrate:
    migrate = Migrate(app, db)

db.init_app(app)

with app.app_context():
    db.create_all()

    if not Bakery.query.first():
        default_bakery = Bakery(name='Default Bakery')
        db.session.add(default_bakery)
        db.session.commit()
    else:
        default_bakery = Bakery.query.first()

    if not BakedGood.query.first():
        default_goods = [
            BakedGood(name='Sample Pastry', price=1.50, bakery=default_bakery),
            BakedGood(name='Sample Cake', price=2.50, bakery=default_bakery),
        ]
        db.session.add_all(default_goods)
        db.session.commit()

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakeries_list = [bakery.to_dict() for bakery in bakeries]
    return make_response(jsonify(bakeries_list), 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    return make_response(jsonify(bakery.to_dict()), 200)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_list = [baked_good.to_dict() for baked_good in baked_goods]
    return make_response(jsonify(baked_goods_list), 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    return make_response(jsonify(baked_good.to_dict()), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
