from flask import Flask,render_template
DIR_STATIC = ''
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')
@app.route('/profile')
def profile():
    return render_template('profile.html')
if __name__ == '__main__':
    app.run(debug=  True)