

import requests                            

def send_otp_sms(phone_number: str):
    # Send OTP SMS
        # we use requests library for the samples
    # session object
    session = requests.Session()
    # base url
    base_url = 'https://api.afromessage.com/api/challenge'
    # api token
    token = 'YOUR_TOKEN'
    # header
    headers = {'Authorization': 'Bearer ' + token}
    # request parameters
    callback = 'YOUR_CALLBACK'
    form_id = 'YOUR_IDENTIFIER_ID'
    sender = 'Enemamar'
    to = 'YOUR_RECIPIENT'
    pre = " Hello, your OTP is: " 
    post = " Thank you for using our service."
    sb = 0
    sa = 0
    ttl = 100
    len = 4
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
    pass

def verify_otp_sms(phone_number: str, otp: str):
    # Verify OTP SMS
    pass