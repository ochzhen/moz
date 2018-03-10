import sys
from moz import app
from config import DEBUG


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    app.run(debug=DEBUG)
