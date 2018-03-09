from flask import Flask

from config import DEBUG
from main.init import init_app

if __name__ == '__main__':
    app = Flask(__name__)
    app = init_app(app)
    app.run(debug=DEBUG)
