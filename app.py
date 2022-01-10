from typing import Tuple

from flask import Flask, jsonify, request, Response, redirect, url_for
from werkzeug.utils import redirect
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.
    
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    # return create_response({"content": "hello world!"})
    return redirect(url_for('user',id='2'))


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)


# TODO: Implement the rest of the API here!

@app.route("/users")
def users():
    data = db.db_state
    return create_response(data)

@app.route("/users/<id>")
def user(id):
    incorrect_id = True
    data = db.db_state['users']
    for i in data:
        print(i)
        if str(i['id'])==id:
            incorrect_id = False
            data = {'users': i} 
            break  
             
    if not incorrect_id:
        return create_response(data)
    else:
        return create_response(status=404, message='id nao existe')


"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=81)
