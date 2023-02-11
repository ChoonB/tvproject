from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

with open("mongodb.txt", "r") as f:
    dburl = f.read()

from pymongo import MongoClient
client = MongoClient(dburl)
db = client.dbsparta

import requests
from bs4 import BeautifulSoup

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/post')
def post():
   return render_template('post.html')

@app.route('/board')
def board():
   return render_template('board.html')


@app.route("/drama", methods=["POST"])
def drama_post():
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')
    star_rank = soup.select_one(
        '#root > div > div.css-1xm32e0 > section > div > div.css-10ofaaw > div > section > div.css-1p7n6er-Pane.e1svyhwg15 > div > div > div > div > div.css-og1gu8-ContentRatings.e1svyhwg20')

    avg_rank = star_rank.text
    image = og_image['content']
    title = og_title['content'].rstrip(' - 왓챠피디아')
    description = og_description['content']

    doc = {
        'url':url_receive,
        'image':image,
        'title':title,
        'desc':description,
        'star':star_receive,
        'comment':comment_receive,
        'avg_star':avg_rank
    }

    db.drama.insert_one(doc)

    return jsonify({'msg':'드라마 등록 완료!'})

@app.route("/drama", methods=["GET"])
def drama_get():
    movies_list = list(db.drama.find({},{'_id':False}))
    return jsonify({'movies':movies_list})
# POST : 삭제 버튼 서버 구현
@app.route("/drama/delete", methods=["POST"])
def drama_delete():
    movies_receive = request.form["button_delete"]
    db.drama.delete_one({'title': movies_receive})
    return jsonify({'msg': '드라마 삭제 완료!'})

@app.route("/board/data", methods=["POST"])
def board_post():
    name_receive = request.form['name_give']
    bcomment_receive = request.form['bcomment_give']
    selected_receive = request.form['selected_give']

    doc = {
        'name': name_receive,
        'bcomment': bcomment_receive,
        'selected': selected_receive
    }

    db.board.insert_one(doc)

    return jsonify({'msg':'저장 완료!'})

@app.route("/board/data", methods=["GET"])
def board_get():
    board_list = list(db.board.find({}, {'_id': False}))
    main_list = list(db.drama.find({}, {'_id': False}))
    return jsonify({'board':board_list,'main':main_list})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)