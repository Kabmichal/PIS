from flask import Flask,render_template,url_for,request,flash,redirect
from zeep import Client
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm
from controllers.zamestnanec_controller import *
from controllers.produkt_controller import *
from controllers.pobocka_controller import *
from controllers.pobocka_produkt_controller import *
from model.produktPobocka import *
from model.produkt import *
from model.zamestnanec import *
from flask_login import LoginManager, login_user, current_user,logout_user
import time

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
login_manager = LoginManager()
login_manager.init_app(app)


client = Client(wsdl='http://pis.predmety.fiit.stuba.sk/pis/ws/Students/Team021zamestnanec?WSDL')
objednavka = Client(wsdl='http://pis.predmety.fiit.stuba.sk/pis/ws/Students/Team021objednavka?WSDL')
produkt = Client(wsdl='http://pis.predmety.fiit.stuba.sk/pis/ws/Students/Team021produkt?WSDL')
pobocka = Client(wsdl='http://pis.predmety.fiit.stuba.sk/pis/ws/Students/Team021pobocka?WSDL')
produkt_pobocka_wsdl = Client(wsdl='http://pis.predmety.fiit.stuba.sk/pis/ws/Students/Team021produkt_pobocka?WSDL')
email_wsdl_notify = Client(wsdl="http://pis.predmety.fiit.stuba.sk/pis/ws/NotificationServices/Email?WSDL")
email_validation = Client(wsdl="http://pis.predmety.fiit.stuba.sk/pis/ws/Validator?WSDL")
email_wsdl = Client(wsdl="http://pis.predmety.fiit.stuba.sk/pis/ws/Students/Team021email?WSDL")
validator = Client(wsdl="http://pis.predmety.fiit.stuba.sk/pis/ws/Validator?WSDL")
hash_func = Client(wsdl="http://pis.predmety.fiit.stuba.sk/pis/ws/TextCipher?WSDL")

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

@login_manager.user_loader
def load_user(user_id):
    zamestnanec = client.service.getById(user_id)
    if zamestnanec.id == user_id:
            return zamestnanec
    return None

@app.route('/uprav_mnozstvo',methods = ['POST','GET'])
def uprav_mnozstvo_pobocka():
    if request.method=='POST':
        flash("ok")
        task_produkt_id = request.form['produkt_id']
        task_mnozstvo = request.form['mnozstvo']
        produkt_server = produkt.service.getById(task_produkt_id)
        print("id produktu ",task_produkt_id)
        print(produkt.service.getAll())
        print("4444444444444444 ",produkt_server)
        najdeny_produkt = produkt_pobocka_wsdl.service.getByAttributeValue("produkt_id",task_produkt_id,produkt_pobocka_wsdl.service.getAll())
        if najdeny_produkt is not None:
            produkt_server = Produkt(produkt_server.id,produkt_server.name,produkt_server.min_pocet,produkt_server.dalsi_predaj)
            print("zzzzzzzzzzzzzzzzzz")
            print(najdeny_produkt)
            print(najdeny_produkt[0].id)
            najdeny_produkt = ProduktPobocka(int(najdeny_produkt[0]['id']),najdeny_produkt[0]['name'],int(najdeny_produkt[0]['produkt_id']),int(najdeny_produkt[0]['pobocka_id']),int(najdeny_produkt[0]['pocet_pobocka']),najdeny_produkt[0]['pokles_minima'])
            if (int(najdeny_produkt.pocet_pobocka)-int(task_mnozstvo))>0:
                hodnota=(int(najdeny_produkt.pocet_pobocka)-int(task_mnozstvo))
                uprav_produkt_pobocka(najdeny_produkt.name,najdeny_produkt.produkt_id,najdeny_produkt.pobocka_id,hodnota,najdeny_produkt.pokles_minima,najdeny_produkt.id,produkt_pobocka_wsdl)
                if hodnota<produkt_server.min_pocet:
                    print("malo!!!!!!!!!!!!!!!!!!")
                    email_wsdl_notify.service.notify(team_id='021',password='RM7MZR',email="bettina.pinkeova@gmail.com",subject="Prenasame PIS :D ",message="R.I.P.")
            else:
                flash("nizka hodnota")
                print("nedostatok tovaru")
        return redirect("/vytvor_pobocka2")
    else:
        flash("ok")
        return render_template('uprav_mnozstvo.html')

