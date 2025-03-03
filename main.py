from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import tools

app = Flask(__name__)

@app.route("/message", methods=["POST"])
def message():
    """Handle incoming WhatsApp messages"""
    incoming_msg = request.form.get("Body").strip()

    if incoming_msg == "1":
        return template()
    
    tools.insert_data(incoming_msg)

    resp = MessagingResponse()
    resp.message(f"Received: {incoming_msg}. Reply with '1' to get a template message.")
    return str(resp)


@app.route("/template", methods=["POST"])
def template():
    """Send a template message when user sends '1'"""
    resp = MessagingResponse()
    resp.message("Nama: <nama_lengkap>\nKSM: <jumlah_ksm>\nKUR: <jumlah_kur>\nCC: <jumlah_cc>")
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
