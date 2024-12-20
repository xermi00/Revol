from flask import Flask, request

app = Flask(__name__)

@app.route('/update', methods=['POST'])
def update_file():
    username = request.form.get('username')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    if not all([username, latitude, longitude]):
        return "Invalid data", 400

    with open("user_data.txt", "a") as file:
        file.write(f"Username: {username}, Latitude: {latitude}, Longitude: {longitude}\n")

    return "Data received and logged", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
