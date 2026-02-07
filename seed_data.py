from app import create_app, db
from app.models import Kamar, Penghuni, Pembayaran
from datetime import date

app = create_app()
with app.app_context():
    # Sample Rooms
    rooms = [
        Kamar(nomor_kamar='10', tipe_kamar='VIP', harga=1500000, status='Terisi', fasilitas='AC, KM Dalam, WiFi', pos_x=12, pos_y=35),
        Kamar(nomor_kamar='09', tipe_kamar='Standar', harga=1000000, status='Kosong', fasilitas='Kipas, KM Luar', pos_x=26, pos_y=35),
        Kamar(nomor_kamar='08', tipe_kamar='Standar', harga=1000000, status='Kosong', fasilitas='Kipas, KM Luar', pos_x=40, pos_y=35),
        Kamar(nomor_kamar='07', tipe_kamar='Standar', harga=1000000, status='Kosong', fasilitas='Kipas, KM Luar', pos_x=54, pos_y=35),
        Kamar(nomor_kamar='06', tipe_kamar='Standar', harga=1200000, status='Kosong', fasilitas='Kipas, KM Dalam', pos_x=68, pos_y=35),
        
        Kamar(nomor_kamar='11', tipe_kamar='VIP', harga=1500000, status='Kosong', fasilitas='AC, KM Dalam, WiFi', pos_x=12, pos_y=68),
        Kamar(nomor_kamar='12', tipe_kamar='Standar', harga=1000000, status='Kosong', fasilitas='Kipas, KM Luar', pos_x=26, pos_y=68),
        Kamar(nomor_kamar='13', tipe_kamar='Standar', harga=1000000, status='Kosong', fasilitas='Kipas, KM Luar', pos_x=40, pos_y=68),
        Kamar(nomor_kamar='14', tipe_kamar='Standar', harga=1000000, status='Kosong', fasilitas='Kipas, KM Luar', pos_x=54, pos_y=68),
        Kamar(nomor_kamar='15', tipe_kamar='Standar', harga=1200000, status='Kosong', fasilitas='Kipas, KM Dalam', pos_x=68, pos_y=68),
    ]
    
    for r in rooms:
        if not Kamar.query.filter_by(nomor_kamar=r.nomor_kamar).first():
            db.session.add(r)
    
    db.session.commit()
    
    # Sample Resident in Room 10
    k10 = Kamar.query.filter_by(nomor_kamar='10').first()
    if not Penghuni.query.filter_by(nik='123456789').first():
        p1 = Penghuni(nama='Budi Santoso', nik='123456789', no_hp='08123456789', alamat='Jakarta', tanggal_masuk=date(2024, 1, 1), id_kamar=k10.id, status='Aktif')
        db.session.add(p1)
        db.session.commit()
        
        # Sample Payment
        pay = Pembayaran(id_penghuni=p1.id, bulan='Januari 2024', jumlah_bayar=1500000, status='Lunas')
        db.session.add(pay)
        db.session.commit()

    print("Sample data seeded.")
