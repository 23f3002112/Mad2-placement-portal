from flask import Blueprint, request, jsonify, send_file
from models import db, Notification
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
import os

notification_bp = Blueprint('notification', __name__)

@notification_bp.route('/', methods=['GET'])
@jwt_required()
def get_notifications():
    current_user = json.loads(get_jwt_identity())
    notifications = Notification.query.filter_by(user_id=current_user['id']).order_by(Notification.created_at.desc()).all()
    
    result = []
    for n in notifications:
        result.append({
            "id": n.id,
            "title": n.title,
            "message": n.message,
            "is_read": n.is_read,
            "created_at": n.created_at
        })
    return jsonify(result), 200

@notification_bp.route('/<int:notif_id>/read', methods=['PUT'])
@jwt_required()
def mark_read(notif_id):
    current_user = json.loads(get_jwt_identity())
    notification = Notification.query.filter_by(id=notif_id, user_id=current_user['id']).first_or_404()
    
    notification.is_read = True
    db.session.commit()
    return jsonify({"msg": "Notification marked as read"}), 200

# Endpoint to serve generated PDFs safely (used in tasks.py)
@notification_bp.route('/downloads/<filename>', methods=['GET'])
def download_file(filename):
    # Ensure it only accesses the exports directory
    safe_path = os.path.join(os.getcwd(), 'exports', filename)
    if os.path.exists(safe_path):
        return send_file(safe_path)
    return jsonify({"msg": "File not found"}), 404
