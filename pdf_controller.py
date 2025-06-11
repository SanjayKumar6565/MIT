#PDF Download Endpoint
from flask import Blueprint, send_file, jsonify
from app.services import PDFService, ApplicationService
from app.exceptions import ApplicationException
from app.utils.logger import log
from datetime import datetime

pdf_bp = Blueprint('pdf', __name__, url_prefix='/api/pdf')
pdf_service = PDFService()
application_service = ApplicationService()

@pdf_bp.route('/offer-letter/<int:app_id>', methods=['GET'])
def generate_offer_letter(app_id):
    try:
        application = application_service.get_application_by_id(app_id)
        
        if application.status != 'Approved':
            return jsonify({'error': 'Application not approved'}), 400
        
        application_data = {
            'applicant_name': application.applicant_name,
            'email': application.email,
            'phone': application.phone,
            'university': application.university,
            'domain': application.domain.name,
            'start_date': application.start_date.strftime('%B %d, %Y'),
            'end_date': application.end_date.strftime('%B %d, %Y'),
            'duration_weeks': application.duration_weeks,
            'issue_date': datetime.now().strftime('%B %d, %Y')
        }
        
        pdf_buffer = pdf_service.generate_offer_letter(application_data)
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f"MIT_Offer_Letter_{application.applicant_name.replace(' ', '_')}.pdf",
            mimetype='application/pdf'
        )
    except ApplicationException as e:
        return jsonify({'error': str(e)}), e.status_code
    except Exception as e:
        log.error(f'Error generating offer letter: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500