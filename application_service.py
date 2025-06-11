#Business Logic (Task 2)

from app.models import Application, Domain
from app.repositories import ApplicationRepository
from app.exceptions import ValidationException, ApplicationException
from datetime import datetime, timedelta
from app.utils.validation import validate_email, validate_phone

class ApplicationService:
    def __init__(self):
        self.repository = ApplicationRepository()
    
    def create_application(self, data):
        # Validate inputs
        if not validate_email(data.get('email')):
            raise ValidationException('Invalid email format')
        
        if not validate_phone(data.get('phone')):
            raise ValidationException('Invalid phone number')
        
        # Calculate duration
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        
        if start_date >= end_date:
            raise ValidationException('End date must be after start date')
        
        duration_weeks = (end_date - start_date).days // 7
        
        if duration_weeks < 4 or duration_weeks > 24:
            raise ValidationException('Internship duration must be between 4 and 24 weeks')
        
        # Check domain exists
        domain = Domain.query.get(data['domain_id'])
        if not domain:
            raise ValidationException('Invalid domain selected')
        
        # Create application
        application = Application(
            applicant_name=data['applicant_name'],
            email=data['email'],
            phone=data['phone'],
            university=data['university'],
            major=data['major'],
            graduation_year=data['graduation_year'],
            domain_id=data['domain_id'],
            start_date=start_date,
            end_date=end_date,
            duration_weeks=duration_weeks
        )
        
        return self.repository.save(application)
    
    def get_application_by_id(self, app_id):
        application = self.repository.find_by_id(app_id)
        if not application:
            raise ApplicationException('Application not found', 404)
        return application
    
    def update_application_status(self, app_id, status):
        valid_statuses = ['Pending', 'Approved', 'Rejected', 'Completed']
        if status not in valid_statuses:
            raise ValidationException(f'Invalid status. Must be one of: {", ".join(valid_statuses)}')
        
        application = self.get_application_by_id(app_id)
        application.status = status
        return self.repository.save(application)