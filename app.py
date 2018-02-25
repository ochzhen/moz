from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/documents')
def documents_list():
    return render_template('documents_list.html')

@app.route('/documents/<int:id>')
def view_document(id):
    return render_template('document.html')

if __name__ == '__main__':
    app.run(debug=True)
