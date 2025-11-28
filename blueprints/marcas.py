from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from models import Marca
from forms import MarcaForm
from extensions import db


marcas_bp = Blueprint('marcas', __name__, template_folder='templates')



@marcas_bp.route('/marcas')
@login_required
def listar_marcas():

    marcas = Marca.query.all()
    

    return render_template('marcas_lista.html', marcas=marcas)


@marcas_bp.route('/marcas/nueva', methods=['GET', 'POST'])
@login_required
def crear_marca():

    form = MarcaForm()
    

    if form.validate_on_submit():

        nueva_marca = Marca(nombre=form.nombre.data)
        

        db.session.add(nueva_marca)
        db.session.commit()
        

        flash('¡Marca registrada con éxito!', 'success')
        

        return redirect(url_for('marcas.listar_marcas'))
    


    return render_template('marcas_form.html', form=form, titulo='Añadir Nueva Marca')






@marcas_bp.route('/marcas/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_marca(id):


    marca = Marca.query.get_or_404(id)
    


    form = MarcaForm(obj=marca)
    
    if form.validate_on_submit():

        marca.nombre = form.nombre.data
        

        db.session.commit()
        
        flash('¡Marca actualizada con éxito!', 'success')
        return redirect(url_for('marcas.listar_marcas'))
    

    return render_template('marcas_form.html', form=form, titulo='Editar Marca')


@marcas_bp.route('/marcas/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_marca(id):

    marca = Marca.query.get_or_404(id)
    

    db.session.delete(marca)
    

    db.session.commit()
    
    flash('¡Marca eliminada con éxito!', 'success')
    return redirect(url_for('marcas.listar_marcas'))