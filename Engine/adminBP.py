from flask import Flask, request, Blueprint, render_template ,flash, jsonify, current_app, session
from Database.Handlers.UserHandler import UserHandler
from Model.User import User
from Database.Handlers.CardHandler import CardHandler
from Database.Handlers.ComplexHandler import ComplexHandler
from Enums.ReturnValues import ReturnValues
userHandler = UserHandler()
cardHandler = CardHandler()
from Database.Handlers.TransactionHandler import TransactionHandler
transactionHandler = TransactionHandler()
complexHandler = ComplexHandler()

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/create-user', methods=['POST'])
def register():
    if not session.get('email'):
        return jsonify({'error': 'Unauthorized access, not logged in'}), 401
    elif session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized access, must be admin user'}), 401
    email = request.form.get('email')
    password = request.form.get('password')
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    error = None

    if not email:
        error = 'Email is required.'
    elif not password:
        error = 'Password is required.'
    elif not firstName:
        error = 'First name is required.'    
    elif not lastName:
        error = 'Last name is required.'        
    if error is None:
        user = User(email, password, firstName, lastName)
        with current_app.app_context(): 
            mail = current_app.extensions['mail']
            returnValue = userHandler.insert(user, mail)
            if(returnValue == ReturnValues.alreadyExists):
                return jsonify({'error': 'User already exists'}), 409
            if(returnValue == ReturnValues.exception):
                return jsonify({'error': 'unexpected exeption'}), 400
            else:
                return jsonify({'message': 'User registered successfully'}), 201
    return jsonify({'error': error}), 400
    
@bp.route('/verifyAccount', methods=['PUT'])
def verify():
        if not session.get('email'):
            return jsonify({'error': 'Unauthorized access, not logged in'}), 401
        elif session.get('role') != 'admin':
            return jsonify({'error': 'Unauthorized access, must be admin user'}), 401
        card = request.form.get('card') 
        if len(card) != 16:
            return jsonify({'error': 'card must have 16 digits.'}), 400

        if cardHandler.verify(card) == ReturnValues.exception: 
             return jsonify({'error': 'Unexpected error'}), 400
        else:
            return jsonify({'message': 'User varified successfully'}), 201
        
@bp.route('/getUnverifiedCardsWithOwner', methods=['GET'])    
def addCard():
    if not session.get('email'):
        return jsonify({'error': 'Unauthorized access, not logged in'}), 401
    elif session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized access, must be admin user'}), 401
    else:
        returnValue = complexHandler.readUnverifiedCardsWithOwnerData()
        if returnValue == ReturnValues.exception:  
            return jsonify({'error': 'Unexpected error'}), 400
        else:
            serialized_data = [card.__dict__ for card in returnValue]
            return jsonify(serialized_data), 201
