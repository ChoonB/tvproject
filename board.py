from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

with open("mongodb.txt", "r") as f:
    dburl = f.read()

from pymongo import MongoClient
client = MongoClient(dburl)
db = client.dbsparta


@app.route('/')
def home():
   return render_template('board.html')

@app.route("/homework", methods=["POST"])
def homework_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    selected_receive = request.form['selected_give']

    doc = {
        'name': name_receive,
        'comment': comment_receive,
        'selected': selected_receive
    }

    db.hw.insert_one(doc)

    return jsonify({'msg':'저장 완료!'})

@app.route("/homework", methods=["GET"])
def homework_get():
    homework_list = list(db.hw.find({}, {'_id': False}))
    main_list = list(db.main.find({}, {'_id': False}))
    return jsonify({'homework':homework_list,'main':main_list})



if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)





