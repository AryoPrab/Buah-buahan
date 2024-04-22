import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask,redirect,url_for,render_template,request, jsonify
from pymongo import MongoClient
from bson import ObjectId

# URL = "mongodb+srv://aryogmeet:12345aryo@cluster0.rbtnrar.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# client = MongoClient(URL)
# db = client.dbfruit
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def home():
    fruit = list(db.fruit.find({}))
    return render_template('dashboard.html', fruit = fruit)


@app.route('/fruit', methods=['GET','POST'])
def fruit():
    daftar = list(db.fruit.find({}))
    return render_template('index.html' , fruit = daftar)

@app.route('/tambah', methods=['GET','POST'])
def tambah():
    if request.method == 'POST':
        nama = request.form['nama']
        harga = request.form['harga']
        deskripsi = request.form['desc']
        gambar = request.files['gambar']

        if gambar :
            fileasli = gambar.filename
            filegambar = fileasli.split('/')[-1]
            print(fileasli)
            gambarpath = f'static/assets/img/imgfruit/{filegambar}'
            gambar.save(gambarpath)
        else : 
            gambar = None

        doc = {
            'nama' : nama,
            'harga' : harga,
            'deskripsi' : deskripsi,
            'gambar' : filegambar
        }

        db.fruit.insert_one(doc)
        return redirect(url_for("fruit"))
    return render_template('Addfruit.html')

@app.route('/edit/<_id>', methods=['GET','POST'])
def edit(_id):
    if request.method == 'POST':
        id = request.form['id']
        nama = request.form['nama']
        harga = request.form['harga']
        deskripsi = request.form['desc']
        gambar = request.files['gambar']
        doc = {
            'nama' : nama,
            'harga' : harga,
            'deskripsi' : deskripsi,
        }

        if gambar :
            fileasli = gambar.filename
            filegambar = fileasli.split('/')[-1]
            print(fileasli)
            gambarpath = f'static/assets/img/imgfruit/{filegambar}'
            gambar.save(gambarpath)
            doc['gambar'] = filegambar
        
        db.fruit.update_one({'_id' : ObjectId(id)},{'$set': doc})
        return redirect(url_for("fruit"))
    
    id = ObjectId(_id)
    data=list(db.fruit.find({'_id': id}))
    print(data)
    return render_template('EditFruit.html', data=data)

@app.route('/delete/<_id>', methods=['GET','POST'])
def delete(_id):
    db.fruit.delete_one({'_id': ObjectId(_id)})
    return redirect(url_for("fruit"))
 


if __name__ == '__main__':
    app.run(port=5000, debug=True)
 

