from flask import Flask, request, Blueprint, session, render_template ,flash, jsonify, current_app
from Database.Handlers.UserHandler import UserHandler
from Database.Handlers.CardHandler import CardHandler
from Database.Handlers.ComplexHandler import ComplexHandler
from Database.Handlers.BalanceHandler import BalanceHandler
from Database.Handlers.TransactionHandler import TransactionHandler
from Model.User import User
from Enums.ReturnValues import ReturnValues
userHandler = UserHandler()
cardHandler = CardHandler()
complexHandler = ComplexHandler()
balanceHandler = BalanceHandler()
transactionHandler = TransactionHandler()
from Model.Transaction import Transaction
from datetime import datetime

bp1 = Blueprint('user', __name__, url_prefix='/user')

@bp1.route('/addCard', methods=['POST'])     #kad se dogovorimo kako, treba podrzati ubacivanje vise kartica
def addCard():
    if not session.get('email'):
        return jsonify({'error': 'Unauthorized access, not logged in'}), 401
    elif session.get('role') != 'user':
        return jsonify({'error': 'Unauthorized access, must be a user'}), 401
    else:
        card = request.form.get('card') 
        email = session.get('email')
        if len(card) != 16:
            return jsonify({'error': '16 digits are required.'}), 400
        returnValue = cardHandler.setOwnerEmail(card, email)
        if returnValue == ReturnValues.alreadyExists:      
            return jsonify({'error': 'Card is already in use'}), 409
        elif returnValue == ReturnValues.exception:  
            return jsonify({'error': 'Unexpected error'}), 400
        elif returnValue == ReturnValues.doesntExist:
            return jsonify({'error': 'The card number you entered does not exist'}), 400
        else:
            return jsonify({'message': 'Successfully added credit card'}), 201


@bp1.route('/updateProfile', methods=['PUT'])   
def update():
    if not session.get('email'):
        return jsonify({'error': 'Unauthorized access, not logged in'}), 401
    elif session.get('role') != 'user':
        return jsonify({'error': 'Unauthorized access, must be a user'}), 401
    else:
        oldEmail = session.get('email')
        email = request.form.get('email')  
        password = request.form.get('password')   
        firstName = request.form.get('firstName')  
        lastName = request.form.get('lastName') 
        if not email:
            return jsonify({'error': 'Email is required.'}), 400
        elif not password:
            return jsonify({'error': 'Password is required'}), 400
        elif not firstName:
            return jsonify({'error': 'First name is required'}), 400
        if not lastName:
            return jsonify({'error': 'Last name is required'}), 400
        user = User(email, password, firstName, lastName)
        returnValue = userHandler.update(oldEmail, user)
        if returnValue == ReturnValues.alreadyExists:       
            return jsonify({'error': 'User with the same email already exists'}), 409
        elif returnValue == ReturnValues.exception:  
            return jsonify({'error': 'Unexpected error'}), 400
        else:
            session['email'] = email
            return jsonify({'message': 'Successfully updated'}), 200


@bp1.route('/balanceOverview', methods=['GET'])   
def overview():
    if not session.get('email'):
        return jsonify({'error': 'Unauthorized access, not logged in'}), 401
    elif session.get('role') != 'user':
        return jsonify({'error': 'Unauthorized access, must be a user'}), 401
    else:
        returnValue = complexHandler.readCardsAndBalancesOfUser(session['email'])
        serialized_data = [card.__dict__ for card in returnValue]
        if returnValue == ReturnValues.exception:  
            return jsonify({'error': 'Unexpected error'}), 400
        else:
            return jsonify(serialized_data), 200
    
@bp1.route('/MakeDeposit', methods=['PUT'])    
def deposit():
    if not session.get('email'):
        return jsonify({'error': 'Unauthorized access, not logged in'}), 401
    elif session.get('role') != 'user':
        return jsonify({'error': 'Unauthorized access, must be a user'}), 401
    else:
        card = request.form.get('card') 
        check = request.form.get('check') 
        if len(card) != 16:
            return jsonify({'error': '16 digits are required for a card.'}), 400
        if len(check) != 15:
            return jsonify({'error': '15 digits are required for a check.'}), 400
        returnValue = balanceHandler.depositWithCheck(check, card)
        if returnValue == ReturnValues.doesntExist:    
            return jsonify({'error': 'Check code does not exist'}), 409
        elif returnValue == ReturnValues.cardNotVerified:   
            return jsonify({'error': 'Card is not verified'}), 400
        elif returnValue == ReturnValues.exception:  
            return jsonify({'error': 'Unexpected error'}), 400
        else:
            return jsonify({'message': 'Successfully added made deposit'}), 201
        
