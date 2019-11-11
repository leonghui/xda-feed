from flask import Flask, request, jsonify
from requests import exceptions

from xda_feed import get_latest_posts

app = Flask(__name__)


@app.route('/', methods=['GET'])
def form():
    thread_id = request.args.get('thread_id')
    usernames = request.args.get('usernames')

    if thread_id is None:
        return 'Please provide value for thread_id'

    if not thread_id.isnumeric():
        return 'Invalid thread_id'

    username_list = []

    if usernames is not None:
        assert isinstance(usernames, str)
        username_list = usernames.split(',')

    try:
        output = get_latest_posts( thread_id, username_list)
        return jsonify(output)
    except exceptions.RequestException:
        return f"Error generating output for thread {thread_id}."


if __name__ == '__main__':
    app.run(host='0.0.0.0')
