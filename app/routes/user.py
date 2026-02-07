from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import User, db
from app.decorators import admin_required

bp = Blueprint('user', __name__)

@bp.route('/')
@login_required
@admin_required
def index():
    users = User.query.all()
    return render_template('user/index.html', users=users)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add():
    if request.method == 'POST':
        user = User(
            username=request.form.get('username'),
            role=request.form.get('role')
        )
        user.set_password(request.form.get('password'))
        db.session.add(user)
        db.session.commit()
        flash('User berhasil ditambahkan')
        return redirect(url_for('user.index'))
    return render_template('user/form.html', title='Tambah User')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.username = request.form.get('username')
        user.role = request.form.get('role')
        if request.form.get('password'):
            user.set_password(request.form.get('password'))
        db.session.commit()
        flash('User berhasil diperbarui')
        return redirect(url_for('user.index'))
    return render_template('user/form.html', user=user, title='Edit User')

@bp.route('/delete/<int:id>')
@login_required
@admin_required
def delete(id):
    if id == current_user.id:
        flash('Tidak dapat menghapus diri sendiri')
        return redirect(url_for('user.index'))
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User berhasil dihapus')
    return redirect(url_for('user.index'))
