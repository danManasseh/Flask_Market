from os import abort
from types import MethodDescriptorType
from market.forms import LoginForm, PurchaseItemForm, RegisterForm, UpdateItemForm
from . import app
from market.models import Item, User
from flask import flash, redirect, render_template, request, url_for
from market import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/market", methods = ['GET', 'POST'])
@login_required
def market():
    user_items = Item.query.filter_by(owner = current_user.id)
    items = Item.query.filter_by(owner = None)
    update_item_form = UpdateItemForm()
    purchase_form = PurchaseItemForm()
    if purchase_form.validate_on_submit():
        item_id = request.form['purchased_item']
        item = Item.query.filter_by(id = item_id).first()
        item_price = item.price
        if current_user.budget >= item_price:
            current_user.budget -= item_price
            item.owner = current_user.id
            db.session.commit()
            flash('Item purhcased!', category='success')
        else:
            flash('You don\'t have enough funds to purchase this item', category='danger')
    elif purchase_form.errors:
        for err in purchase_form.errors.values():
            flash(f'{err}')

    return render_template('market.html', items = items, purchase_form = purchase_form,
                           user_items=user_items, update_item_form = update_item_form)

@app.route('/market/item/<item_id>/update', methods= ['POST'])
@login_required
def update(item_id):
    update_item_form = UpdateItemForm()
    if update_item_form.validate_on_submit():
        item_to_update = Item.query.filter_by(id = item_id).first()
        item_to_update.name = update_item_form.name.data
        item_to_update.price = update_item_form.price.data
        item_to_update.barcode = update_item_form.barcode.data
        item_to_update.description = update_item_form.description.data
        db.session.commit()
        flash('Item successfully updated!', category='success')
    elif update_item_form.errors:
        for err in update_item_form.errors.values():
            flash(f'Update Unsuccessful!:{err}', category='danger')
    return redirect(url_for('market'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email_address.data
        password1 = form.password1.data
        user_to_create=User(username=username, email_address=email, password=password1)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash('Welcome to the FlaskMarket!', category='info')
        return redirect(url_for('market'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user:{err_msg}', category='danger')
    return render_template('register.html', form = form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        find_user = User.query.filter_by(username=username).first()
        if find_user and find_user.check_password_correction(attempted_password = password):
            login_user(find_user)
            flash(f'Welcome back, {username.title()}', category='success')
            return redirect(url_for('market'))
        else:
            flash('Username and Password do not match. Please try again!', category='danger')
    if form.errors != {}:
        for errs in form.errors.values():
            flash(f'There was an error with the login:{errs}', category='danger')
    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    flash('User has been logged successfully!', category='info')
    return redirect('/')