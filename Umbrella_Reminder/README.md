README.md
Umbrella Reminder
A Flask application that sends an umbrella reminder email based on the weather.
Features
Sends an umbrella reminder email if it's going to rain
Supports multiple languages (English, Spanish, French)
Uses password hashing for secure authentication
Uses Flask-Babel for translation management
Requirements
Python 3.8+
Flask 2.0+
Flask-Babel 2.0+
Flask-Bcrypt 1.0+
requests 2.25+
beautifulsoup4 4.9+
Installation
Clone the repository: git clone https://github.com/your-username/umbrella-reminder.git
Install the requirements: pip install -r requirements.txt
Create a .env file with your email credentials and weather API key
Run the application: flask run
Usage
Open the application in your web browser: http://localhost:5000
Enter your email address and password
Select your language preference
Click the "Send Umbrella Reminder Email" button
