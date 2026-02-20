from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random


app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)
    
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}



with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random", methods=["GET"])
def get_random_cafe():
    cafes = db.session.execute(db.select(Cafe)).scalars().all()

    if not cafes:
        return jsonify(error="No cafes found"), 404

    random_cafe = random.choice(cafes)
    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all")
def get_all_cafes():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    #This uses a List Comprehension but you could also split it into 3 lines.
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


@app.route("/search")
def get_cafe_at_location():
    query_location = request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    # Note, this may get more than one cafe per location
    all_cafes = result.scalars().all()
    if all_cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404

# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def post_new_cafe():
    new_cafe = Cafe(
    name=request.form.get("name"),
    map_url=request.form.get("map_url"),
    img_url=request.form.get("img_url"),
    location=request.form.get("location"),
    seats=request.form.get("seats"),
    has_toilet=bool(request.form.get("has_toilet")),
    has_wifi=bool(request.form.get("has_wifi")),
    has_sockets=bool(request.form.get("has_sockets")),
    can_take_calls=bool(request.form.get("can_take_calls")),
    coffee_price=request.form.get("coffee_price"),
)

    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    # Step 2: Get the new price from request args
    new_price = request.args.get("new_price")
    
    if not new_price:
        return jsonify(error="Missing new_price parameter"), 400  # Bad Request if no price provided
    
    # Step 3: Fetch cafe by ID
    cafe = db.session.get(Cafe, cafe_id)
    
    if not cafe:
        return jsonify(error="Cafe not found"), 404  # Resource not found
    
    # Step 4: Update the field and commit
    cafe.coffee_price = new_price
    db.session.commit()
    
    # Step 5: Return a success message
    return jsonify(success=f"Cafe id {cafe_id} price updated to {new_price}"), 200

# HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    # Step 1: Check API key
    api_key = request.args.get("api-key")
    if api_key != "TopSecretAPIKey":
            return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403
    
    # Step 2: Fetch cafe by ID
    cafe = db.session.get(Cafe, cafe_id)
    if not cafe:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
            
    # Step 3: Delete cafe and commit
    db.session.delete(cafe)
    db.session.commit()
    
    # Step 4: Return success message
    return jsonify(success=f"Cafe id {cafe_id} successfully deleted"), 200

    
    
if __name__ == '__main__':
    app.run(debug=True)