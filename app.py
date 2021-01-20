from flask import Flask, render_template, request

app = Flask(__name__)

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
    return render_template('success.html')

if __name__ == '__main__':
    app.debug = True
    app.run()