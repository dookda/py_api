from flask import Flask
from api import api
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.register_blueprint(api, url_prefix='/api')


@app.route("/")
def service():
    return "Service is running!"


if __name__ == "__main__":
    app.run()


# run server
# flask run
