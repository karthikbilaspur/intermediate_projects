from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/configure', methods=['POST'])
def configure():
    config = request.get_json()
    # Save config to config.json
    return 'Configuration saved.'

if __name__ == '__main__':
    app.run()