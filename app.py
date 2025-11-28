import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from blueprints.auth import auth_bp
from blueprints.marcas import marcas_bp
from blueprints.tipos_equipo import tipos_bp
from blueprints.clientes import clientes_bp
from blueprints.equipos import equipos_bp
from blueprints.repuestos import repuestos_bp
from blueprints.ordenes import ordenes_bp
from blueprints.usuarios import usuarios_bp


from extensions import db, migrate, bcrypt, login_manager


from forms import LoginForm
from models import Usuario, Cliente, Orden, Repuesto


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Rme-serv123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'servicio-tecnico.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
login_manager.init_app(app)
app.register_blueprint(auth_bp)
app.register_blueprint(marcas_bp)
app.register_blueprint(tipos_bp)
app.register_blueprint(clientes_bp)
app.register_blueprint(equipos_bp)
app.register_blueprint(repuestos_bp)
app.register_blueprint(ordenes_bp)
app.register_blueprint(usuarios_bp)




@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))



@app.route('/')
@login_required
def index():

    total_clientes = Cliente.query.count()




    ordenes_activas = Orden.query.filter(Orden.estado_id < 4).count()


    repuestos_bajos = Repuesto.query.filter(Repuesto.stock < 5).count()

    return render_template('dashboard.html', 
                           n_clientes=total_clientes,
                           n_ordenes=ordenes_activas,
                           n_bajos=repuestos_bajos)

if __name__ == '__main__':
    app.run(debug=True)