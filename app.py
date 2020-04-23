from flask import Flask,render_template,url_for,request,flash,redirect
from zeep import Client
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm
from controllers.zamestnanec_controller import try2_func,update_func

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

client = Client(wsdl='http://pis.predmety.fiit.stuba.sk/pis/ws/Students/Team021zamestnanec?WSDL')
objednavka = Client(wsdl='http://pis.predmety.fiit.stuba.sk/pis/ws/Students/Team021objednavka?WSDL')

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

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
        update_func(task_name, task_rola,task_pobocka,id,client)
        return redirect('/')
    else:
        return render_template('update.html',user=user)

@app.route('/',methods = ['POST','GET'])
def index():
    #try2_func()
    #get_names()
    if request.method=='POST':
        task_name = request.form['name']
        task_rola = request.form['rola']
        task_pobocka = request.form['pobocka']
        print(task_name,' a cena ',task_rola," a ",task_pobocka)
        try2_func(task_name,task_rola,task_pobocka,client)
        return redirect('/')
    else:
        client_list = client.service.getAll()
        if client_list is None:
            client_list = []
        print(client_list)
        print("skuska")
        for lists in client_list:
            print(lists.id)
            print(lists.name)
            #skuska = Zamestnanec()
        return render_template('index.html',client_list=client_list)

if __name__ == "__main__":
    app.run(debug=True)