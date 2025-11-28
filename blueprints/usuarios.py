from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Usuario, Rol
from forms import UsuarioForm
from extensions import db, bcrypt, admin_required

usuarios_bp = Blueprint('usuarios', __name__, template_folder='templates')

@usuarios_bp.route('/usuarios')
@login_required
@admin_required 
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios_lista.html', usuarios=usuarios)


@usuarios_bp.route('/usuarios/nuevo', methods=['GET', 'POST'])
@login_required
@admin_required
def crear_usuario():
    form = UsuarioForm()

    form.rol.choices = [(r.id, r.nombre) for r in Rol.query.all()]
    
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        nuevo_usuario = Usuario(
            nombre=form.nombre.data,
            email=form.email.data,
            password_hash=hashed_password,
            rol_id=form.rol.data
        )
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Usuario creado exitosamente.', 'success')
        return redirect(url_for('usuarios.listar_usuarios'))
        
    return render_template('usuarios_form.html', form=form, titulo='Nuevo Usuario')

@usuarios_bp.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    form = UsuarioForm(obj=usuario)
    form.rol.choices = [(r.id, r.nombre) for r in Rol.query.all()]
    
    if form.validate_on_submit():
        usuario.nombre = form.nombre.data
        usuario.email = form.email.data
        usuario.rol_id = form.rol.data
        
        if form.password.data:
            usuario.password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            
        db.session.commit()
        flash('Usuario actualizado.', 'success')
        return redirect(url_for('usuarios.listar_usuarios'))
    
    return render_template('usuarios_form.html', form=form, titulo='Editar Usuario')

@usuarios_bp.route('/usuarios/eliminar/<int:id>', methods=['POST'])
@login_required
@admin_required
def eliminar_usuario(id):

    if id == current_user.id:
        flash('No puedes eliminar tu propia cuenta mientras estás logueado.', 'danger')
        return redirect(url_for('usuarios.listar_usuarios'))

    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado.', 'success')
    return redirect(url_for('usuarios.listar_usuarios'))