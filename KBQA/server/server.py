# encoding=utf-8
import os
import sys

from flask import Flask, request, jsonify, render_template, redirect, url_for

PWD = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(PWD))
sys.path.insert(0, BASE)

from KBQA.kbqa_main import KBQAMain

app = Flask(__name__)

kbqa = KBQAMain()


@app.route('/search_books', methods=['GET'])
def search_books():
    return render_template('search.html')


@app.route('/search_books/m', methods=['GET'])
def search_books_mobile():
    return render_template('mobile.html')


@app.route('/get_books', methods=['POST'])
def get_books():
    user_data = request.json
    if not user_data.get("query"):
        return redirect(url_for("search_books"))
    else:
        kbqa.run(request=user_data)
        response = kbqa.response
    response = {"result": response}
    return jsonify(response)


@app.route('/get_books_table', methods=['POST'])
def get_books_table():
    user_data = request.form
    if not user_data.get("query"):
        return redirect(url_for("search_books"))
    else:
        kbqa.run(request=user_data)
        response = kbqa.response
        results = []
        # 没有url时指定为form表单
        no_url = """
        <form id="form_{id}" method="post" action="/get_books_table">
          <input type="hidden" name="query" value="{book_name}" /> 
          <U><a color="blue" onclick="document.getElementById('form_{id}').submit();">{book_name}</a></U>
        </form>
        """
        i = 0
        for book_similar in response:
            result = [["经名", "译者"]]
            for info in book_similar:
                if info.get("地址"):
                    url = '<a href="{}" target="_blank">{}</a>'.format(
                        info.get("地址", ""), info.get("经名", ""))
                else:
                    url = no_url.format(id=i, book_name=info.get("经名", ""))
                result.append(
                    [url, info.get("译者", "")]
                )
                i += 1
            results.append(result)
    return render_template('detail.html', results=results, title=user_data.get("query") or "result")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
