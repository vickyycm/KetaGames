from flask import Flask, render_template

app = Flask(__name__, template_folder='vistas')
app.config.from_object('config.Config')

@app.route('/')
def index():
    """Página de inicio"""
    return render_template('index.html')


@app.route('/auth/login')
def login():
    """Página de login"""
    return render_template('auth/login.html')


@app.route('/auth/registro')
def registro():
    """Página de registro"""
    return render_template('auth/registro.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
