
from flask import Blueprint,  jsonify, request, json
from flask_jwt_extended import jwt_required, get_jwt
from . import db
from .models import Category, Services, User, ServiceRequest

api = Blueprint('api', __name__)


@api.route('/status', methods=["GET"])
def status():
    return jsonify("Website api is running"), 200


@api.route("/getServices", methods=["GET"])
# @jwt_required()
def getServices():
    serviceList = []
    services = Services.query.all()
    if (len(services) == 0):
        return jsonify({"error": "No services available"}), 204
    for service in services:
        serviceList.append({
            "id": service.id,
            "name": service.name,
            "description": service.description,
            "price": service.price,
            "time_required": service.time_required
        })
    return jsonify({"data": serviceList}), 200


@api.route("getService", methods=["POST"])
@jwt_required()
def getService():
    data = request.get_json()
    service_id = data.get('service_id')
    print(data)
    service = Services.query.filter_by(id=service_id).first()
    if (service == None):
        return jsonify({"error": "Service not found"}), 404
    return jsonify({"data": {
        "service_name": service.name,
        "service_description": service.description,
        "price": service.price,
        "time_required": service.time_required
    }}), 200


@api.route("/addService", methods=["POST"])
@jwt_required()
def addService():
    print(get_jwt())
    data = request.get_json()
    print(data)
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    time_required = data.get('time_required')
    new_service = Services(name=name, description=description,
                           price=price, time_required=time_required)
    db.session.add(new_service)
    db.session.commit()
    return jsonify({"message": "Service added successfully"}), 200


@api.route("/deleteService", methods=["POST"])
@jwt_required()
def deleteService():
    data = request.get_json()
    service_id = data.get('service_id')
    service = Services.query.filter_by(id=service_id).first()
    if (service == None):
        return jsonify({"error": "Service not found"}), 404
    db.session.delete(service)
    db.session.commit()
    return jsonify({"message": "Service deleted successfully"}), 200


@api.route("/editService", methods=["POST"])
@jwt_required()
def editService():
    data = request.get_json()
    service_id = data.get('service_id')
    service = Services.query.filter_by(id=service_id).first()
    if (service == None):
        return jsonify({"error": "Service not found"}), 404
    else:
        service.name = data.get('service_name')
        service.description = data.get('service_description')
        service.price = data.get('base_price')
        service.time_required = data.get('time_required')
        db.session.commit()
        return jsonify({"message": "Service edited successfully"}), 200


@ api.route("/getProfessionals", methods=["GET"])
@ jwt_required()
def getProfessionals():
    profList = []
    prof = User.query.filter_by(role="professional").all()
    for pro in prof:
        profList.append({
            "id": pro.id,
            "email": pro.email,
            "role": pro.role,
            "xp": pro.xp
        })
    if (len(prof) == 0):
        return jsonify({"error": "No professionals available"}), 204
    return jsonify({"data": profList}), 200


@ api.route("/getServiceRequests", methods=["GET"])
@ jwt_required()
def getServicesRequests():
    ser_req = ServiceRequest.query.all()
    ser_req_list = []
    for ser in ser_req:
        ser_req_list.append({
            "id": ser.id,
            "customer_id": ser.customer_id,
            "professional_id": ser.professional_id,
            "service_id": ser.service_id,
            "status": ser.status,
            "date_of_request": ser.date_of_request,
            "date_of_completion": ser.date_of_completion,
            "remarks": ser.remarks
        })
    if (len(ser_req) == 0):
        return jsonify({"error": "No services available"}), 204
    return jsonify({"data": ser_req_list}), 200


@ api.route("/createServiceRequest", methods=["POST"])
@ jwt_required()
def createServiceRequest():
    data = request.get_json()


@api.route("/getCategories", methods=["GET"])
@jwt_required()
def getCategories():
    categoryList = []
    categories = Category.query.all()
    if (len(categories) == 0):
        return jsonify({"error": "No categories available"}), 204
    for category in categories:
        categoryList.append({
            "id": category.id,
            "name": category.name,
            "description": category.description
        })
    return jsonify({"data": categoryList}), 200


@api.route("/getCategory", methods=["POST"])
@jwt_required()
def getCategory():
    data = request.get_json()
    category_id = data.get('category_id')
    category = Category.query.filter_by(id=category_id).first()
    if (category == None):
        return jsonify({"error": "Category not found"}), 404
    return jsonify({"data": {
        "name": category.name,
        "description": category.description
    }}), 200


@api.route("/createCategory", methods=["POST"])
@jwt_required()
def addCategory():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    new_category = Category(name=name, description=description)
    db.session.add(new_category)
    db.session.commit()
    return jsonify({"message": "Category added successfully"}), 200


@api.route("/deleteCategory", methods=["POST"])
@jwt_required()
def deleteCategory():
    data = request.get_json()
    category_id = data.get('category_id')
    category = Category.query.filter_by(id=category_id).first()
    if (category == None):
        return jsonify({"error": "Category not found"}), 404
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted successfully"}), 200


@api.route("editCategory", methods=["POST"])
@jwt_required()
def editCategory():
    data = request.get_json()
    category_id = data.get('category_id')
    category = Category.query.filter_by(id=category_id).first()
    if (category == None):
        return jsonify({"error": "Category not found"}), 404
    else:
        category.name = data.get('name')
        category.description = data.get('description')
        db.session.commit()
        return jsonify({"message": "Category edited successfully"}), 200
