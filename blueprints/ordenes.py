from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Orden, Equipo, Estado, Repuesto, DetalleOrden
from forms import OrdenForm
from extensions import db

ordenes_bp = Blueprint('ordenes', __name__, template_folder='templates')


@ordenes_bp.route('/ordenes')
@login_required
def listar_ordenes():


    ordenes = Orden.query.order_by(Orden.fecha_ingreso.desc()).all()
    
    return render_template('ordenes_lista.html', ordenes=ordenes)





@ordenes_bp.route('/ordenes/nueva', methods=['GET', 'POST'])
@login_required
def crear_orden():
    form = OrdenForm()
    



    equipos = Equipo.query.all()
    

    opciones_equipos = []
    for e in equipos:
        texto = f"{e.cliente.nombre} - {e.tipo_equipo.nombre} {e.marca.nombre} ({e.modelo})"
        opciones_equipos.append((e.id, texto))
    

    form.equipo.choices = opciones_equipos
    
    if form.validate_on_submit():

        estado_inicial = Estado.query.filter_by(nombre='Ingresado').first()
        

        nueva_orden = Orden(
            problema_reportado=form.problema.data,
            equipo_id=form.equipo.data,
            estado=estado_inicial,      
            tecnico=current_user
        )
        

        db.session.add(nueva_orden)
        db.session.commit()
        
        flash('¡Orden de trabajo creada exitosamente!', 'success')
        return redirect(url_for('ordenes.listar_ordenes'))
        
    return render_template('ordenes_form.html', form=form, titulo='Nueva Orden de Trabajo')





@ordenes_bp.route('/ordenes/<int:id>', methods=['GET', 'POST'])
@login_required
def ver_orden(id):
    orden = Orden.query.get_or_404(id)
    

    if request.method == 'POST':

        nuevo_estado_id = request.form.get('nuevo_estado')
        
        if nuevo_estado_id:
            orden.estado_id = nuevo_estado_id
            db.session.commit()
            flash('¡Estado de la orden actualizado!', 'success')

            return redirect(url_for('ordenes.ver_orden', id=id))


    estados = Estado.query.all()
    lista_repuestos = Repuesto.query.filter(Repuesto.stock > 0).all()
    
    return render_template('orden_detalle.html', orden=orden, estados=estados, repuestos = lista_repuestos)

@ordenes_bp.route('/ordenes/<int:id>/agregar_repuesto', methods=['POST'])
@login_required
def agregar_repuesto(id):
    orden = Orden.query.get_or_404(id)
    

    repuesto_id = request.form.get('repuesto_id')
    cantidad = int(request.form.get('cantidad'))
    

    repuesto = Repuesto.query.get_or_404(repuesto_id)
    

    if repuesto.stock < cantidad:
        flash(f'Error: No hay suficiente stock. Solo quedan {repuesto.stock}.', 'danger')
        return redirect(url_for('ordenes.ver_orden', id=id))
    

    detalle = DetalleOrden(
        orden_id=orden.id,
        repuesto_id=repuesto.id,
        cantidad=cantidad,
        precio_unitario=repuesto.precio
    )
    

    repuesto.stock = repuesto.stock - cantidad
    

    db.session.add(detalle)
    db.session.commit()
    
    flash('Repuesto agregado a la orden.', 'success')
    return redirect(url_for('ordenes.ver_orden', id=id))