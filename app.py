from flask import Flask, render_template, request, redirect ,url_for, session
import db, string, random
from datetime import timedelta

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')
    
    if msg == None:
        return render_template('index.html')
    else:
        return render_template('index.html', msg = msg)
    
@app.route('/', methods=['POST'])
def login():
    user_name = request.form.get('username')
    password = request.form.get('password')
    
    if db.login(user_name, password):
        session['user'] = True #sessionにuserバリューにTrueを保存
        # 下2行は操作しないとログインページに戻されるやつ
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=100)
        return redirect(url_for('mypage'))
    else:
        error = 'ログインに失敗しました。'
        input_data  = {
            'user_name': user_name,
            'password': password
        }
        return render_template('index.html', error = error, data = input_data)

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
    user_name = request.form.get('username')
    password = request.form.get('password')
    
    if user_name == '':
        error = 'ユーザー名が未入力です。'
        return render_template('register.html', error = error)
    if password == '':
        error = 'パスワードが未入力です。'
        return render_template('register.html', error = error)
    
    count = db.insert_user(user_name, password)
    
    if count == 1:
        msg = '登録が完了しました。'
        return render_template('index.html', msg=msg)
    else:
        error = '登録に失敗しました。'
    return render_template('register.html', error=error)
    
@app.route('/list')
def list():
    shop_list = db.select_all_shops()
    return render_template('list.html', shops=shop_list)

@app.route('/shop_register')
def shop_register():
    return render_template('shop_register.html')

@app.route('/shop_register_exe', methods=['POST'])
def shop_register_exe():
    shops_name = request.form.get('shops_name')
    company = request.form.get('company')
    price = request.form.get('price')
    stock = request.form.get('stock')
    if shops_name == '':
        error = '商品名が入力されてません。'
        return render_template('shop_register.html', error=error)
    if company == '':
        error = '会社名が入力されてません。'
        return render_template('shop_register.html', error=error)
    if price == '':
        error = '価格が入力されてません。'
        return render_template('shop_register.html', error=error)
    if stock == '':
        error = '在庫が入力されてません。'
        return render_template('shop_register.html', error=error)
    count = db.insert_shops(shops_name, company, price, stock)
    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('shop_register', msg=msg))
    else:
        error = '登録に失敗しました。'
        print()
        return render_template('register.html', error=error)

    
@app.route('/search_shops_exe', methods=['POST'])
def search_shops_exe():
    name = request.form.get('name')
    shop_list = db.search_shops(name)
    return render_template('list.html', shops=shop_list)

@app.route('/shop', methods=['POST'])
def shop():
    id = request.form.get('id')
    
    db.shop(id)
    
    return render_template('shop_success.html')


@app.route('/shop_delete', methods=['POST'])
def shop_delete():
    id = request.form.get('id')
    
    db.shop_delete(id)
    
    return render_template('shop_delete_success.html')

@app.route('/topmenuback')
def topmenuback():
    shop_list = db.select_all_shops()
    return render_template('list.html', shops=shop_list)
  

@app.route('/shopdelete')
def shopdelete():
    return render_template('shop_delete.html')

@app.route('/loginback')
def loginback():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)