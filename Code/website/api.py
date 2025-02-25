
from flask import Blueprint,  jsonify, request, json
from flask_jwt_extended import jwt_required, get_jwt
from . import db
from .models import Services, User, ServiceRequest

api = Blueprint('api', __name__)


@api.route("/getServices", methods=["GET"])
@jwt_required()
def getServices():
    serviceList = []
    services = Services.query.all()
    if (len(services) == 0):
        return jsonify({"error": "No services available"}), 204
    for service in services:
        service_request = []
        for req in service.service_requests:
            service_request.append({
                "id": req.id,
                "customer_id": req.customer_id,
                "professional_id": req.professional_id,
                "status": req.status,
                "date_of_request": req.date_of_request,
                "date_of_completion": req.date_of_completion,
                "remarks": req.remarks
            })
        serviceList.append({
            "id": service.id,
            "name": service.name,
            "description": service.description,
            "price": service.price,
            "time_required": service.time_required
        })
    return jsonify({"data": serviceList}), 200
