import cgi
import cgitb
cgitb.enable()

# https://docs.python.org/3/library/cgi.html

print("Content-Type: text/html")    # HTML is following
print()                             # blank line, end of headers

print("<head><TITLE>Login Submitted</TITLE></head>")
print ("<body>")
print("<H1>Welcome to the login page</H1>")
form = cgi.FieldStorage()
print("Username:", form["username"].value)
print("Password:", form["password"].value)
print("</body>")
