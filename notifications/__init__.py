from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/alert', methods=['POST'])
def alert():
    data = request.json
    alert_message = data['message']
    
    # Replace this with production-ready notification mechanism
    print(alert_message)
    return jsonify({"message": "Notification sent"}), 200

if __name__ == '__main__':
    app.run(debug=True)