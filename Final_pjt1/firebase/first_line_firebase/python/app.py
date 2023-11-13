from flask import Flask, request, jsonify
# from google.cloud import firestore
import firebase_admin
from firebase_admin import db, credentials

app = Flask(__name__)

cred = credentials.Certificate('./ServiceAccountKey.json')
db = firebase_admin.initialize_app(cred)

def get_latest_data(collection_name):
    ref = db.reference(collection_name)
    # Get the latest document from the collection
    docs = ref.get()

    if docs[4].to_dict()['image'] != 'null':
        return 1
    else:
        return 0

@app.route('/getLatestData', methods=['GET'])
def get_data():
    result = get_latest_data('user')
    return jsonify({'result': result}), 200

@app.route('/', methods=['GET'])
log("hello_world started")
def hello_world():
log("hello_world finished")
    return 'hello world!'

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)

