import cgi
import cgitb
cgitb.enable()

# https://docs.python.org/3/library/cgi.html

print("Content-Type: text/html")    # HTML is following
print()                             # blank line, end of headers

print("<head><TITLE>Fitness Login Submitted</TITLE></head>")
print ("<body>")
print("<H1>Welcome to the Fitness page</H1>")
form = cgi.FieldStorage()
username = form["username"].value
password = form["password"].value
print("Username:", form["username"].value)
print("Password:", form["password"].value)

passwordRev = password[::-1]

if (username == passwordRev):
    print("<p>Login Succeeded")
else:
    print("<p>Invalid username/password")

print("<p><a href=\"/\"/> click here to go back</a>")

print("</body>")
