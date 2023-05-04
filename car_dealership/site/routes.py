from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from car_dealership.forms import CarForm
from car_dealership.models import Car, db
# from car_dealership.helpers import random_joke_generator

site = Blueprint('site', __name__, template_folder='site_templates')



@site.route('/')
def home():
    print("ooga booga in the terminal")
    return render_template('index.html')

@site.route('/profile', methods = ['GET','POST'])
@login_required
def profile():
    my_car = CarForm()

    try:
        if request.method == 'POST' and my_car.validate_on_submit():
            color = my_car.color.data
            year = my_car.year.data
            make = my_car.make.data
            model = my_car.model.data
            user_token = current_user.token

            car = Car( color, year, make, model, user_token)
            # print(car)
            db.session.add(car)
            db.session.commit()

            return redirect(url_for('site.profile'))

    except:
        raise Exception('Car not added, please check your form and try again!') 

    current_user_token = current_user.token

    cars = Car.query.filter_by(user_token=current_user_token)

    return render_template('profile.html', form=my_car, cars = cars)