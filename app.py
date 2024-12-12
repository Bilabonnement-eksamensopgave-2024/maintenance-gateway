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

# ----------------------------------------------------- GET /
# Root endpoint with gateway documentation
@app.route('/', methods=['GET'])
def service_info():
    return jsonify({
        "service": "Car and Damage Management Gateway",
        "description": "This gateway routes requests to microservices handling cars, damage reports, and related financial operations.",
        "endpoints": [
            {
                "path": "/cars",
                "method": "GET",
                "description": "Fetches a list of cars",
                "response": "JSON array of car objects",
                "role_required": "user or admin"
            },
            {
                "path": "/cars/<id>",
                "method": "GET",
                "description": "Fetches details of a specific car by ID",
                "response": "JSON object with car details",
                "role_required": "user or admin"
            },
            {
                "path": "/cars/<id>",
                "method": "PATCH",
                "description": "Updates details of a specific car by ID",
                "response": "JSON object with updated car details",
                "role_required": "admin"
            },
            {
                "path": "/damage-types",
                "method": "GET",
                "description": "Fetches a list of all damage types",
                "response": "JSON array of damage type objects",
                "role_required": "admin"
            },
            {
                "path": "/damage-types",
                "method": "POST",
                "description": "Adds a new damage type",
                "response": "JSON object with new damage type",
                "role_required": "admin"
            },
            {
                "path": "/damage-types/<id>",
                "method": "PATCH",
                "description": "Updates details of a specific damage type by ID",
                "response": "JSON object with updated damage type",
                "role_required": "admin"
            },
            {
                "path": "/damage-reports",
                "method": "GET",
                "description": "Fetches a list of all damage reports",
                "response": "JSON array of damage report objects",
                "role_required": "admin or finance"
            },
            {
                "path": "/damage-reports",
                "method": "POST",
                "description": "Adds a new damage report",
                "response": "JSON object with new damage report",
                "role_required": "admin"
            },
            {
                "path": "/damage-reports/cars/<id>",
                "method": "GET",
                "description": "Fetches damage reports for a specific car by ID",
                "response": "JSON array of damage reports",
                "role_required": "admin or finance"
            },
            {
                "path": "/damage-reports/subscriptions/<id>/total-cost",
                "method": "GET",
                "description": "Fetches the total cost of damage reports for a specific subscription ID",
                "response": "JSON object with total cost",
                "role_required": "finance"
            },
            {
                "path": "/login",
                "method": "POST",
                "description": "Authenticates a user and sets authorization cookies",
                "response": "JSON object with token or error message",
                "role_required": "none"
            },
            {
                "path": "/health",
                "method": "GET",
                "description": "Returns the health status of the service",
                "response": "JSON object with health status",
                "role_required": "none"
            }
        ]
    })


# ----------------------------------------------------- GET /cars
@app.route('/cars', methods=['GET'])
@swag_from('swagger/get_cars.yaml')
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
@swag_from('swagger/get_cars_by_id.yaml')
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
@swag_from('swagger/patch_car.yaml')
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
    



# ----------------------------------------------------- GET /damage-types
@app.route('/damage-types', methods=['GET'])
@swag_from('swagger/get_damage_types.yaml')
def get_damage_types_route():
    response = requests.get(f"{MICROSERVICES['damage']}/damage-types",cookies=request.cookies)
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


# ----------------------------------------------------- GET /damage-types/<id>
@app.route('/damage-types/<int:id>', methods=['GET'])
@swag_from('swagger/get_damage_type_by_id.yaml')
def get_damage_types_by_id_route(id):
    response = requests.get(f"{MICROSERVICES['damage']}/damage-types/{id}",cookies=request.cookies)
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
def post_damage_reports_route():
    response = requests.post(f"{MICROSERVICES['damage']}/damage-types",json=request.json,cookies=request.cookies)
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


# ----------------------------------------------------- GET /damage-reports

