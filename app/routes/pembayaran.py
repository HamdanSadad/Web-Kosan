from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Pembayaran, Penghuni, db
from app.decorators import petugas_required
from datetime import datetime

bp = Blueprint('pembayaran', __name__)

@bp.route('/')
@login_required
def index():
    pembayaran_list = Pembayaran.query.order_by(Pembayaran.tanggal_bayar.desc()).all()
    return render_template('pembayaran/index.html', pembayaran_list=pembayaran_list)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
@petugas_required
def add():
    penghuni_list = Penghuni.query.filter_by(status='Aktif').all()
    if request.method == 'POST':
        pembayaran = Pembayaran(
            id_penghuni=int(request.form.get('id_penghuni')),
            bulan=request.form.get('bulan'),
            jumlah_bayar=float(request.form.get('jumlah_bayar')),
            status=request.form.get('status'),
            denda=float(request.form.get('denda', 0.0)),
            tanggal_bayar=datetime.now()
        )
        db.session.add(pembayaran)
        db.session.commit()
        flash('Pembayaran berhasil dicatat')
        return redirect(url_for('pembayaran.index'))
    return render_template('pembayaran/form.html', title='Catat Pembayaran', penghuni_list=penghuni_list)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@petugas_required
def edit(id):
    pembayaran = Pembayaran.query.get_or_404(id)
    penghuni_list = Penghuni.query.filter_by(status='Aktif').all()
    if request.method == 'POST':
        pembayaran.id_penghuni = int(request.form.get('id_penghuni'))
        pembayaran.bulan = request.form.get('bulan')
        pembayaran.jumlah_bayar = float(request.form.get('jumlah_bayar'))
        pembayaran.status = request.form.get('status')
        pembayaran.denda = float(request.form.get('denda', 0.0))
        db.session.commit()
        flash('Pembayaran berhasil diperbarui')
        return redirect(url_for('pembayaran.index'))
    return render_template('pembayaran/form.html', pembayaran=pembayaran, title='Edit Pembayaran', penghuni_list=penghuni_list)
