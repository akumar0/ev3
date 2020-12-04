from flask import Flask, render_template, session, redirect, url_for, request
from markupsafe import escape

app = Flask(__name__)    

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]//'
 
@app.route('/home')
def home():
  return render_template('login.html')

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <html><body>
        <form method="post">
            <p>Username: <input type=text name=username>
            <p><input type=submit value=Login>
        </form>
        </body></html>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))  
 
if __name__ == '__main__':
  app.run(debug=True)
  