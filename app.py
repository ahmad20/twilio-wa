from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/message", methods=["POST"])
def message():
    """Handle incoming WhatsApp messages"""
    incoming_msg = request.form.get("Body").strip()

    if incoming_msg == "1":
        return template()

    resp = MessagingResponse()
    resp.message(f"Received: {incoming_msg}. Reply with '1' to get a template message.")
    return str(resp)


@app.route("/template", methods=["POST"])
def template():
    """Send a template message when user sends '1'"""
    resp = MessagingResponse()
    resp.message("Hello! This is your template message. How can I help you?")
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
