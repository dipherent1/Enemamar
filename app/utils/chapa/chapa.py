from chapa import Chapa
from app.core.config.env import get_settings
import random
import string
settings = get_settings()
# Replace 'your_secret_key' with your actual Chapa secret key

def generete_tx_ref(length):
    #Generate a transaction reference
    tx_ref = string.ascii_lowercase
    return ''.join(random.choice(tx_ref) for i in range(length))

def pay_course(payment_data):
    data = {
		# Required fields
		'email': payment_data['email'], # customer/client email address
		'amount': payment_data['amount'], # total payment
		'first_name': payment_data['first_name'], # customer/client first name
		'last_name': payment_data['last_name'], # customer/client last name
		'tx_ref': payment_data['tx_ref'],  # Fixed syntax error by changing ')' to '}'
		
		# Optional fields
		'callback_url': payment_data['callback_url'], # after successful payment chapa will redirect your customer/client to this url
		'customization': {
			'title': payment_data['title'],  # Fixed syntax error by changing ')' to '}'
            'description': f'Payment for your course: {payment_data["title"]}',
            
		}
	}
    
    
    chapa = Chapa(settings.CHAPA_SECRET_KEY)
    response = chapa.initialize(**data)

    return response

def verify_payment(transaction_id):
    chapa = Chapa(settings.CHAPA_SECRET_KEY)
    verification_response = chapa.verify(transaction_id)
    return verification_response