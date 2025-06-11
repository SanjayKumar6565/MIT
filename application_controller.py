#REST API (Task 1)
from flask import Blueprint, request, jsonify
from app.services import ApplicationService
from app.exceptions import ValidationException, ApplicationException
from app.utils.logger import log

application_bp = Blueprint('application', __name__, url_prefix='/api/applications')
application_service = ApplicationService()

@application_bp.route('/', methods=['POST'])
def create_application():
    try:
        data = request.get_json()
        application = application_service.create_application(data)
        return jsonify({
            'message': 'Application submitted successfully',
            'application_id': application.id
        }), 201
    except ValidationException as e:
        log.error(f'Validation error: {str(e)}')
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        log.error(f'Error creating application: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@application_bp.route('/<int:app_id>', methods=['GET'])
def get_application(app_id):
    try:
        application = application_service.get_application_by_id(app_id)
        return jsonify(application.to_dict()), 200
    except ApplicationException as e:
        return jsonify({'error': str(e)}), e.status_code
    except Exception as e:
        log.error(f'Error fetching application: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@application_bp.route('/<int:app_id>/status', methods=['PUT'])
def update_status(app_id):
    try:
        data = request.get_json()
        status = data.get('status')
        if not status:
            raise ValidationException('Status is required')
        
        application = application_service.update_application_status(app_id, status)
        return jsonify({
            'message': 'Status updated successfully',
            'status': application.status
        }), 200
    except (ValidationException, ApplicationException) as e:
        return jsonify({'error': str(e)}), e.status_code
    except Exception as e:
        log.error(f'Error updating status: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500