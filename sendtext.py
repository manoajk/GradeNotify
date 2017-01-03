from twilio.rest import TwilioRestClient
from userinfo import myNum, twilioNum, ACCOUNT_SID, AUTH_TOKEN
from getgrades import text

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

try:
	client.messages.create(
	    to = myNum,
	    from_ = twilioNum,
	    body = text,
	)
except TwilioRestException as e:
	print(e)
