from flask import Flask, render_template, request, redirect, url_for, session
import db, string, random
from datetime import timedelta

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=255))

@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')
    
    if msg == None:
        return render_template('index.html')
    else:
        return render_template('index.html', msg=msg)
    
    return render_template('index.html')

@app.route('/', methods=['POST'])
def login():
    user_name = request.form.get('username')
    password = request.form.get('password')
    
    if db.login(user_name, password):
        session['user'] = True
        return redirect(url_for('mypage'))
        session.premanent = True
        app.permanent_session_lifetime = timedelta(minutes=1)
    else:
       error = 'ログインに失敗しました'
       input_data = {
           'user_name' : user_name,
           'password' : password,
       }
       return render_template('index.html', error=error, data=input_data)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/mypage', methods=['GET'])
def mypage():
    if 'user' in session:
        return render_template('mypage.html')
    else:
        return redirect(url_for('index'))

@app.route('/register')
def register_form():
    return render_template('register.html')

@app.route('/register_exe', methods=['POST'])
def register_exe():
    user_name = request.form.get('user_name')
    password = request.form.get('password')
    
    
    if user_name == '':
        error = 'ユーザー名が入力されていません'
        return render_template('register.html', error=error)
    if password == '':
        error = 'パスワードが入力されていません'
        return render_template('register.html', error=error)
    
    count = db.insert_user(user_name, password)
    
    if count == 1:
        msg = '登録が完了しました'
        return redirect(url_for('index', msg=msg))
    else:
        error = '登録に失敗しました'
        return render_template('register.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)