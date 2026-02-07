from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Penghuni, Kamar, db
from app.decorators import petugas_required
from datetime import datetime

bp = Blueprint('penghuni', __name__)

@bp.route('/')
@login_required
def index():
    penghuni_list = Penghuni.query.all()
    return render_template('penghuni/index.html', penghuni_list=penghuni_list)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
@petugas_required
def add():
    kamar_list = Kamar.query.filter_by(status='Kosong').all()
    if request.method == 'POST':
        penghuni = Penghuni(
            nama=request.form.get('nama'),
            nik=request.form.get('nik'),
            no_hp=request.form.get('no_hp'),
            alamat=request.form.get('alamat'),
            tanggal_masuk=datetime.strptime(request.form.get('tanggal_masuk'), '%Y-%m-%d'),
            id_kamar=int(request.form.get('id_kamar')) if request.form.get('id_kamar') else None,
            status='Aktif'
        )
        if penghuni.id_kamar:
            kamar = Kamar.query.get(penghuni.id_kamar)
            kamar.status = 'Terisi'
        
        db.session.add(penghuni)
        db.session.commit()
        flash('Penghuni berhasil ditambahkan')
        return redirect(url_for('penghuni.index'))
    return render_template('penghuni/form.html', title='Tambah Penghuni', kamar_list=kamar_list)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@petugas_required
def edit(id):
    penghuni = Penghuni.query.get_or_404(id)
    kamar_list = Kamar.query.filter((Kamar.status == 'Kosong') | (Kamar.id == penghuni.id_kamar)).all()
    if request.method == 'POST':
        old_kamar_id = penghuni.id_kamar
        new_kamar_id = int(request.form.get('id_kamar')) if request.form.get('id_kamar') else None
        
        penghuni.nama = request.form.get('nama')
        penghuni.nik = request.form.get('nik')
        penghuni.no_hp = request.form.get('no_hp')
        penghuni.alamat = request.form.get('alamat')
        penghuni.tanggal_masuk = datetime.strptime(request.form.get('tanggal_masuk'), '%Y-%m-%d')
        penghuni.status = request.form.get('status')
        penghuni.id_kamar = new_kamar_id

        # Update room status
        if old_kamar_id != new_kamar_id:
            if old_kamar_id:
                old_k = Kamar.query.get(old_kamar_id)
                old_k.status = 'Kosong'
            if new_kamar_id:
                new_k = Kamar.query.get(new_kamar_id)
                new_k.status = 'Terisi'
        
        if penghuni.status == 'Nonaktif' and penghuni.id_kamar:
            k = Kamar.query.get(penghuni.id_kamar)
            k.status = 'Kosong'
            penghuni.id_kamar = None

        db.session.commit()
        flash('Penghuni berhasil diperbarui')
        return redirect(url_for('penghuni.index'))
    return render_template('penghuni/form.html', penghuni=penghuni, title='Edit Penghuni', kamar_list=kamar_list)
