from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'dev'
  
if ENV == 'dev':
  app.debug = True  
  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1503548@localhost/postgres' 
else:
  app.debug = False
  app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
  __tablename__ = 'feedback'
  id = db.Column(db.Integer, primary_key=True)
  customer = db.Column(db.String(200), unique=True)
  server = db.Column(db.String(200))
  rating = db.Column(db.Integer)
  comments = db.Column(db.Text())

  def __init__(self, customer, server, rating, comments):
    self.customer = customer
    self.server = server
    self.rating = rating
    self.comments = comments

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
  if request.method == 'POST':
    customer = request.form['customer']
    server = request.form['server']
    rating = request.form['rating']
    comments = request.form['comments']
    #print(customer, server, rating, comments)
    if customer == '' or server == '':
      return render_template('index.html', message='Please enter required fields')
    if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
      data = Feedback(customer, server, rating, comments)
      db.session.add(data)
      db.session.commit()
      send_mail(customer, server, rating, comments)
      return render_template('success.html')
    return render_template('index.html', message='You have already submitted feedback')

if __name__ == '__main__':
    
    app.run()