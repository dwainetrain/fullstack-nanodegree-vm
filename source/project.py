from flask import Flask
from flask import request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def homePage():
    restaurants = session.query(Restaurant).all()
    output =''
    output = '<ul>'
    for restaurant in restaurants:
        output += '<li>'
        output += '<a href="/restaurants/%s/">' %restaurant.id 
        output += restaurant.name
        output += '</a>'
        output += '</li>'
    output += '</ul>'
    return output

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    output = ''
    for i in items:
        output += i.name
        output += '</br>'
        output += i.price
        output += '</br>'
        output += i.description
        output += '</br>'
        output += '<a href="/restaurant/%s/%s/edit">Edit</a>' % (restaurant_id, i.id)
        output += '</br>'
        output += '<a href="/restaurant/%s/%s/delete">Delete</a>' % (restaurant_id, i.id)
        output += '</br></br>'
    output += '<a href="/restaurant/%s/add">Add new menu item</a>' %restaurant_id
    return output

# Create functions to newMenuItem, editMenuItem and deleteMenuItem...

@app.route('/restaurant/<int:restaurant_id>/add', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    output = ''
    output += "<html><body><p>Task 1 Complete!"
    # Ah, handcoding something you didn't need to handcode.
    #I'll clean this up in a bit
    # if request.method == 'POST':
    #     name = request.form['name']
    #     description = request.form['description']
    #     price = request.form['price']
    #     # Below is 'mapping' the object so you can add it to the database
    #     new_menu_item = MenuItem(
    #         name=name, description=description, 
    #         price=price, restaurant_id=restaurant_id
    #         )
    #     session.add(new_menu_item)
    #     session.commit()

    #     output += "<h3> You've added the following new Menu item to %s</h3><br />" %restaurant.name
    #     output += '<strong>' + name + '</strong>'
    #     output += '</br>'
    #     output += description
    #     output += '</br>'
    #     output += price
    #     output += '</br>'

    # else:
       
    #     output += "<h1>Add a New Menu Item to %s</h1>" %restaurant.name
    #     output += "<form method='POST' enctype='multipart/form-data' action='/add-menu-item/%s'>" %restaurant.id
    #     output += "<h2>Please enter the new menu item info below:</h2>" 

    #     output += "<input name='name' type='text' ><br />"
    #     output += "<input name='description' type='text' ><br />"
    #     output += "<input name='price' type='text'><br />"
    #     output += "<input type='submit' value='submit'> </form>"

    output += "</body></html>"
    return output

@app.route('/restaurant/<int:restaurant_id>/<int:menuItem_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menuItem_id):
    menuItem = session.query(MenuItem).filter_by(id = menuItem_id).one()
    output = ''
    output += "<html><body><p>Task 2 Complete!</p>"
    # if request.method == 'POST':
    #     output = ''
    #     output += 'Edit the menu item here'
    #     output += '</br>'
    #     output += menuItem.name
    #     output += '</br>'
    #     output += menuItem.description
    #     output += '</br>'
    #     output += menuItem.price
    #     output += '</br>'

    #     name = request.form['name']
    #     description = request.form['description']
    #     price = request.form['price']
    #     # Below is 'mapping' the object so you can add it to the database
    #     update_menu_item = MenuItem(
    #         name=name, description=description, 
    #         price=price, id=menuItem_id
    #         )
    #     session.add(update_menu_item)
    #     session.commit()

    #     output += "<h3> You've updated the following Menu item</h3><br />"
    #     output += '<strong>' + name + '</strong>'
    #     output += '</br>'
    #     output += description
    #     output += '</br>'
    #     output += price
    #     output += '</br>'

    # else:
    #     output = ''
    #     output += 'Edit the menu item here'
    #     output += '</br>'
    #     output += menuItem.name
    #     output += '</br>'
    #     output += menuItem.description
    #     output += '</br>'
    #     output += menuItem.price
    #     output += '</br>'

    #     output += "<h1>Edit a Menu Item</h1>"
    #     output += "<form method='POST' enctype='multipart/form-data' action='/edit-menu-item/%s'>" %menuItem.id
    #     output += "<h2>Please update the menu item info below:</h2>" 

    #     output += "Name: <input name='name' type='text' ><br />"
    #     output += "Description: <input name='description' type='text' ><br />"
    #     output += "Price: <input name='price' type='text'><br />"
    #     output += "<input type='submit' value='submit'> </form>"

    output += "</body></html>"
    return output

@app.route('/restaurant/<int:restaurant_id>/<int:menuItem_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menuItem_id):
    menuItem = session.query(MenuItem).filter_by(id = menuItem_id).one()
    output = ''
    output += "<html><body><p>Task 3 Complete!</p>"

    output += "</body></html>"
    return output


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)