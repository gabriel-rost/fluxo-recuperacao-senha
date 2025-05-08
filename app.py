from flask import Flask, render_template, request, redirect, url_for, flash
import json, random, os

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_flash'

USERS_FILE = 'users_db.json'

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

def enviar_codigo(destino, meio):
    codigo = str(random.randint(100000, 999999))
    print(f"[SIMULADO] Código enviado para {meio} {destino}: {codigo}", flush=True)
    return codigo

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        email = request.form['email']
        users = load_users()
        if email in users:
            metodo = request.form['metodo']
            if metodo == 'email':
                codigo = enviar_codigo(email, 'email')
                users[email]['codigo'] = codigo
                save_users(users)
                return redirect(url_for('verificar_email', email=email))
            elif metodo == 'sms':
                telefone = users[email]['telefone']
                codigo = enviar_codigo(telefone, 'telefone')
                users[email]['codigo'] = codigo
                save_users(users)
                return redirect(url_for('verificar_sms', email=email))
            elif metodo == 'duplo':
                codigo_email = enviar_codigo(email, 'email')
                codigo_sms = enviar_codigo(users[email]['telefone'], 'telefone')
                users[email]['codigo_email'] = codigo_email
                users[email]['codigo_sms'] = codigo_sms
                save_users(users)
                return redirect(url_for('verificar_duplo', email=email))
        print('Usuário não encontrado.', flush=True)
    return render_template('forgot_password.html')

@app.route('/verificar_email/<email>', methods=['GET', 'POST'])
def verificar_email(email):
    if request.method == 'POST':
        codigo = request.form['codigo']
        nova_senha = request.form['senha']
        users = load_users()
        if codigo == users[email].get('codigo'):
            users[email]['senha'] = nova_senha
            save_users(users)
            print('Senha alterada com sucesso!', flush=True)
            return redirect(url_for('home'))
        print('Código inválido.', flush=True)
    return render_template('reset_email.html', email=email)

@app.route('/verificar_sms/<email>', methods=['GET', 'POST'])
def verificar_sms(email):
    if request.method == 'POST':
        codigo = request.form['codigo']
        nova_senha = request.form['senha']
        users = load_users()
        if codigo == users[email].get('codigo'):
            users[email]['senha'] = nova_senha
            save_users(users)
            print('Senha alterada com sucesso!', flush=True)
            return redirect(url_for('home'))
        print('Código inválido.', flush=True)
    return render_template('reset_sms.html', email=email)

@app.route('/verificar_duplo/<email>', methods=['GET', 'POST'])
def verificar_duplo(email):
    if request.method == 'POST':
        codigo_email = request.form['codigo_email']
        codigo_sms = request.form['codigo_sms']
        nova_senha = request.form['senha']
        users = load_users()
        if (codigo_email == users[email].get('codigo_email') and codigo_sms == users[email].get('codigo_sms')):
            users[email]['senha'] = nova_senha
            save_users(users)
            print('Senha alterada com sucesso!', flush=True)
            return redirect(url_for('home'))
        print('Códigos inválidos.', flush=True)
    return render_template('reset_double.html', email=email)

@app.route('/cadastrar')
def cadastrar():
    users = load_users()
    users['usuario@example.com'] = {'senha': '1234', 'telefone': '51999999999'}
    save_users(users)
    return 'Usuário cadastrado. <a href="/">Voltar</a>'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')