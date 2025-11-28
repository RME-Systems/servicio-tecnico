from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from models import Equipo, Cliente, Marca, TipoEquipo
from forms import EquipoForm
from extensions import db

equipos_bp = Blueprint('equipos', __name__, template_folder='templates')

@equipos_bp.route('/equipos')
@login_required
def listar_equipos():
    equipos = Equipo.query.all()
    

    return render_template('equipos_lista.html', equipos=equipos)


@equipos_bp.route('/equipos/nuevo', methods=['GET', 'POST'])
@login_required
def crear_equipo():

    form = EquipoForm()
    



    form.cliente.choices = [(c.id, c.nombre) for c in Cliente.query.order_by(Cliente.nombre).all()]
    form.marca.choices = [(m.id, m.nombre) for m in Marca.query.order_by(Marca.nombre).all()]
    form.tipo.choices = [(t.id, t.nombre) for t in TipoEquipo.query.order_by(TipoEquipo.nombre).all()]
    
    if form.validate_on_submit():


        nuevo_equipo = Equipo(
            modelo=form.modelo.data,
            serial=form.serial.data,
            cliente_id=form.cliente.data,
            marca_id=form.marca.data,
            tipo_id=form.tipo.data
        )
        
        db.session.add(nuevo_equipo)
        db.session.commit()
        
        flash('¡Equipo registrado con éxito!', 'success')
        return redirect(url_for('equipos.listar_equipos'))
    

    return render_template('equipos_form.html', form=form, titulo='Añadir Nuevo Equipo')

@equipos_bp.route('/equipos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_equipo(id):

    equipo = Equipo.query.get_or_404(id)
    

    form = EquipoForm(obj=equipo)
    

    form.cliente.choices = [(c.id, c.nombre) for c in Cliente.query.order_by(Cliente.nombre).all()]
    form.marca.choices = [(m.id, m.nombre) for m in Marca.query.order_by(Marca.nombre).all()]
    form.tipo.choices = [(t.id, t.nombre) for t in TipoEquipo.query.order_by(TipoEquipo.nombre).all()]
    
    if form.validate_on_submit():

        equipo.modelo = form.modelo.data
        equipo.serial = form.serial.data
        equipo.cliente_id = form.cliente.data
        equipo.marca_id = form.marca.data
        equipo.tipo_id = form.tipo.data
        

        db.session.commit()
        
        flash('¡Equipo actualizado con éxito!', 'success')
        return redirect(url_for('equipos.listar_equipos'))
    


    return render_template('equipos_form.html', form=form, titulo='Editar Equipo')

@equipos_bp.route('/equipos/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_equipo(id):

    equipo = Equipo.query.get_or_404(id)
    

    db.session.delete(equipo)
    
    db.session.commit()
    
    flash('¡Equipo eliminado con éxito!', 'success')
    return redirect(url_for('equipos.listar_equipos'))