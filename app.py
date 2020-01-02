from flask import Flask, request, Response, render_template, url_for, redirect
import web_app

user_list = set()
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
last = ""

@app.route('/user', methods=['POST'])
def pick_user():
    global last
    option = request.form['option'].split(" ")[-1]
    message = "User added " + option
    user_list.add(option)
    last = option
    return redirect(url_for('index', success=message))

@app.route('/delete', methods=['POST'])
def delete():
    global last
    user = request.form['delete']
    message = "User deleted " + user
    user_list.discard(user)
    last = ""
    return redirect(url_for('index', success=message))

@app.route('/', methods=[ 'GET', "POST"])
def index():
    if request.method == "POST":
        request.files['image'].save("./current.jpg")
        options = web_app.start()
        if options == "no_text":
            return "no_text"
        return "/?options=" + str(options)
    if request.method == "GET":
        manual = request.args.get('manual')
        if manual:
            options = web_app.get_names(manual)
        else:
            options = request.args.get('options')
        if options != None:
            options = str(options).replace("'", "").replace("(","").replace(")","")
            options = options.strip("[]").split(", ")
        return render_template('getImage.html', options=options, success=request.args.get('success'), current_list=user_list,last=last)

if __name__ == '__main__':
    app.run(debug=True)
