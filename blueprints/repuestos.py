from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from models import Repuesto
from forms import RepuestoForm
from extensions import db


repuestos_bp = Blueprint('repuestos', __name__, template_folder='templates')



@repuestos_bp.route('/repuestos')
@login_required
def listar_repuestos():

    repuestos = Repuesto.query.all()
    

    return render_template('repuestos_lista.html', repuestos=repuestos)





@repuestos_bp.route('/repuestos/nuevo', methods=['GET', 'POST'])
@login_required
def crear_repuesto():
    form = RepuestoForm()
    
    if form.validate_on_submit():

        nuevo_repuesto = Repuesto(
            nombre=form.nombre.data,
            stock=form.stock.data,
            precio=form.precio.data
        )
        
        db.session.add(nuevo_repuesto)
        db.session.commit()
        
        flash('¡Repuesto registrado con éxito!', 'success')
        return redirect(url_for('repuestos.listar_repuestos'))
    

    return render_template('repuestos_form.html', form=form, titulo='Añadir Nuevo Repuesto')





@repuestos_bp.route('/repuestos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_repuesto(id):

    repuesto = Repuesto.query.get_or_404(id)
    

    form = RepuestoForm(obj=repuesto)
    
    if form.validate_on_submit():

        repuesto.nombre = form.nombre.data
        repuesto.stock = form.stock.data
        repuesto.precio = form.precio.data
        

        db.session.commit()
        
        flash('¡Repuesto actualizado con éxito!', 'success')
        return redirect(url_for('repuestos.listar_repuestos'))
    

    return render_template('repuestos_form.html', form=form, titulo='Editar Repuesto')





@repuestos_bp.route('/repuestos/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_repuesto(id):

    repuesto = Repuesto.query.get_or_404(id)
    

    db.session.delete(repuesto)
    

    db.session.commit()
    
    flash('¡Repuesto eliminado del inventario!', 'success')
    return redirect(url_for('repuestos.listar_repuestos'))