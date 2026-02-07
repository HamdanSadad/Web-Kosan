from app import create_app, db
from app.models import User, Kamar, Penghuni, Pembayaran

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Kamar': Kamar, 'Penghuni': Penghuni, 'Pembayaran': Pembayaran}

if __name__ == '__main__':
    app.run(debug=True)
