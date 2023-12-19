from twilio.rest import Client


#client = Client(account_sid, auth_token)

def sendMessage(phone_number,message):
    client = Client('AC33ab0f263ce5c846b0fe11baf0822f8d', 'cd1317207b4daf03c8ee6fac54b8c262')
    client.messages.create(
    body=message,
    from_='+18556195096',
    to=phone_number
    )

