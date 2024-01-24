from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nomads.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.app_context().push()

db = SQLAlchemy(app)

class Nomads(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(20), nullable = False)
    completed = db.Column(db.Integer, default = 0)
    nickname = db.Column(db.String(20), nullable = False)
    created = db.Column(db.DateTime, default = datetime.utcnow)
    country = db.Column(db.String)

    def __repr__(self):
        return repr((self.user_name, self.nickname, self.country)) 
    
with open('data/countries.txt', 'r') as file: country_list = file.read().split('\n')

@app.route('/', methods =['POST', 'GET'])
def split():
    if request.method == 'POST' and 'login' in request.form:
        return redirect('/login')
    elif request.method == 'POST':
        return redirect('/signup')
    else:
        return render_template('split.html')


@app.route('/login', methods =['POST', 'GET'])
def flaskwall():
    
    if request.method == 'POST':
        users = Nomads.query.order_by(Nomads.id).all()
        User_name = request.form['user_name'] #new
        for user in users:
            if User_name in user.user_name:
                if request.form['nickname'] == user.nickname:
                    return redirect(f'/index/{user.id}')
                else:
                    return render_template('login.html', message = 'Wrong Password')
                
        return render_template('login.html', message = 'Unkown User')
         
    else:
        return render_template('login.html')


@app.route('/signup', methods =['POST', 'GET'])
def SIGNUP():  
    if request.method == 'POST':
        users = Nomads.query.order_by(Nomads.id).all()
        print(users)
        User_name = request.form['user_name'] #new
        for user in users:
            if User_name == user.user_name:
                request.method = 'GET'
                return render_template('signup.html', message = 'User already exists', country_list = country_list)
        else:
            Nickname = request.form['nickname']
            Country = request.form['country']
            new_user = Nomads(user_name = User_name, nickname = Nickname, country = Country)
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect(f'/index/{new_user.id}')
            except:
                return 'Error with signing up'

    else:
        return render_template('signup.html', country_list = country_list)
    

@app.route('/index/<int:id>')
def index(id):
    Country = Nomads.query.get_or_404(id).country.replace(' ', '_')
    print(Country)
    return render_template('index.html', country = Country)  


if __name__ == "__main__":
    app.run(debug=True)