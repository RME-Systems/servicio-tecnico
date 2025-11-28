from flask import redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from functools import wraps


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()


login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, inicie sesión para acceder a esta página.'
login_manager.login_message_category = 'info'


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):


        if not current_user.is_authenticated or current_user.rol.nombre != 'Admin':
            flash('Acceso denegado. Se requieren permisos de Administrador.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function