@bp1.route('/Convert', methods=['PUT'])    
def convert():
    if not session.get('email'):
        return jsonify({'error': 'Unauthorized access, not logged in'}), 401
    elif session.get('role') != 'user':
        return jsonify({'error': 'Unauthorized access, must be a user'}), 401
    else:
        card = request.form.get('card') 
        amount = request.form.get('amount')
        currencyFrom = request.form.get('currencyFrom')
        currencyTo = request.form.get('currencyTo')
        if len(card) != 16:
            return jsonify({'error': '16 digits are required.'}), 400
        if not amount:
            return jsonify({'error': 'amount is required.'}), 400
        if not currencyFrom:
            return jsonify({'error': 'Currency from is required.'}), 400
        if not currencyTo:
            return jsonify({'error': 'Currency to is required.'}), 400      
        if (currencyFrom == currencyTo):
            return jsonify({"error": 'Cannot convert to the same currency'}), 400  
        try:
            amount = int(amount)
        except ValueError:
            return jsonify({'error': 'Amount must be a valid integer.'}), 400
        returnValue = balanceHandler.convert(card, currencyFrom, currencyTo, amount)
        if returnValue == ReturnValues.cardNotVerified:    
            return jsonify({'error': 'Card is not verified'}), 400
        if returnValue == ReturnValues.insufficientFunds:    
            return jsonify({'error': 'Insufficient Funds'}), 400
        elif returnValue == ReturnValues.exception:  
            return jsonify({'error': 'Unexpected error'}), 400
        else:
            return jsonify({'message': 'Successfully converted funds'}), 200


@bp1.route('/MakeTransaction', methods=['POST'])    
def transaction():
    if not session.get('email'):
        return jsonify({'error': 'Unauthorized access, not logged in'}), 401
    elif session.get('role') != 'user':
        return jsonify({'error': 'Unauthorized access, must be a user'}), 401
    else:
        #card = request.form.get('card') 
        amount = request.form.get('amount')
        currency = request.form.get('currency')
        senderCardNum = request.form.get('senderCardNum')
        receiverCardNum = request.form.get('receiverCardNum')
        receiverEmail = request.form.get('receiverEmail')
        receiverFirstName = request.form.get('receiverFirstName')
        receiverLastName = request.form.get('receiverLastName')
        #if len(card) != 16:
            #return jsonify({'error': '16 digits are required.'}), 400
        if not amount:
            return jsonify({'error': 'amount is required.'}), 400
        if not currency:
            return jsonify({'error': 'Currency from is required.'}), 400
        if not senderCardNum:
            return jsonify({'error': 'Sender Card Num to is required.'}), 400  
        if not receiverCardNum:
            return jsonify({'error': 'Receiver Card Num to is required.'}), 400  
        if not receiverEmail:
            return jsonify({'error': 'Receiver email is required.'}), 400 
        if not receiverFirstName:
            return jsonify({'error': 'Receiver first name is required.'}), 400 
        if not receiverLastName:
            return jsonify({'error': 'Receiver last name is required.'}), 400 
        
        returnValue = transactionHandler.insert(senderCardNum, receiverCardNum, currency, float(amount), receiverEmail, receiverFirstName, receiverLastName)
        if returnValue == ReturnValues.cardNotVerified:  
            return jsonify({'error': 'Card is not verified.'}), 400  
        elif returnValue == ReturnValues.doesntExist:    
            return jsonify({'error': 'Card does not exist.'}), 400
        elif returnValue == ReturnValues.unexecutedTransactionAlreadyExists:    
            return jsonify({'error': 'Transaction already exists.'}), 400
        elif returnValue == ReturnValues.insufficientFunds:    
            return jsonify({'error': 'Insufficient Funds.'}), 400
        elif returnValue == ReturnValues.emailInvalid:
            return jsonify({'error': 'Invalid email.'}), 400
        elif returnValue == ReturnValues.firstNameInvalid:
            return jsonify({'error': 'Invalid first name.'}), 400
        elif returnValue == ReturnValues.lastNameInvalid:
            return jsonify({'error': 'Invalid last name.'}), 400
        elif returnValue == ReturnValues.exception:  
            return jsonify({'error': 'Unexpected error.'}), 400
        else:
            return jsonify({'message': 'Successfully started transaction'}), 200 
