from flask import Flask
from main.views import main
from config import DEBUG

app = Flask(__name__)
app.register_blueprint(main)
if __name__ == '__main__':
    app.run(debug=DEBUG)
