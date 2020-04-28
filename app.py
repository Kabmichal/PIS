from flask import Flask,render_template,url_for,request,flash,redirect
from zeep import Client
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm
from controllers.zamestnanec_controller import *
from controllers.produkt_controller import *
from controllers.pobocka_controller import *
from controllers.pobocka_produkt_controller import *
from controllers.objednavka_controller import *
from model.produktPobocka import *
from model.produkt import *
from model.zamestnanec import *
from flask_login import LoginManager, login_user, current_user,logout_user
import time
from controllers.email_controller import *
import datetime
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from controllers.produkt_objednavka_controller import *

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
login_manager = LoginManager()
login_manager.init_app(app)
scheduler = BackgroundScheduler()



client = Client(wsdl='http://pis.predmety.fiit.stuba.sk/pis/ws/Students/Team021zamestnanec?WSDL')
objednavka = Client(wsdl='http://pis.predmety.fiit.stuba.sk/pis/ws/Students/Team021objednavka?WSDL')
produkt = Client(wsdl='http://pis.predmety.fiit.stuba.sk/pis/ws/Students/Team021produkt?WSDL')
pobocka = Client(wsdl='http://pis.predmety.fiit.stuba.sk/pis/ws/Students/Team021pobocka?WSDL')
produkt_pobocka_wsdl = Client(wsdl='http://pis.predmety.fiit.stuba.sk/pis/ws/Students/Team021produkt_pobocka?WSDL')
email_wsdl_notify = Client(wsdl="http://pis.predmety.fiit.stuba.sk/pis/ws/NotificationServices/Email?WSDL")
email_wsdl = Client(wsdl="http://pis.predmety.fiit.stuba.sk/pis/ws/Students/Team021email?WSDL")
validator = Client(wsdl="http://pis.predmety.fiit.stuba.sk/pis/ws/Validator?WSDL")
hash_func = Client(wsdl="http://pis.predmety.fiit.stuba.sk/pis/ws/TextCipher?WSDL")
calendar = Client(wsdl="http://pis.predmety.fiit.stuba.sk/pis/ws/Calendar?WSDL")
produkt_objednavka = Client(wsdl="http://pis.predmety.fiit.stuba.sk/pis/ws/Students/Team021produkt_objednavka?WSDL")


def print_date_time():
    emails = email_wsdl.service.getAll()
    for email in emails:
        if email.vybaveny == 0:
            email_date = email.datum
            rozdiel = calendar.service.convertIntervalToDays(time.strftime("%Y-%m-%d"),email_date.strftime("%Y-%m-%d"))
            if(rozdiel>3):
                email_wsdl_notify.service.notify(team_id='021',password='RM7MZR',email="bettina.pinkeova@gmail.com",subject="Prenasame PIS :D ",message="R.I.P.")
                print("Upozornenie veduceho")
            else:
                print("nepresli 3 dni, presli len ",rozdiel)
             

def get_emails_by_user(user_id):
    emails = email_wsdl.service.getAll()
    list_of_emails = []
    for email in emails:
        if email.id_zamestnanec == user_id:
            list_of_emails.append(email)
    return(list_of_emails)



class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

@login_manager.user_loader
def load_user(user_id):
    zamestnanec = client.service.getById(user_id)
    if zamestnanec.id == user_id:
            return zamestnanec
    return None

def find_zamestnanec(pobocka_id):
    najdeni_zamestnanci = client.service.getAll()
    print("nasiel som tychto typkov: ")
    print(najdeni_zamestnanci)
    for najdeny_zamestnanec in najdeni_zamestnanci:
        if((int(najdeny_zamestnanec.pobocka_id) == int(pobocka_id)) and (int(najdeny_zamestnanec.rola) == 1)):
            return najdeny_zamestnanec
    return None

def find_product(task_produkt_id):
    najdene_produkty = produkt_pobocka_wsdl.service.getAll()
    for najdeny_produkt in najdene_produkty:
        if int(najdeny_produkt.produkt_id) == int(task_produkt_id):
            print("!!!!! nasiel som produkt !!!!!")
            return najdeny_produkt
    return None

def email_product(task_produkt_id):
    najdene_produkty = produkt.service.getAll()
    for najdeny_produkt in najdene_produkty:
        if int(najdeny_produkt.id) == int(task_produkt_id):
            print("!!!!! nasiel som produkt !!!!!")
            return najdeny_produkt
    return None

def najdi_aktualnu_objednavku():
    objednavky = objednavka.service.getAll()
    if objednavky is not None:
        for objednavka2 in objednavky:
            if objednavka2.zamestnanec_id == current_user.id and objednavka2.odoslana == 0:
                return objednavka2
    return None




