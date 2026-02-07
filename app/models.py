from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(255))
    role = db.Column(db.Enum('admin', 'petugas', 'penghuni'), default='penghuni')
    id_penghuni = db.Column(db.Integer, db.ForeignKey('penghuni.id'), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Kamar(db.Model):
    __tablename__ = 'kamar'
    id = db.Column(db.Integer, primary_key=True)
    nomor_kamar = db.Column(db.String(10), unique=True, index=True)
    tipe_kamar = db.Column(db.String(50))
    harga = db.Column(db.Float)
    status = db.Column(db.Enum('Kosong', 'Terisi', 'Nonaktif'), default='Kosong')
    fasilitas = db.Column(db.Text)
    pos_x = db.Column(db.Integer, default=0)
    pos_y = db.Column(db.Integer, default=0)
    
    penghuni = db.relationship('Penghuni', backref='kamar', lazy='dynamic')

class Penghuni(db.Model):
    __tablename__ = 'penghuni'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), index=True)
    nik = db.Column(db.String(20), unique=True)
    no_hp = db.Column(db.String(20))
    alamat = db.Column(db.Text)
    tanggal_masuk = db.Column(db.Date, default=datetime.utcnow)
    id_kamar = db.Column(db.Integer, db.ForeignKey('kamar.id'))
    status = db.Column(db.Enum('Aktif', 'Nonaktif'), default='Aktif')
    
    user = db.relationship('User', backref='penghuni', uselist=False)
    pembayaran = db.relationship('Pembayaran', backref='penghuni', lazy='dynamic')

class Pembayaran(db.Model):
    __tablename__ = 'pembayaran'
    id = db.Column(db.Integer, primary_key=True)
    id_penghuni = db.Column(db.Integer, db.ForeignKey('penghuni.id'))
    bulan = db.Column(db.String(20)) # e.g., "Januari 2024"
    jumlah_bayar = db.Column(db.Float)
    tanggal_bayar = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum('Lunas', 'Belum Lunas'), default='Belum Lunas')
    denda = db.Column(db.Float, default=0.0)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
