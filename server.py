from flask import Flask, request, redirect, url_for

from xda_feed import get_latest_json

app = Flask(__name__)


@app.route('/xda-feed/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        input_text = request.form['input']
        if input_text == '' or not input_text.isnumeric():
            return redirect(url_for('form'))
        else:
            return redirect(url_for('hello', thread_id=input_text))
    return '''
        <form method="post">
            <p><input type=text name=input>
            <p><input type=submit value=Go>
        </form>
    '''


@app.route('/xda-feeds/<thread_id>/')
def hello(thread_id):
    output = get_latest_json(thread_id)
    if output is not None:
        return output
    else:
        return 'Error'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