@app.route('/pridaj_do_objednavky/<int:id>',methods = ['POST','GET'])
def pridaj_do_objednavky(id):
    najdena_objednavka = najdi_aktualnu_objednavku()
    print("dano")
    print(najdena_objednavka)
    if najdena_objednavka is None:
        vytvor_objednavku("objednavka",current_user.id,0,objednavka)
        najdena_objednavka=najdi_aktualnu_objednavku()
    vytvor_produkt_objednavka("polozka",najdena_objednavka.id,id,produkt_objednavka)
    return redirect('/emails')

@app.route('/etiketa_update/<int:id>',methods = ['POST','GET'])
def etiketa_update(id):
    print("som dnu")
    email = email_wsdl.service.getById(id)
    najdeny_mail = email_product(email.id_produkt)
    print("QQQQQQQQQQ",najdeny_mail)
    print("nasiel som mail",najdeny_mail)
    task_name = najdeny_mail.name
    task_pocet = najdeny_mail.min_pocet
    task_predaj = 0
    produkt_id = najdeny_mail.id
    uprav_produkt(task_name, task_pocet,task_predaj,produkt_id,produkt)
    print("upravil som etiketu")
    return redirect('/emails')


@app.route('/emails',methods = ['POST','GET'])
def zobraz_emaily():
    list_emails_products = []
    dictionary = {}
    emails = get_emails_by_user(current_user.id)
    print("maily su " , emails)
    for email in emails:
        najdeny_mail = email_product(email.id_produkt)
        najdeny_pobocka = find_product(email.id_produkt)
        print("najdeny mail je " , najdeny_mail," ma id ",email.id_produkt)
        dictionary.update({
                        "email_id" : email.id,
                        "produkt_id":najdeny_mail.id,
                        "produkt_name":najdeny_mail.name,
                        "dalsi_predaj":najdeny_mail.dalsi_predaj,
                        "min_pocet":najdeny_mail.min_pocet,
                        "aktualny_pocet": najdeny_pobocka.pocet_pobocka
                    })
        list_emails_products.append(dictionary.copy())
    print("list produktov ", list_emails_products)
    return render_template('emails.html',list_emails_products=list_emails_products)

def find_concrete_mail(id_produkt):
    all_emails = email_wsdl.service.getAll()
    for email in all_emails:
        if ((email.id_zamestnanec == current_user.id) and (email.id_produkt == id_produkt)):
            return email
    return None

def najdi_polozku(email_id):
    vsetky_polozky = produkt_objednavka.service.getAll()
    for polozka in vsetky_polozky:
        if polozka.email_id == email_id:
            return polozka
    return None

@app.route('/uprav_mnozstvo',methods = ['POST','GET'])
def uprav_mnozstvo_pobocka():
    if request.method=='POST':
        print("bol stlaceny ",request.form['button'])
        if request.form['button'] == 'Odrataj':
            flash("ok")
            task_produkt_id = request.form['produkt_id']
            task_mnozstvo = request.form['mnozstvo']
            produkt_server = produkt.service.getById(task_produkt_id)
            najdeny_produkt = find_product(task_produkt_id)
            if najdeny_produkt is not None:
                produkt_server = Produkt(produkt_server.id,produkt_server.name,produkt_server.min_pocet,produkt_server.dalsi_predaj)
                print("najdeny produkt",najdeny_produkt)
                najdeny_produkt = ProduktPobocka(int(najdeny_produkt.id),najdeny_produkt.name,int(najdeny_produkt.produkt_id),int(najdeny_produkt.pobocka_id),int(najdeny_produkt.pocet_pobocka),najdeny_produkt.pokles_minima)
                if (int(najdeny_produkt.pocet_pobocka)-int(task_mnozstvo))>0:
                    hodnota=(int(najdeny_produkt.pocet_pobocka)-int(task_mnozstvo))
                    uprav_produkt_pobocka(najdeny_produkt.name,najdeny_produkt.produkt_id,najdeny_produkt.pobocka_id,hodnota,najdeny_produkt.pokles_minima,najdeny_produkt.id,produkt_pobocka_wsdl)
                    print("pokles minima je ",najdeny_produkt.pokles_minima )
                    if ((hodnota<produkt_server.min_pocet) and (najdeny_produkt.pokles_minima == 0)):
                        najdeny_zamestnanec = find_zamestnanec(najdeny_produkt.pobocka_id)
                        print("najdeny zamestnanec je")
                        print(najdeny_zamestnanec)
                        if najdeny_zamestnanec is not None:
                            posli_email('vypredany tovar', najdeny_zamestnanec.id,najdeny_produkt.produkt_id,datetime.datetime.now(),0,email_wsdl)
                            uprav_produkt_pobocka(najdeny_produkt.name, najdeny_produkt.produkt_id,najdeny_produkt.pobocka_id,hodnota,1,najdeny_produkt.id,produkt_pobocka_wsdl)
                            scheduler.add_job(func=print_date_time, trigger="interval", seconds=150000)
                            scheduler.start()
                            atexit.register(lambda: scheduler.shutdown())
                            email_wsdl_notify.service.notify(team_id='021',password='RM7MZR',email="bettina.pinkeova@gmail.com",subject="Prenasame PIS :D ",message="R.I.P.")
                else:
                    flash("nizka hodnota")
                    print("nedostatok tovaru")
        elif request.form['button'] == 'Prirataj':
            task_produkt_id = request.form['produkt_id']
            task_mnozstvo = request.form['mnozstvo']
            produkt_server = produkt.service.getById(task_produkt_id)
            najdeny_produkt = find_product(task_produkt_id)
            if najdeny_produkt is not None:
                produkt_server = Produkt(produkt_server.id,produkt_server.name,produkt_server.min_pocet,produkt_server.dalsi_predaj)
                najdeny_produkt = ProduktPobocka(int(najdeny_produkt.id),najdeny_produkt.name,int(najdeny_produkt.produkt_id),int(najdeny_produkt.pobocka_id),int(najdeny_produkt.pocet_pobocka),najdeny_produkt.pokles_minima)
                ziskany_produkt = produkt.service.getById(najdeny_produkt.produkt_id)
                hodnota=(int(najdeny_produkt.pocet_pobocka)+int(task_mnozstvo))
                uprav_produkt_pobocka(najdeny_produkt.name,najdeny_produkt.produkt_id,najdeny_produkt.pobocka_id,hodnota,0,najdeny_produkt.id,produkt_pobocka_wsdl)
                if (hodnota>ziskany_produkt.min_pocet):
                    email_to_remove=find_concrete_mail(najdeny_produkt.produkt_id)
                    polozka_na_odstranenie = najdi_polozku(email_to_remove.id)
                    email_wsdl.service.delete(team_id="021",team_password="RM7MZR",entity_id=email_to_remove.id)
                    produkt_objednavka.service.delete(team_id="021",team_password="RM7MZR",entity_id=polozka_na_odstranenie.id)
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

