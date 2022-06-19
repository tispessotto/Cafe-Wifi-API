from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from random import choice

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


@app.route("/")
def home():
    all_cafes_list = []
    for i in Cafe.query.all():
        cafe = i.to_dict()
        all_cafes_list.append(cafe)
    return render_template("index.html", cafes=all_cafes_list)


@app.route("/random")
def random():
    cafes = db.session.query(Cafe).all()
    random_cafe = choice(cafes)
    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all")
def all_cafes():
    all_cafes_list = []
    for i in Cafe.query.all():
        cafe = i.to_dict()
        all_cafes_list.append(cafe)
    return jsonify(cafe=all_cafes_list)


@app.route("/search")
def get_cafe_at_location():
    query_location = request.args.get("loc")
    cafe = db.session.query(Cafe).filter_by(location=query_location).first()
    if cafe:
        return jsonify(cafe=cafe.to_dict())
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})


@app.route("/add", methods=["GET", "POST"])
def add():
    def get_boolean(value):
        positive_list = ["yes", "1", "true"]
        negative_list = ["no", "0", "false"]
        if value in positive_list:
            return True
        elif value in negative_list:
            return False

    new_name = request.args.get("name")
    new_loc = request.args.get("location")
    new_map_url = request.args.get("map_url")
    new_img_url = request.args.get("img_url")
    new_seats = request.args.get("seats")
    new_coffee_price = request.args.get("coffee_price")

    new_has_toilet = get_boolean(request.args.get("has_toilet").lower())
    new_has_wifi = get_boolean(request.args.get("has_wifi").lower())
    new_has_sockets = get_boolean(request.args.get("has_sockets").lower())
    new_can_take_calls = get_boolean(request.args.get("can_take_calls").lower())

    new_cafe = Cafe(name=new_name, location=new_loc, map_url=new_map_url, img_url=new_img_url, seats=new_seats,
                    has_toilet=new_has_toilet, has_wifi=new_has_wifi, has_sockets=new_has_sockets,
                    can_take_calls=new_can_take_calls, coffee_price=new_coffee_price)
    db.session.add(new_cafe)
    db.session.commit()

    return jsonify(response={"Success": "You did it."})


@app.route("/update-price/<int:cafe_id>", methods=["GET", "PATCH"])
def update_price(cafe_id):
    try:
        cafe_to_update = Cafe.query.get(cafe_id)
        updated_price = request.args.get("new_price")
        cafe_to_update.coffee_price = updated_price
        db.session.commit()
        message = {"Success": "Price successfully updated."}
        return jsonify(response=message)
    except AttributeError:
        error = {"Error": "We couldn't find a cafe with this ID."}
        return jsonify(response=error)


@app.route("/report-closed/<int:cafe_id>", methods=["GET", "DELETE"])
def delete(cafe_id):
    api_key = request.args.get("api-key")
    try:
        cafe_to_delete = Cafe.query.get(cafe_id)
        if api_key == "TopSecretAPIKey":
            db.session.delete(cafe_to_delete)
            db.session.commit()
            success = {"Success": "Cafe deleted with success."}
            return jsonify(response=success)
        else:
            fail = {"Fail": "You don't have access to delete data."}
            return jsonify(response=fail)
    except:
        error = {"Error": "We couldn't find a cafe with this ID."}
        return jsonify(response=error)


if __name__ == '__main__':
    app.run(debug=True)
