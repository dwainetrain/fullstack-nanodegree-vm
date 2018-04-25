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
        output += '<strong>' + i.name + '</strong>'
        output += '</br>'
        output += i.price
        output += '</br>'
        output += i.description
        output += '</br>'
    output += '<a href="/add-menu-item/%s">Add new menu item</a>' %restaurant_id
    return output

# Create functions to newMenuItem, editMenuItem and deleteMenuItem...

@app.route('/add-menu-item/<int:restaurant_id>', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    output = ''
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        # Below is 'mapping' the object so you can add it to the database
        new_menu_item = MenuItem(
            name=name, description=description, 
            price=price, restaurant_id=restaurant_id
            )
        session.add(new_menu_item)
        session.commit()

        output += "You've added the following new Menu item to %s" %restaurant.name
        output += '<strong>' + name + '</strong>'
        output += '</br>'
        output += description
        output += '</br>'
        output += price
        output += '</br>'

    else:
        output += "<html><body>"
        output += "<h1>Add a New Menu Item to %s</h1>" %restaurant.name
        output += "<form method='POST' enctype='multipart/form-data' action='/add-menu-item/%s'>" %restaurant.id
        output += "<h2>Please enter the new menu item info below:</h2>" 

        output += "<input name='name' type='text' ><br />"
        output += "<input name='description' type='text' ><br />"
        output += "<input name='price' type='text'><br />"
        output += "<input type='submit' value='submit'> </form>"
        output += "</body></html>"
    return output

@app.route('/add-menu-item/<int:restaurant_id>', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    output = ''



if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)