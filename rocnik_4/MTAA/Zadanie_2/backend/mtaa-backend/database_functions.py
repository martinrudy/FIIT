from models import Recipe, recipe_items, fridge_items, Item
from database import engine, db_session


def add_item_to_recipe(recipe_id, item_id, item_count):
    con = engine.connect()
    con.execute(recipe_items.insert(), recipe_id=recipe_id, item_id=item_id, item_count=item_count)

def add_item_to_fridge(fridge_id, item_id, item_count):
    con = engine.connect()
    con.execute(fridge_items.insert(), fridge_id=fridge_id, item_id=item_id, item_count=item_count)

def update_fridge_item(fridge_id, item_id, value):
    con = engine.connect()
    con.execute(fridge_items.update().where(fridge_items.c.fridge_id==fridge_id).where(fridge_items.c.item_id==item_id).values(item_count=value))

def delete_fridge_item(fridge_id, item_id):
    con = engine.connect()
    con.execute(fridge_items.delete().where(fridge_items.c.fridge_id==fridge_id).where(fridge_items.c.item_id==item_id))

def add_item(title, category, file_path):
    item = Item(title, category, file_path)
    db_session.add(item)
    db_session.commit()

def add_recipe(title, text):
    recipe = Recipe(title, text)
    db_session.add(recipe)
    db_session.flush()
    db_session.refresh(recipe)
    db_session.commit()
    return recipe.id