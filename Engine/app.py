from Database.Handlers.ComplexHandler import ComplexHandler
from flask import Flask, session, jsonify, request, current_app
from flask_session import Session
from flask_mail import Mail
from flask_cors import CORS
from flask_socketio import SocketIO
from Utils.EmailSender import EmailSender
from Database.Handlers.AdminHandler import AdminHandler
from Database.Handlers.BalanceHandler import BalanceHandler
from Database.Handlers.UserHandler import UserHandler
from Database.Handlers.TransactionHandler import TransactionHandler
from Enums.ReturnValues import ReturnValues
from adminBP import bp
from userBP import bp1
import json
import re
from DTOs.TransactionWithUserDataDTO import TransactionWithUserDataDTO
emailSender = EmailSender() 
userHandler = UserHandler()
adminHandler = AdminHandler()
balanceHandler = BalanceHandler()
transactionHandler = TransactionHandler()

from multiprocessing import Process, Queue, freeze_support
from time import sleep
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
sharedQueue = Queue()
app.register_blueprint(bp)
app.register_blueprint(bp1)

app.config.from_pyfile('config.py')
mail = Mail(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@db:3307/drs'
Session(app)
CORS(app, supports_credentials=True)
# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

@app.route('/')
def hello():
    return 'Hello!'

@app.route('/SendMail')
def send():
    return emailSender.sendEmailCredentials("1dragangavric@gmail.com", "password", mail)

@app.route('/getLogedInUserData', methods=['GET'])
def getData():
    if not session.get('email'):
        return jsonify({'error': 'Not loged in'}), 401
    elif(session.get('role') == 'admin'):
        admin = adminHandler.read(session.get('email'))
        if(admin == ReturnValues.exception):
            return jsonify({'error': 'Unexpected error'}), 404
        serialized_data = [admin.__dict__]
        return jsonify(serialized_data), 200
    else:
         user = userHandler.read(session.get('email'))
         if(user == ReturnValues.exception):
            return jsonify({'error': 'Unexpected error'}), 404
         serialized_data = [user.__dict__]
         return jsonify(serialized_data), 200

@app.route('/login', methods=['POST'])
def checkCredentials():
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')
    if(role == 'admin'):
        admin = adminHandler.read(email)
        if(admin == ReturnValues.doesntExist):
            return jsonify({'error': 'Username does not exist'}), 404
        if(admin == ReturnValues.exception):
            return jsonify({'error': 'Unexpected error'}), 404
        if(admin.password != password):
            return jsonify({'error': 'wrong password'}), 401
        session['email'] = admin.email
        session['role'] = role
        admin_instance = admin
        admin_dict = {
        "email": admin_instance.email,
        "password": admin_instance.password,
        "firstName": admin_instance.firstName,
        "lastName": admin_instance.lastName,
        "address": admin_instance.address,
        "city": admin_instance.city,
        "country": admin_instance.country,
        "phoneNum": admin_instance.phoneNum,
        }
        return jsonify(admin=admin_dict), 200
    elif(role == 'user'):
        user = userHandler.read(email)
        if(user == ReturnValues.doesntExist):
            return jsonify({'error': 'Username does not exist'}), 404
        if(user == ReturnValues.exception):
            return jsonify({'error': 'Unexpected error'}), 404
        if(user.password != password):
            return jsonify({'error': 'wrong password'}), 401
        session['email'] = user.email
        session['role'] = role
        user_instance = user
        user_dict = {
        "email": user_instance.email,
        "password": user_instance.password,
        "firstName": user_instance.firstName,
        "lastName": user_instance.lastName,
        }
        return jsonify(user=user_dict), 200
    else:
        return jsonify({'error': 'Role does not exist'}), 404

# Periodicno poziva executeUnexecutedTransactions() i stavlja izvrsene transakcije u sharedQueue, da bi ih emitter procitao i emit-ovao
def executioner(sharedQueue):
    complexHandler = ComplexHandler()
    try:
        while True:
            with app.app_context():
                mail = current_app.extensions['mail']
                transactionsWithUserData = complexHandler.executeUnexecutedTransactions(mail)
                if transactionsWithUserData:
                    sharedQueue.put(transactionsWithUserData)
                    print(sharedQueue)

            sleep(10)
    except KeyboardInterrupt:
        return

# Define the emitter function
def emitter():
    try:
        while True:
            if not sharedQueue.empty():
                transactionsWithUserData = sharedQueue.get()
                serialized_data = [TransactionWithUserDataDTO( transaction=td.transaction.to_dict(), sender=td.sender.__dict__, receiver=td.receiver.__dict__).__dict__ for td in transactionsWithUserData]
                print("executing...")
                socketio.emit('freshly_executed_transactions', serialized_data)
                print("executed")
            sleep(1)
    except KeyboardInterrupt:
        return

if __name__ == '__main__':
    freeze_support()
    import os
    HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5000'))
    except ValueError:
        PORT = 5000

    with app.app_context():
        executioner_process = Process(target=executioner, args=[sharedQueue])
        executioner_process.daemon = True
        executioner_process.start()

    socketio.start_background_task(target=emitter)
    socketioThread = Thread()
    socketioThread.daemon = True
    socketioThread.start()
    socketioThread.join()

    socketio.run(app, HOST, PORT, debug=False)