from flask import Flask, jsonify, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)


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
    return render_template('index.html', flowers=flowers, current_season=None, suppliers=suppliers,
                           filtered_suppliers=filtered_suppliers, sellers=sellers)


@app.route('/add_seller', methods=['POST'])
def add_seller():
    name = request.form.get('name')
    address = request.form.get('address')

    new_seller = {"name": name, "address": address}
    sellers.append(new_seller)

    save_data(sellers, 'sellers.json')

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
