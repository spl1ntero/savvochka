from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Замените на ваш секретный ключ


def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


def save_data(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


flowers = load_data('flowers.json')
suppliers = load_data('suppliers.json')
sellers = load_data('sellers.json')


@app.route('/', methods=['GET'])
def index():
    current_season = request.args.get('season')
    if current_season:
        filtered_flowers = [flower for flower in flowers if flower['season'] == current_season]
        return render_template('index.html', flowers=filtered_flowers, current_season=current_season,
                               suppliers=suppliers, sellers=sellers)
    else:
        return render_template('index.html', flowers=flowers, current_season=None, suppliers=suppliers, sellers=sellers)


@app.route('/add_info', methods=['GET'])
def add_info():
    if 'username' in session and session['username'] == 'admin':
        return render_template('add_info.html')
    else:
        flash('Пожалуйста, войдите для доступа к админ-панели.')
        return redirect(url_for('login'))


@app.route('/get_flowers', methods=['GET'])
def get_flowers():
    return jsonify(flowers)


@app.route('/get_suppliers', methods=['GET'])
def get_suppliers():
    return jsonify(suppliers)


@app.route('/get_sellers', methods=['GET'])
def get_sellers():
    return jsonify(sellers)


@app.route('/filter_by_season', methods=['GET'])
def filter_by_season():
    season = request.args.get('season')
    filtered_flowers = [flower for flower in flowers if flower['season'] == season]
    return render_template('index.html', flowers=filtered_flowers, suppliers=suppliers, sellers=sellers)


@app.route('/filter_by_country', methods=['GET'])
def filter_by_country():
    country = request.args.get('country')
    filtered_flowers = [flower for flower in flowers if flower['country'] == country]
    return render_template('index.html', flowers=filtered_flowers, current_season=None, suppliers=suppliers,
                           sellers=sellers)


@app.route('/filter_by_supplier', methods=['GET'])
def filter_by_supplier():
    name = request.args.get('name')
    filtered_suppliers = [supplier for supplier in suppliers if supplier['name'] == name]
    return render_template('index.html', flowers=flowers, current_season=None, suppliers=suppliers, filtered_suppliers=filtered_suppliers, sellers=sellers)



@app.route('/add_seller', methods=['POST'])
def add_seller():
    if 'username' in session and session['username'] == 'admin':
        name = request.form.get('name')
        address = request.form.get('address')

        new_seller = {"name": name, "address": address}
        sellers.append(new_seller)

        save_data(sellers, 'sellers.json')

        return redirect(url_for('add_info'))
    else:
        flash('Недостаточно прав.')
        return redirect(url_for('login'))


@app.route('/add_supplier', methods=['POST'])
def add_supplier():
    if 'username' in session and session['username'] == 'admin':
        name = request.form.get('name')
        type = request.form.get('type')
        address = request.form.get('address')

        new_supplier = {"name": name, "type": type, "address": address}
        suppliers.append(new_supplier)

        save_data(suppliers, 'suppliers.json')

        return redirect(url_for('add_info'))
    else:
        flash('Недостаточно прав.')
        return redirect(url_for('login'))


@app.route('/add_flower', methods=['POST'])
def add_flower():
    if 'username' in session and session['username'] == 'admin':
        name = request.form.get('name')
        type = request.form.get('type')
        country = request.form.get('country')
        season = request.form.get('season')
        sort = request.form.get('sort')
        price = request.form.get('price')
        supplier = request.form.get('supplier')
        seller = request.form.get('seller')

        new_flower = {
            "name": name,
            "type": type,
            "country": country,
            "season": season,
            "sort": sort,
            "price": price,
            "supplier": supplier,
            "seller": seller
        }
        flowers.append(new_flower)

        save_data(flowers, 'flowers.json')

        return redirect(url_for('add_info'))
    else:
        flash('Недостаточно прав.')
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin':
            session['username'] = username
            return redirect(url_for('add_info'))
        else:
            flash('Неправильное имя пользователя или пароль.')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/flowers_by_supplier', methods=['GET'])
def flowers_by_supplier():
    supplier_name = request.args.get('supplier')
    supplier_flowers = [flower for flower in flowers if flower['supplier'] == supplier_name]
    return render_template('index.html', flowers=supplier_flowers, current_season=None, suppliers=suppliers, sellers=sellers, filtered_suppliers=None)

@app.route('/suppliers_by_flower_sort', methods=['GET'])
def suppliers_by_flower_sort():
    flower_sort = request.args.get('sort')
    flower_suppliers = [supplier for supplier in suppliers if flower_sort in [flower['sort'] for flower in flowers if flower['supplier'] == supplier['name']]]
    return render_template('index.html', flowers=flowers, current_season=None, suppliers=suppliers, sellers=sellers, filtered_suppliers=flower_suppliers)

@app.route('/expensive_flower_sellers', methods=['GET'])
def expensive_flower_sellers():
    max_price = max([float(flower['price']) for flower in flowers])
    expensive_sellers = [seller for seller in sellers if any(flower for flower in flowers if float(flower['price']) == max_price and flower['seller'] == seller['name'])]
    return render_template('index.html', flowers=flowers, current_season=None, suppliers=suppliers, sellers=expensive_sellers, filtered_suppliers=None)

@app.route('/common_suppliers', methods=['GET'])
def common_suppliers():
    seller1 = request.args.get('seller1')
    seller2 = request.args.get('seller2')
    suppliers_seller1 = {flower['supplier'] for flower in flowers if flower['seller'] == seller1}
    suppliers_seller2 = {flower['supplier'] for flower in flowers if flower['seller'] == seller2}
    common_suppliers = list(suppliers_seller1.intersection(suppliers_seller2))
    return render_template('index.html', flowers=flowers, current_season=None, suppliers=common_suppliers, sellers=sellers, filtered_suppliers=None)


if __name__ == '__main__':
    app.run(debug=True)
