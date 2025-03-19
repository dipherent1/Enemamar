import requests  
from app.core.config.env import get_settings


setting = get_settings()
def send_otp_sms(phone_number: str):
    # Send OTP SMS
        # we use requests library for the samples
    # session object
    session = requests.Session()
    # base url
    base_url = 'https://api.afromessage.com/api/challenge'
    # api token
    token = setting.SMS_TOKEN
    # header
    headers = {'Authorization': 'Bearer ' + token}
    # request parameters
    callback = ""
    form_id = setting.SMS_ID
    sender = ""
    to = phone_number
    pre = " Hello, your OTP is: " 
    post = " Thank you for using our service."
    sb = 0
    sa = 0
    ttl = 100
    len = 6
    t = 0
    # final url
    url = '%s?from=%s&sender=%s&to=%s&pr=%s&ps=%s&callback=%s&sb=%d&sa=%d&ttl=%d&len=%d&t=%d' % (base_url, form_id, sender, to, pre, post, callback, sb, sa, ttl, len, t)
    # make request
    result = session.get(url, headers=headers)
    # check result
    if result.status_code == 200:
        # request is success. inspect the json object for the value of `acknowledge`
        json = result.json()
        if json['acknowledge'] == 'success':
            # do success
            print ("api success")
        else:
            # do failure
            print ("api error") 
    else:
        # anything other than 200 goes here.
        print ("http error ... code: %d , msg: %s " % (result.status_code, result.content))    
    
    return (result.status_code, result.content)

def verify_otp_sms(phone_number: str, code: str):
    # we use reqests library for the samples
    import requests
    # session configuration
    session = requests.Session()
    # base url
    base_url = 'https://api.afromessage.com/api/verify'
    # api token
    token = setting.SMS_TOKEN
    # header
    headers = {'Authorization': 'Bearer ' + token}
    # request parameters
    # Note: You can also use the verification id sent in the challenge request. 
    # Use the `vc` query parameter to verify via verification id.
    to = phone_number
    code = code
    # final url
    url = '%s?to=%s&code=%s' % (base_url, to, code)
    # make request
    result = session.get(url, headers=headers)
    # check result
    if result.status_code == 200:
        # request is success. inspect the json object for the value of `acknowledge`
        json = result.json()
        if json['acknowledge'] == 'success':
            # do success
            print ('api success')
        else:
            # do failure
            print ('api error')
    else:
        # anything other than 200 goes here.
        print ('http error ... code: %d , msg: %s ' % (result.status_code, result.content))
    
    return (result.status_code, result.content)
                                