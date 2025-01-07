from flask import Flask, render_template, request, jsonify
from weather_api import get_weather_data
from email_service import send_email
from auth import authenticate_email
from flask_bcrypt import Bcrypt
from flask_babel import Babel

app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel(app)
bcrypt = Bcrypt(app)

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to send umbrella reminder email
@app.route('/send_email', methods=['POST'])
def send_umbrella_reminder_email():
    email = request.form['email']
    password = request.form['password']
    language = request.form['language']

    if authenticate_email(email, password):
        weather_data = get_weather_data()
        if weather_data['weather'][0]['main'] == 'Rain':
            subject = _("Umbrella Reminder")
            body = _("Don't forget to carry an umbrella today!")
            send_email(email, subject, body)
            return jsonify({'message': _('Email sent!')})
        else:
            return jsonify({'message': _('No rain today!')})
    else:
        return jsonify({'message': _('Invalid email or password!')})

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['en', 'es', 'fr'])

if __name__ == '__main__':
    app.run(debug=True)