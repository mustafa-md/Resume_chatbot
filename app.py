from flask import Flask, request, make_response
import json
import os
from flask_cors import cross_origin
from SendEmail.sendEmail import EmailSender
from logger import logger

app = Flask(__name__)


# geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():
    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# processing the request from dialogflow
def processRequest(req):
    log = logger.Log()

    sessionID = req.get('responseId')

    result = req.get("queryResult")
    user_says = result.get("queryText")
    log.write_log(sessionID, "User Says: " + user_says)
    parameters = result.get("parameters")
    email = parameters.get("email")

    email_sender = EmailSender()
    email_sender.send_email_to_student(email)
    return {
        "fulfillmentText": result.get("fulfillmentText"),
        "fulfillmentMessages": result.get("fulfillmentMessages")
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