@app.route('/damage-reports', methods=['GET'])
@swag_from('swagger/get_all_damage_reports.yaml')
def get_damage_reports_route():
    response = requests.get(f"{MICROSERVICES['damage']}/damage-reports",cookies=request.cookies)
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

# ----------------------------------------------------- GET /damage-reports/<id>

@app.route('/damage-reports/<int:id>', methods=['GET'])
@swag_from('swagger/get_the_selected_damage_report.yaml')
def get_damage_reports_by_id_route(id):
    response = requests.get(f"{MICROSERVICES['damage']}/damage-reports/{id}",cookies=request.cookies)
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
    


# ----------------------------------------------------- GET /damage-reports/cars/<id>
@app.route('/damage-reports/cars/<int:id>', methods=['GET'])
@swag_from('swagger/get_the_selected_damage_report_carid.yaml')
def get_damage_reports_by_car_id_route(id):
    response = requests.get(f"{MICROSERVICES['damage']}/damage-reports/cars/{id}",cookies=request.cookies)
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
    


# ----------------------------------------------------- GET /damage-reports/subscriptions/<id>
@app.route('/damage-reports/subscriptions/<int:id>', methods=['GET'])
@swag_from('swagger/get_the_selected_damage_report_subscriptionid.yaml')
def get_damage_reports_by_subscriptions_id_route(id):
    response = requests.get(f"{MICROSERVICES['damage']}/damage-reports/subscriptions/{id}",cookies=request.cookies)
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

# ----------------------------------------------------- GET /damage-reports/subscriptions/<id>/total-cost
@app.route('/damage-reports/subscriptions/<int:id>/total-cost', methods=['GET'])
@swag_from('swagger/get_total_cost_by_subscriptionid.yaml')
def get_damage_reports_by_subscriptions_id_total_route(id):
    response = requests.get(f"{MICROSERVICES['damage']}/damage-reports/subscriptions/{id}/total-cost",cookies=request.cookies)
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


# ----------------------------------------------------- PATCH /damage-reports/<id>
@app.route('/damage-reports/<int:id>', methods=['PATCH'])
@swag_from('swagger/update_damage_report_by_id.yaml')
def patch_damage_report_by_id(id):
    response = requests.patch(f"{MICROSERVICES['damage']}/damage-reports/{id}",json=request.json ,cookies=request.cookies)
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
    
# ----------------------------------------------------- DELETE /damage-reports/<id>
@app.route('/damage-reports/<int:id>', methods=['DELETE'])
@swag_from('swagger/delete_damage_report.yaml')
def delete_damage_report_by_id(id):
    response = requests.delete(f"{MICROSERVICES['damage']}/damage-reports/{id}",json=request.json ,cookies=request.cookies)
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
    
# ----------------------------------------------------- POST /damage-reports
@app.route('/damage-reports', methods=['POST'])
@swag_from('swagger/add_damage_report.yaml')
def post_damage_report():
    response = requests.post(f"{MICROSERVICES['damage']}/damage-reports",json=request.json ,cookies=request.cookies)
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


# ----------------------------------------------------- PATCH /damage-types/<id>
@app.route('/damage-types/<int:id>', methods=['PATCH'])
@swag_from('swagger/update_damage_type.yaml')
def patch_damage_types_by_id(id):
    response = requests.patch(f"{MICROSERVICES['damage']}/damage-types/{id}",json=request.json ,cookies=request.cookies)
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


# ----------------------------------------------------- DELETE /damage-types/<id>
@app.route('/damage-types/<int:id>', methods=['DELETE'])
@swag_from('swagger/delete_damage_type.yaml')
def delete_damage_type_by_id(id):
    response = requests.delete(f"{MICROSERVICES['damage']}/damage-types/{id}",json=request.json ,cookies=request.cookies)
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
    
# ----------------------------------------------------- POST /damage-types
@app.route('/damage-types', methods=['POST'])
@swag_from('swagger/add_damage_type.yaml')
def post_damage_type():
    response = requests.post(f"{MICROSERVICES['damage']}/damage-types",json=request.json ,cookies=request.cookies)
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
