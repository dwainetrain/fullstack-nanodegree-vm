import cgi
from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Connect to the database and start a session
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# Can't get this working in Python 3
# Get weird path errors
# 404's when I send the submit...
# 

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:

            if self.path.endswith("/restaurants"):
                query = session.query(Restaurant).all()

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                output = ""
                output += '<html><body><p><a href="/restaurants/add">Add a new Restaurant</a></p><ul>'
                for entry in query:
                    output += '<li> %s </br>' % entry.name
                    output += '<p><a href="/restaurants/%s/edit">Edit</a></br>' % entry.id
                    output += '<a href="restaurants/%s/delete">Delete</a></p></li>' % entry.id
                output += "</body></html>"
                self.wfile.write(bytes(output, 'UTF-8')) 
                return
            
            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if myRestaurantQuery:
                    print (myRestaurantQuery)
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    # So, create the form here?
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Edit the Restaurant Name</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action='restaurants/%s/edit'>" %restaurantIDPath
                    output += "<h2>Please edit the Restaurant's name below:</h2>"
                    output += "<input name='restaurantEdit' type='text' >"
                    output += "<input type='submit' value='Submit'> </form>"
                    output += "</body></html>"
                    self.wfile.write(bytes(output, 'UTF-8'))
                    return
            # Get
            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    # So, create the form here?
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Edit the Restaurant Name</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action='restaurants/%s/delete'>" %restaurantIDPath
                    output += "<h2>Are you sure want to delete this restaurant?</h2>"
                    output += "<input type='submit' value='Delete'> </form>"
                    output += "</body></html>"
                    self.wfile.write(bytes(output, 'UTF-8'))
                    return

            if self.path.endswith("/restaurants/add"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                # So, create the form here?
                output = ""
                output += "<html><body>"
                output += "<h1>Add a New Restaurant</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/add'><h2>Please enter the new restaurant name below:</h2>"
                output += "<input name='restaurant' type='text' >"
                output += "<input type='submit' value='submit'> </form>"
                output += "</body></html>"
                self.wfile.write(bytes(output, 'utf-8'))
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)
    
    def do_POST(self):
        if self.path.endswith("/restaurants/add"):
            ctype, pdict = cgi.parse_header(
                self.headers['content-type'])
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                restaurant_name = fields.get('restaurant')

                newRestaurant = Restaurant(name=restaurant_name[0])
                session.add(newRestaurant)
                session.commit()
                
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants') # HTTP Header information needed for redirect
                self.end_headers()

        # Post
        if self.path.endswith("/edit"):
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                restaurant_edit = fields.get('restaurantEdit')
                restaurantIDPath = self.path.split("/")[2]

            myRestaurantQuery = session.query(Restaurant).filter_by(
                id=restaurantIDPath).one()
            if myRestaurantQuery != []:
                myRestaurantQuery.name = restaurant_edit[0]
                session.add(myRestaurantQuery)
                session.commit()
                
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants') # HTTP Header information needed for redirect
                self.end_headers()

        if self.path.endswith("/delete"):
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                # restaurant_edit = fields.get('restaurantEdit')
                restaurantIDPath = self.path.split("/")[2]

            myRestaurantQuery = session.query(Restaurant).filter_by(
                id=restaurantIDPath).one()
            if myRestaurantQuery != []:
                # myRestaurantQuery.name = restaurant_edit[0]
                session.delete(myRestaurantQuery)
                session.commit()
                
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants') # HTTP Header information needed for redirect
                self.end_headers()

        # except:
        #     self.send_error(404, "File Not Found %s" % self.path)

def main():
    try:
        port = 8080
        server = HTTPServer(('',port), WebServerHandler)
        print ("Web server running on http://localhost:%s" % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print ("^C entered, stopping web server...")
        server.socket.close()

if __name__ == '__main__':
    main()