from twilio.rest import Client


#client = Client(account_sid, auth_token)

def sendMessage(phone_number,message):
    client = Client('AC33ab0f263ce5c846b0fe11baf0822f8d', '7f389a4f3a9e9d7bf92271378fc061e1')
    client.messages.create(
    body=message,
    from_='+18556195096',
    to=phone_number
    )

