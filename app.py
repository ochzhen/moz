from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/email-confirmation')
def email_confirmation():
    return ''

@app.route('/documents/<int:id>')
def view_document(id):
    return str(id);

if __name__ == '__main__':
    app.run(debug=True)
