from chapa import Chapa
from app.core.config.env import get_settings
settings = get_settings()
# Replace 'your_secret_key' with your actual Chapa secret key
def pay(email, amount, first_name, last_name, tx_ref, callback_url):
    chapa = Chapa(settings.CHAPA_SECRET_KEY)
    
    response = chapa.initialize(
    email=email,
    amount=amount,
    first_name=first_name,
    last_name=last_name,
    tx_ref=tx_ref,
    callback_url=callback_url
    )

    print(response)

def verify(transaction_id):
    chapa = Chapa(settings.CHAPA_SECRET_KEY)
    verification_response = chapa.verify(transaction_id)
    print(verification_response)