# 🔐 Sistema de Recuperação de Senha com Flask
Este é um protótipo de sistema web feito com Flask que simula um processo de recuperação de senha via e-mail, SMS ou verificação dupla (e-mail + SMS). Os dados dos usuários são armazenados em um arquivo JSON (users_db.json).
## ⚙️ Funcionalidades
* Tela de login (simulada).
* Página de recuperação de senha com 3 métodos:
    * Apenas e-mail
    * Apenas SMS
    * Duplo fator (e-mail + SMS)
* Verificação de código enviado (simulado no terminal).
* Redefinição de senha.
* Cadastro de usuário de teste (/cadastrar).
## 🗂 Estrutura
* ```app.py```: aplicação principal Flask.
* ```users_db.json```: banco de dados simulado em JSON.
### Templates:
* ```login.html```
* ```forgot_password.html```
* ```reset_email.html```
* ```reset_sms.html```
* ```reset_double.html```
## 📦 Rodando o Container
* ```docker-compose build```
* ```docker-compose up```