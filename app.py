from flask import Flask, jsonify, request, make_response
import requests
import os
from flasgger import swag_from
from dotenv import load_dotenv
from swagger.config import init_swagger


app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# MICROSERVICES:
MICROSERVICES = {
    "user": os.getenv("USER_MICROSERVICE_URL", "http://localhost:5005"),
    "car": os.getenv("CAR_MICROSERVICE_URL", "http://localhost:5006"),
    "damage": os.getenv("SKADE_MICROSERVICE_URL", "http://localhost:5007"),
}

# Initialize Swagger
init_swagger(app)


# ----------------------------------------------------- GET /cars
@app.route('/cars', methods=['GET'])
#@swag_from('swagger/get_subscriptions.yaml') #TODO
def get_cars():
    response = requests.get(
        url=f"{MICROSERVICES['car']}/cars", 
        cookies=request.cookies
        )
    try: 
        data = response.json() 
    except requests.exceptions.JSONDecodeError: 
        data = []

    if response.status_code in [200, 201, 204]:
        return jsonify(data), response.status_code
    else:
        return jsonify({
            "error": "Failed to fetch from microservice",
            "data_returned_from_microservice": data
        }), response.status_code

# ----------------------------------------------------- GET /cars/<id>
@app.route('/cars/<int:id>', methods=['GET'])
#@swag_from('swagger/get_current_subscriptions_total_price.yaml') #TODO
def get_car_by_id(id):
    response = requests.get(f"{MICROSERVICES['car']}/cars/{id}",cookies=request.cookies)
    try: 
        data = response.json() 
    except requests.exceptions.JSONDecodeError: 
        data = []

    if response.status_code in [200, 201, 204]:
        return jsonify(data), response.status_code
    else:
        return jsonify({
            "error": "Failed to fetch from microservice",
            "data_returned_from_microservice": data
        }), response.status_code
    

# ----------------------------------------------------- PATCH /cars/<id>
@app.route('/cars/<int:id>', methods=['PATCH'])
#@swag_from('swagger/get_current_subscriptions_total_price.yaml') #TODO
def patch_car_by_id(id):
    response = requests.patch(f"{MICROSERVICES['car']}/cars/{id}",json=request.json ,cookies=request.cookies)
    try: 
        data = response.json() 
    except requests.exceptions.JSONDecodeError: 
        data = []

    if response.status_code in [200, 201, 204]:
        return jsonify(data), response.status_code
    else:
        return jsonify({
            "error": "Failed to fetch from microservice",
            "data_returned_from_microservice": data
        }), response.status_code
    



# ----------------------------------------------------- GET /damage
@app.route('/damage-types', methods=['GET'])
@swag_from('swagger/get_damage_types.yaml')
def get_damage_types_route():
    response = requests.get(f"{MICROSERVICES['c']}/cars/{id}",cookies=request.cookies)
    try: 
        data = response.json() 
    except requests.exceptions.JSONDecodeError: 
        data = []

    if response.status_code in [200, 201, 204]:
        return jsonify(data), response.status_code
    else:
        return jsonify({
            "error": "Failed to fetch from microservice",
            "data_returned_from_microservice": data
        }), response.status_code


# ----------------------------------------------------- POST /damage-report
@app.route('/damage-types', methods=['POST'])
@swag_from('swagger/add_damage_type.yaml')
def add_to_types():
    data = request.json

    if not data:
        return jsonify({"message": "No data provided"}), 400

    try:
        damage_type_item = _data_to_damage_type_dict(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    result = add_new_types(damage_type_item)
    return jsonify(result[1]), result[0]




# ----------------------------------------------------- POST /login
@app.route('/login', methods=['POST'])
@swag_from('swagger/login.yaml')
def login():
    response = requests.post(
        url=f"{MICROSERVICES['user']}/login",
        cookies=request.cookies,
        json=request.json,
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code == 200:
        response_data = response.json()
        
        # Create the Flask response
        flask_response = jsonify(response_data)
        
        # Extract cookies from the microservice response
        if 'Authorization' in response.cookies:
            auth_cookie = response.cookies['Authorization']
            flask_response.set_cookie('Authorization', auth_cookie, httponly=True, secure=True)
        
        return flask_response, 200
    else:
        data = response.json()
        return jsonify({
            "error": "Failed to fetch from microservice",
            "data_returned_from_microservice": data
        }), response.status_code

# ----------------------------------------------------- GET /health
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

# ----------------------------------------------------- Catch-all route for unmatched endpoints 
@app.errorhandler(404)
def page_not_found_404(e):
    return jsonify({"message": "Endpoint does not exist"})

@app.errorhandler(405)
def page_not_found_405(e):
    return jsonify({"message": "Method not allowed - double check the method you are using"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5002)))
