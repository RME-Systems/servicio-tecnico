from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from models import TipoEquipo
from forms import TipoEquipoForm
from extensions import db


tipos_bp = Blueprint('tipos', __name__, template_folder='templates')

@tipos_bp.route('/tipos')
@login_required
def listar_tipos():

    tipos = TipoEquipo.query.all()
    

    return render_template('tipos_lista.html', tipos=tipos)

@tipos_bp.route('/tipos/nuevo', methods=['GET', 'POST'])
@login_required
def crear_tipo():

    form = TipoEquipoForm()
    
    if form.validate_on_submit():

        nuevo_tipo = TipoEquipo(nombre=form.nombre.data)
        
        db.session.add(nuevo_tipo)
        db.session.commit()
        
        flash('¡Tipo de equipo registrado con éxito!', 'success')
        return redirect(url_for('tipos.listar_tipos'))
    


    return render_template('marcas_form.html', form=form, titulo='Añadir Nuevo Tipo de Equipo')


@tipos_bp.route('/tipos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_tipo(id):

    tipo = TipoEquipo.query.get_or_404(id)
    

    form = TipoEquipoForm(obj=tipo)
    
    if form.validate_on_submit():

        tipo.nombre = form.nombre.data
        

        db.session.commit()
        
        flash('¡Tipo de equipo actualizado con éxito!', 'success')
        return redirect(url_for('tipos.listar_tipos'))
    

    return render_template('marcas_form.html', form=form, titulo='Editar Tipo de Equipo')

@tipos_bp.route('/tipos/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_tipo(id):

    tipo = TipoEquipo.query.get_or_404(id)
    

    db.session.delete(tipo)
    

    db.session.commit()
    
    flash('¡Tipo de equipo eliminado con éxito!', 'success')
    return redirect(url_for('tipos.listar_tipos'))