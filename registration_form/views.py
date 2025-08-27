from datetime import datetime

from flask import Blueprint, render_template, request

from .extensions import db

from .models import Language, Topic, Member

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
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

        print("Email:", email)
        print("Password:", password)
        print("Location:", location)
        print("First Learn Date:", first_learn_date)
        print("Favorite Language:", fav_language)
        print("About:", about)
        print("Learn New Interest:", learn_new_interest)
        print("Interest in Topics:", interest_in_topics)

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

        return "Form submitted!"
    
    languages = Language.query.all()
    topics = Topic.query.all()

    context = {
        'languages' : languages,
        'topics' : topics
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
