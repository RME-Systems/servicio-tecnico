from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from models import Cliente
from forms import ClienteForm
from extensions import db


clientes_bp = Blueprint('clientes', __name__, template_folder='templates')



@clientes_bp.route('/clientes')
@login_required
def listar_clientes():

    clientes = Cliente.query.all()
    

    return render_template('clientes_lista.html', clientes=clientes)





@clientes_bp.route('/clientes/nuevo', methods=['GET', 'POST'])
@login_required
def crear_cliente():

    form = ClienteForm()
    
    if form.validate_on_submit():

        nuevo_cliente = Cliente(
            nombre=form.nombre.data,
            telefono=form.telefono.data,
            email=form.email.data
        )
        
        db.session.add(nuevo_cliente)
        db.session.commit()
        
        flash('¡Cliente registrado con éxito!', 'success')
        return redirect(url_for('clientes.listar_clientes'))
    

    return render_template('clientes_form.html', form=form, titulo='Añadir Nuevo Cliente')

@clientes_bp.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_cliente(id):

    cliente = Cliente.query.get_or_404(id)
    

    form = ClienteForm(obj=cliente)
    
    if form.validate_on_submit():

        cliente.nombre = form.nombre.data
        cliente.telefono = form.telefono.data
        cliente.email = form.email.data
        
        db.session.commit()
        
        flash('¡Cliente actualizado con éxito!', 'success')
        return redirect(url_for('clientes.listar_clientes'))
    

    return render_template('clientes_form.html', form=form, titulo='Editar Cliente')


@clientes_bp.route('/clientes/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_cliente(id):

    cliente = Cliente.query.get_or_404(id)
    

    db.session.delete(cliente)
    

    db.session.commit()
    
    flash('¡Cliente eliminado con éxito!', 'success')
    return redirect(url_for('clientes.listar_clientes'))