@app.route('/vytvor_pobocka2',methods = ['POST','GET'])
def add_pobocka():
    if request.method=='POST':
        print(request.form['button'])
        if request.form['button'] == 'Pridaj pobocku':
            print("pridaj pobocku")
            task_name = request.form['name']
            task_adresa = request.form['adresa']
            pridaj_pobocku(task_name,task_adresa,pobocka)
        else:
            print("pridaj produkt")
            task_name = request.form['nazov']
            task_produkt_id = request.form['produkt_id']
            task_pobocka_id= request.form['pobocka_id']
            task_pocet_pobocka = request.form['pocet_pobocka']
            task_pokles_minima = request.form['pokles_minima']
            pridaj_produkt_pobocka(task_name,task_produkt_id,task_pobocka_id,task_pocet_pobocka,task_pokles_minima,produkt_pobocka_wsdl)
        return redirect('/vytvor_pobocka2')
    else:
        pobocky = pobocka.service.getAll()
        print("current user jeeeee ")
        print(current_user)
        if pobocky is None:
            pobocky = []
        return render_template('pobocka.html',pobocky=pobocky)


@app.route('/objednavka', methods = ['GET','POST'])
def objednaj():
    if request.method == 'POST':
        return redirect('/')
    else:
        return render_template('objednavka.html')

@app.route('/vytvor_produkt', methods = ['GET','POST'])
def vytvor_produkt():
    if request.method == 'POST':
        task_name = request.form['name']
        task_pocet = request.form['min_pocet']
        task_predaj = request.form['dalsi_predaj']
        pridaj_produkt(task_name, task_pocet,task_predaj,produkt)
        return redirect('/vytvor_produkt')
    else:
        produkt_list = produkt.service.getAll()
        if produkt_list is None:
            produkt_list = []
        return render_template('produkt.html',produkt_list=produkt_list)

@app.route('/update_produkt/<int:id>', methods = ['GET','POST'])
def update_produkt(id):
    vstupny_produkt = produkt.service.getById(id)
    print("vstupny produkt ",vstupny_produkt)
    if request.method == 'POST':
        task_name = request.form['name']
        task_pocet = request.form['min_pocet']
        task_predaj = request.form['dalsi_predaj']
        uprav_produkt(task_name, task_pocet,task_predaj,id,produkt)
        return redirect('/vytvor_produkt')
    else:
        return render_template('produkt_update.html',vstupny_produkt=vstupny_produkt)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = {
        "team_id": "021",
        "team_password" : "RM7MZR",
        "entity_id": int(id)
    }
    try:
        client.service.delete(**task_to_delete)
        return redirect('/')
    except:
        return "niekde nastal problem"


@app.route('/update/<int:id>', methods = ['GET','POST'])
def update(id):
    user = client.service.getById(id)
    if request.method == 'POST':
        task_name = request.form['name']
        task_rola = request.form['rola']
        task_pobocka = request.form['pobocka']
        task_email = request.form['email']
        task_heslo = request.form['heslo']
        update_func(task_name, task_rola,task_pobocka,task_email,task_heslo,id,client)
        return redirect('/')
    else:
        return render_template('update.html',user=user)

@app.route('/login',methods = ['POST','GET'])
def login():
    if request.method=='POST':
        zamestnanci = client.service.getAll()
        task_email = request.form['email']
        task_heslo = request.form['heslo']
        task_heslo = hash_func.service.encrypt_text(text=task_heslo,key=task_email)
        print("hesielko ")
        print(task_heslo)
        for zamestnanec in zamestnanci:
            if(zamestnanec.email == task_email and zamestnanec.heslo == task_heslo):
                actual_user = Zamestnanec(zamestnanec.id,zamestnanec.name,zamestnanec.rola,zamestnanec.email,zamestnanec.heslo,zamestnanec.is_authenticated,zamestnanec.pobocka_id)
                login_user(actual_user,force=True)
                print(type(current_user))
                print("aaaaaassssssaaaaa")
                print(current_user)
                return redirect('/')
        flash("zle udaje")
        return redirect('/')
    else:
        return render_template('login.html')


@app.route('/',methods = ['POST','GET'])
def index():
    #try2_func()
    #get_names()
    
    if request.method=='POST':
        task_name = request.form['name']
        task_rola = request.form['rola']
        task_pobocka = request.form['pobocka']
        task_email = request.form['email']
        task_heslo = request.form['heslo']
        print("-------------------")
        print(validator.service.validateEmail(task_email))
        if validator.service.validateEmail(task_email):
            task_heslo = hash_func.service.encrypt_text(text=task_heslo,key=task_email)
            try2_func(task_name,task_rola,task_pobocka,task_email,task_heslo,client)
            flash("ucet uspesne vytvoreny")
            return redirect('/')
        else:
            flash("email nema validnu formu")
            return redirect('/')
    else:
        client_list = client.service.getAll()
        if client_list is None:
            client_list = []
        #print(current_user.is_authenticated)
        if(str(type(current_user))=="<class 'werkzeug.local.LocalProxy'>"):
            print("pasuje to")
            #skuska = Zamestnanec()
        return render_template('index.html',client_list=client_list,current_user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    print(type(current_user))
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)