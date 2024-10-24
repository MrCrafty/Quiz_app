
from flask import Blueprint,  jsonify, request, json
from flask_jwt_extended import jwt_required, get_jwt
from . import db
from .models import Services, User, ServiceRequest

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