def najdi_produkt_pobocka(id_produkt,id_pobocka):
    produkty_v_pobocke= produkt_pobocka_wsdl.service.getAll()
    for produkt_v_pobocke in produkty_v_pobocke:
        if((produkt_v_pobocke.produkt_id == id_produkt) and (produkt_v_pobocke.pobocka_id==id_pobocka)):
            return produkt_v_pobocke
    return None

def odstran_vsetko(zoznam):
    ziskana_objednavka = produkt_pobocka_wsdl.service.getById(zoznam['produkt_pobocka_id'])
    uprav_produkt_pobocka(ziskana_objednavka.name, ziskana_objednavka.produkt_id,ziskana_objednavka.pobocka_id,zoznam['objednavane_mnozstvo'],0,ziskana_objednavka.id,produkt_pobocka_wsdl)
    produkt_objednavka.service.delete(team_id="021",team_password="RM7MZR",entity_id=zoznam['produkt_objednavka_id'])
    email_wsdl.service.delete(team_id="021",team_password="RM7MZR",entity_id=zoznam['email_id'])

#https://codepen.io/Middi/pen/rJYOyz
@app.route('/objednavka', methods = ['GET','POST'])
def objednaj():
    najdena_objednavka = najdi_aktualnu_objednavku()
    dictionary = {}
    list_of_orders = []
    if najdena_objednavka is not None:
        produkty_v_objednavke = produkt_objednavka.service.getAll()
        for produkt_v_objednavke in produkty_v_objednavke:
            if produkt_v_objednavke.objednavka_id == najdena_objednavka.id:
                email_info = email_wsdl.service.getById(produkt_v_objednavke.email_id)
                produkt_info = produkt.service.getById(email_info.id_produkt)
                produkt_v_pobocke = najdi_produkt_pobocka(produkt_info.id,current_user.pobocka_id)
                dictionary.update({
                        "email_id" : email_info.id,
                        "produkt_id":produkt_info.id,
                        "produkt_name":produkt_info.name,
                        "min_pocet":produkt_info.min_pocet,
                        "objednavane_mnozstvo": int(produkt_info.min_pocet)*2,
                        "aktualne_mnozstvo":produkt_v_pobocke.pocet_pobocka,
                        "produkt_pobocka_id":produkt_v_pobocke.id,
                        "produkt_objednavka_id":produkt_v_objednavke.id,
                        "objednavka_id":produkt_v_objednavke.objednavka_id,
                        "poznamka":" "

                    })
                list_of_orders.append(dictionary.copy())
    print("!!!!POD!!!!")
    print(list_of_orders)
    if request.method == 'POST':
        for order in list_of_orders:
            print("order",order)
            order['poznamka'] = "objednane od subdodavatela"
            odstran_vsetko(order)
        objednavka.service.delete(team_id="021",team_password="RM7MZR",entity_id=order['objednavka_id'])
        return render_template('objednavka_fixnuta.html',list_of_orders=list_of_orders)
    else:
        return render_template('objednavka.html',list_of_orders=list_of_orders)

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