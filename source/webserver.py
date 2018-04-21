import cgi
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Connect to the database and start a session
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

## You still have a way to go to understand this...don't give up
## here's some hints, action back to '/restaurants/add'
## For Post, don't forget you need to get the first element in the
## returned content
## use 301 to redirect at the end...

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # if self.path.endswith("/hello"):
            #     self.send_response(200)
            #     self.send_header('Content-type', 'text/html')
            #     self.end_headers()

            #     output = ""
            #     output += "<html><body>"
            #     output += "<h1>Hello!</h1>"
            #     output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            #     output += "</body></html>"
            #     self.wfile.write(output)
            #     print (output)
            #     return
            
            # if self.path.endswith("/hola"):
            #     self.send_response(200)
            #     self.send_header('Content-type', 'text/html')
            #     self.end_headers()

            #     output = ""
            #     output += "<html><body>&#16Hola<a href= '/hello'>Back to Hello</a></body></html>"
            #     self.wfile.write(output)
            #     print (output)
            #     return

            # Ok, so the challenge for edit is to get the restaurants id...

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
                    output += '<a href="/delete">Delete</a></p></li>' 
                output += "</body></html>"
                self.wfile.write(output)
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
                    self.wfile.write(output)
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
                output += "<input type='submit' value='Submit'> </form>"
                output += "</body></html>"
                self.wfile.write(output)
                return


            if self.path.endswith("/delete"):
                # Try a 'are you sure you want to delete *Restaurant name*
                pass
            



        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)
    
    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/add"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
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


            # output = ""
            # output += "<html><body>"
            # output += " <h2> Okay, how about this: </h2>"
            # output += "<h1> %s </h1>" % restaurant_name[0]
            # output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants'><h2>What would you like me to say?</h2><input name="restaurant" type="text" ><input type="submit" value="Submit"> </form>'''
            # output += "</body></html>"
            # self.wfile.write(output)
            # print(output)

        except:
            self.send_error(404, "File Not Found %s" % self.path)


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