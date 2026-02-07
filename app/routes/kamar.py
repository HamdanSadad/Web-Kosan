from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Kamar
from app import db
from app.decorators import petugas_required, admin_required

bp = Blueprint('kamar', __name__)

@bp.route('/')
@login_required
def index():
    kamar_list = Kamar.query.all()
    return render_template('kamar/index.html', kamar_list=kamar_list)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
@petugas_required
def add():
    if request.method == 'POST':
        kamar = Kamar(
            nomor_kamar=request.form.get('nomor_kamar'),
            tipe_kamar=request.form.get('tipe_kamar'),
            harga=float(request.form.get('harga')),
            status=request.form.get('status'),
            fasilitas=request.form.get('fasilitas'),
            pos_x=int(request.form.get('pos_x', 0)),
            pos_y=int(request.form.get('pos_y', 0))
        )
        db.session.add(kamar)
        db.session.commit()
        flash('Kamar berhasil ditambahkan')
        return redirect(url_for('kamar.index'))
    return render_template('kamar/form.html', title='Tambah Kamar')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@petugas_required
def edit(id):
    kamar = Kamar.query.get_or_404(id)
    if request.method == 'POST':
        kamar.nomor_kamar = request.form.get('nomor_kamar')
        kamar.tipe_kamar = request.form.get('tipe_kamar')
        kamar.harga = float(request.form.get('harga'))
        kamar.status = request.form.get('status')
        kamar.fasilitas = request.form.get('fasilitas')
        kamar.pos_x = int(request.form.get('pos_x', 0))
        kamar.pos_y = int(request.form.get('pos_y', 0))
        db.session.commit()
        flash('Kamar berhasil diperbarui')
        return redirect(url_for('kamar.index'))
    return render_template('kamar/form.html', kamar=kamar, title='Edit Kamar')

@bp.route('/delete/<int:id>')
@login_required
@admin_required
def delete(id):
    kamar = Kamar.query.get_or_404(id)
    db.session.delete(kamar)
    db.session.commit()
    flash('Kamar berhasil dihapus')
    return redirect(url_for('kamar.index'))

@bp.route('/denah')
@login_required
def denah():
    kamar_list = Kamar.query.all()
    return render_template('kamar/denah.html', kamar_list=kamar_list)
