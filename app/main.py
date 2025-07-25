
from flask import Flask, abort, jsonify, redirect, request
from werkzeug.exceptions import HTTPException
from app.models import store
from app.routes import bp
from app.utils import generate_short_code, validate_url

app = Flask(__name__)

app.register_blueprint(bp)


@app.errorhandler(HTTPException)
def handle_http_exception(e):
    
    response = e.get_response()
    response.data = jsonify({
        "error": e.name,
        "message": e.description,
    }).data
    response.content_type = "application/json"
    return response, e.code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)