import os
from crypt import methods
import re
from urllib import response
from flask import (
    Flask,
    request,
    jsonify,
    Response,
    send_from_directory,
    flash,
    redirect,
    url_for,
)
from werkzeug.utils import secure_filename
from database import db_session, init_db, engine
import testweb

from models import (
    User,
    Recipe,
    Fridge,
    recipe_items,
    Item,
    fridge_items,
)
from database_functions import (
    add_item_to_recipe,
    add_item_to_fridge,
    delete_fridge_item,
    update_fridge_item,
    delete_fridge_item,
    add_item,
    add_recipe,
)
from sqlalchemy import and_

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.abspath(UPLOAD_FOLDER)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter(
        User.email == data["email"], User.password == data["password"]
    ).first()
    if user:
        fridges = Fridge.query.filter(Fridge.user_id == user.id).all()
        for fridge in fridges:
            if fridge.in_use:
                fridge_dict = {"id": fridge.id, "name": fridge.name}
        user_json = {
            "email": user.email,
            "name": user.name,
            "id": user.id,
            "fridge": fridge_dict,
        }
        return jsonify(user_json)
    else:
        return Response(status=404)


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    user = User.query.filter(User.email == data["email"]).first()
    if user:
        return Response(status=409)
    else:
        u = User(data["name"], data["email"], data["password"])
        db_session.add(u)
        db_session.commit()
        fridge = Fridge(data["fridge_name"], u.id, True)
        db_session.add(fridge)
        db_session.commit()
        response_json = {"fridge_id": fridge.id}
        return jsonify(response_json), 201


@app.route("/refrigerator/<uuid>/recipes", methods=["GET"])
def get_recipes(uuid):
    recipes_dict = []
    recipes = Recipe.query.all()
    for recipe in recipes:
        items = []
        con = engine.connect()
        recipe_refs = con.execute(
            recipe_items.select(recipe_items.c.recipe_id == recipe.id)
        )
        for recipe_ref in recipe_refs:
            items_refs = con.execute(
                fridge_items.select().where(
                    and_(
                        fridge_items.c.item_id == recipe_ref.item_id,
                        fridge_items.c.item_count >= recipe_ref.item_count,
                        fridge_items.c.fridge_id == int(uuid)
                    )
                )
            ).first()
            if items_refs == None:
                items = []
                break
            item_act = Item.query.filter(Item.id == recipe_ref["item_id"]).first()
            item = {"id": items_refs["item_id"], "item_count": recipe_ref["item_count"], "title": item_act.title}
            items.append(item)
        if len(items) <= 0:
            continue
        recipe_json = {"id": recipe.id, "title": recipe.title, "text": recipe.text, "items": items}
        recipes_dict.append(recipe_json)

    return jsonify(recipes_dict)


@app.route("/refrigerator/<uuid>/food", methods=["GET"])
def get_fridge_items(uuid):
    items_dict = []
    con = engine.connect()
    references_to_items = con.execute(
        fridge_items.select(fridge_items.c.fridge_id == uuid)
    )
    for reference in references_to_items:
        item = Item.query.filter(Item.id == reference["item_id"]).first()
        item_dict = {
            "foodType_id": item.id,
            "title": item.title,
            "category": item.category,
            "item_count": reference.item_count,
        }
        items_dict.append(item_dict)
    sort_items = sorted(items_dict, key=lambda x: x["foodType_id"], reverse=True)
    return jsonify(sort_items)


@app.route("/refrigerator/<uuid>/food", methods=["POST"])
def add_fridge_item(uuid):
    data = request.json
    if not data:
        return Response(status=400)
    con = engine.connect()
    fridge = Fridge.query.filter(Fridge.id == uuid).first()
    if fridge == None:
        return Response(status=400)
    item = con.execute(
        fridge_items.select().where(
            and_(
                fridge_items.c.fridge_id == uuid,
                fridge_items.c.item_id == data["item_id"],
            )
        )
    ).first()
    food_type = Item.query.filter(Item.id == data["item_id"]).first()
    if food_type == None:
        return Response(status=400)
    if item:
        return Response(status=409)
    else:
        add_item_to_fridge(uuid, data["item_id"], data["item_count"])
        return Response(status=201)


@app.route("/refrigerator/<fridge_uuid>/food/<food_uuid>", methods=["PUT"])
def modify_fridge_item(fridge_uuid, food_uuid):
    data = request.json
    update_fridge_item(fridge_uuid, food_uuid, data["item_count"])
    return Response(status=204)


@app.route("/user/<uuid>/refrigerator/<uuid_fridge>", methods=["PATCH"])
def set_fridge_use(uuid, uuid_fridge):
    fridges = Fridge.query.filter(Fridge.user_id == uuid).all()
    for fridge in fridges:
        if int(fridge.id) == int(uuid_fridge):
            fridge.in_use = True
        elif fridge.in_use:
            fridge.in_use = False

    db_session.commit()

    return Response(status=200)


@app.route("/refrigerator/<fridge_uuid>/food/<food_uuid>", methods=["DELETE"])
def extract_fridge_item(fridge_uuid, food_uuid):
    delete_fridge_item(fridge_uuid, food_uuid)
    return Response(status=204)


@app.route("/users/<uuid>/refrigerators", methods=["POST"])
def add_user_fridge(uuid):
    data = request.json
    if data == None:
        return Response(status=400)
    user = User.query.filter(User.id == uuid).first()
    if user == None:
        return Response(status=400)
    fridge = Fridge.query.filter(
        Fridge.name == data["name"], Fridge.user_id == uuid
    ).first()
    if fridge != None:
        return Response(status=409)
    else:
        fridge = Fridge(data["name"], uuid, False)
        db_session.add(fridge)
        db_session.commit()
        return Response(status=201)


@app.route("/refrigerators/<uuid>", methods=["DELETE"])
def delete_user_fridge(uuid):
    fridge = Fridge.query.filter(Fridge.id == uuid).first()
    if fridge == None:
        return Response(status=409)
    else:
        db_session.delete(fridge)
        db_session.commit()
        return Response(status=204)


@app.route("/users/<uuid>/refrigerators", methods=["GET"])
def get_user_fridges(uuid):
    fridges = Fridge.query.filter(Fridge.user_id == uuid).all()
    json_fridges = []
    for fridge in fridges:
        json_fridge = {
            "id": fridge.id,
            "name": fridge.name,
            "user_id": fridge.user_id,
            "in_use": fridge.in_use,
        }
        json_fridges.append(json_fridge)
    return jsonify(json_fridges)


@app.route("/foodTypes", methods=["GET"])
def get_food_types():
    items = Item.query.all()
    json_items = []
    for item in items:
        json_item = {
            "id": item.id,
            "title": item.title,
            "category": item.category,
            "file_path": item.file_path,
        }
        json_items.append(json_item)
    return jsonify(json_items)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/uploads", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            data = request.form.to_dict()
            filename = secure_filename(file.filename)
            string_path = UPLOAD_FOLDER + "/" + filename
            add_item(data["title"], data["category"], string_path)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return Response(status=201)
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    """


@app.route("/uploads/<name>")
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route("/recipes", methods=["POST"])
def add_recipe_endpoint():
    data = request.json
    recipe_id = add_recipe(data["title"], data["text"])
    for item in data["items"]:
        add_item_to_recipe(recipe_id, item["id"], item["item_count"])

    return Response(status=201)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    init_db()
    app.run(port=5000, host="0.0.0.0")

