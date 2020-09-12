from flask import Flask, request, jsonify

from KBQA.kbqa_main import KBQAMain


app = Flask(__name__)

kbqa = KBQAMain()


@app.route('/get_books', methods=['POST'])
def get_books():
    user_data = request.json
    if not user_data.get("query"):
        response = {"info": "请指定query"}
    else:
        kbqa.run(request=user_data)
        response = kbqa.response
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=55555)
