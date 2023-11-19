from twilio.rest import Client



def sendMessage(phone_number,message):
    client = Client('', '')
    client.messages.create(
    body=message,
    from_='+',
    to=phone_number
    )

