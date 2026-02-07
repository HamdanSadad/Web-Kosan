from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Kamar, Penghuni, Pembayaran

bp = Blueprint('dashboard', __name__)

@bp.route('/')
@bp.route('/dashboard')
@login_required
def index():
    if current_user.role == 'admin':
        # Admin stats
        total_kamar = Kamar.query.count()
        kamar_terisi = Kamar.query.filter_by(status='Terisi').count()
        kamar_kosong = total_kamar - kamar_terisi
        total_penghuni = Penghuni.query.filter_by(status='Aktif').count()
        tunggakan = Pembayaran.query.filter_by(status='Belum Lunas').count()
        kamar_list = Kamar.query.all()
        return render_template('dashboard/admin.html', 
                             total_kamar=total_kamar,
                             kamar_terisi=kamar_terisi,
                             kamar_kosong=kamar_kosong,
                             total_penghuni=total_penghuni,
                             tunggakan=tunggakan,
                             kamar_list=kamar_list)
    elif current_user.role == 'petugas':
        total_kamar = Kamar.query.count()
        kamar_terisi = Kamar.query.filter_by(status='Terisi').count()
        total_penghuni = Penghuni.query.filter_by(status='Aktif').count()
        return render_template('dashboard/petugas.html',
                             total_kamar=total_kamar,
                             kamar_terisi=kamar_terisi,
                             total_penghuni=total_penghuni)
    else:
        # Penghuni stats
        penghuni = Penghuni.query.get(current_user.id_penghuni) if current_user.id_penghuni else None
        tagihan = Pembayaran.query.filter_by(id_penghuni=current_user.id_penghuni, status='Belum Lunas').all() if current_user.id_penghuni else []
        return render_template('dashboard/penghuni.html', penghuni=penghuni, tagihan=tagihan)
