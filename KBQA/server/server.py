# encoding=utf-8
import os
import sys

from flask import Flask, request, jsonify, render_template

PWD = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(PWD))
sys.path.insert(0, BASE)

from KBQA.kbqa_main import KBQAMain

app = Flask(__name__)

kbqa = KBQAMain()


@app.route('/search_books', methods=['GET'])
def search_books():
    return render_template('search.html')


@app.route('/get_books', methods=['POST'])
def get_books():
    user_data = request.json
    if not user_data.get("query"):
        response = {"info": "请指定query"}
    else:
        kbqa.run(request=user_data)
        response = kbqa.response
    response = {"result": response}
    return jsonify(response)


@app.route('/get_books_table', methods=['POST'])
def get_books_table():
    user_data = request.form
    if not user_data.get("query"):
        result = []
    else:
        kbqa.run(request=user_data)
        response = kbqa.response
        result = [["经名", "译者"]]
        # 变成二维列表
        for info in response:
            url = '<a href="{}" target="_blank">{}</a>'.format(
                info.get("地址", ""), info.get("经名", ""))
            result.append(
                [url, info.get("译者", "")]
            )
    return render_template('detail.html', result=result, title=user_data.get("query") or "result")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
