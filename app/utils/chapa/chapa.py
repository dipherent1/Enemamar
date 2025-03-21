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
    print(payment_data.title)
    data = {
        # Required fields
        'email': payment_data.email,  # Use attribute-style access
        'amount': payment_data.amount,  # Use attribute-style access
        'first_name': payment_data.first_name,  # Use attribute-style access
        'last_name': payment_data.last_name,  # Use attribute-style access
        'tx_ref': payment_data.tx_ref,  # Use attribute-style access
        
        # Optional fields
        'callback_url': payment_data.callback_url,  # Use attribute-style access
        'customization': {
            'title': "Course Payment",  # Use attribute-style access
            'description': f'Payment for your course {payment_data.title}',  # Use attribute-style access
        }
    }
    
    
    chapa = Chapa(settings.CHAPA_SECRET_KEY)
    response = chapa.initialize(**data)

    return response

def verify_payment(transaction_id):
    chapa = Chapa(settings.CHAPA_SECRET_KEY)
    verification_response = chapa.verify(transaction_id)
    return verification_response