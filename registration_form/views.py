from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for

from .extensions import db

from .models import Language, Topic, Member

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'], defaults = {'member_id' : None})
@main.route('/<int:member_id>', methods=['GET', 'POST'])
def index(member_id):

    member = None
    if member_id:
        member = Member.query.get_or_404(member_id) # get member info if member_id is provided else 404 error

    errors = {}

    if request.method == "POST":
        # geather all info
        email = request.form['email']
        password = request.form['password']
        location = request.form['location']
        first_learn_date = request.form['first_learn_date']
        fav_language = request.form['fav_language']
        about = request.form['about']
        learn_new_interest = request.form['learn_new_interest']
        interest_in_topics = request.form.getlist('interest_in_topics')

        # print("Email:", email)
        # print("Password:", password)
        # print("Location:", location)
        # print("First Learn Date:", first_learn_date)
        # print("Favorite Language:", fav_language)
        # print("About:", about)
        # print("Learn New Interest:", learn_new_interest)
        # print("Interest in Topics:", interest_in_topics)

        if not email:
            errors['email'] = "Email is required."
        if not password and not member_id:
            errors['password'] = "Password is required."
        if not location:
            errors['location'] = "Location is required."
        if not first_learn_date:
            errors['first_learn_date'] = "First Learn Date is required."
        if not about:
            errors['about'] = "About is required."
        if not interest_in_topics:
            errors['interest_in_topics'] = "Please select at least one topic."
        

        if not errors:
            if member:
                member.email = email
                if password:
                    member.password = password
                member.location = location
                member.first_learn_date = datetime.strptime(first_learn_date, '%Y-%m-%d')
                member.fav_language = fav_language
                member.about = about
                member.learn_new_interest = True if learn_new_interest == 'yes' else False

                member.interest_in_topics[:] = []

            else:
            # save to database
                member = Member(
                    email = email,
                    password = password,
                    location = location,
                    first_learn_date = datetime.strptime(first_learn_date, '%Y-%m-%d'),# Convert string to date
                    fav_language = fav_language,
                    about = about,
                    learn_new_interest = (
                        True if learn_new_interest == 'yes' else False
                    )
                                    )

                db.session.add(member)

            for topic_id in interest_in_topics:
                topic = Topic.query.get(int(topic_id))
                member.interest_in_topics.append(topic)

            db.session.commit()

            return redirect(url_for('main.index', member_id=member.id))
    
    languages = Language.query.all()
    topics = Topic.query.all()

    context = {
        'member_id' : member_id,
        'languages' : languages,
        'topics' : topics,
        'member' : member,
        'errors' : errors
    }
    return render_template('form.html', **context)






# '''Alternative version using JSON data'''


# from flask import Blueprint, request, jsonify

# main = Blueprint('main', __name__)

# @main.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == "POST":
#         data = request.get_json()  # Get JSON data from request body
#         email = data.get('email')
#         password = data.get('password')
#         location = data.get('location')
#         first_learn_date = data.get('first_learn_date')
#         fav_language = data.get('fav_language')
#         about = data.get('about')
#         learn_new_interest = data.get('learn_new_interest')
#         interest_in_topics = data.get('interest_in_topics', [])
        
#         # Here, you can add validation and save data to the database
        
#         return jsonify({"message": "Form submitted!", "data": data}), 200
    
#     return jsonify({"message": "Send a POST request with JSON data"}), 200
