#PDF Generation (Task 4)
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from app.utils.logger import log

class PDFService:
    def generate_offer_letter(self, application_data):
        try:
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title = Paragraph("MIT Internship Program - Offer Letter", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 12))
            
            # Date
            date_text = f"Date: {application_data['issue_date']}"
            story.append(Paragraph(date_text, styles['Normal']))
            story.append(Spacer(1, 24))
            
            # Recipient
            recipient = f"""
            <b>{application_data['applicant_name']}</b><br/>
            {application_data['university']}<br/>
            {application_data['email']}<br/>
            {application_data['phone']}
            """
            story.append(Paragraph(recipient, styles['Normal']))
            story.append(Spacer(1, 24))
            
            # Body
            body = f"""
            <b>Subject: Internship Offer Letter</b><br/><br/>
            
            Dear {application_data['applicant_name']},<br/><br/>
            
            We are pleased to offer you an internship position in our <b>{application_data['domain']}</b> 
            program at MIT. Your internship is scheduled to begin on <b>{application_data['start_date']}</b> 
            and end on <b>{application_data['end_date']}</b>, for a duration of <b>{application_data['duration_weeks']} weeks</b>.<br/><br/>
            
            During this internship, you will be working on exciting projects under the guidance of our 
            experienced mentors. We believe this opportunity will provide you with valuable experience 
            and skills in your field of study.<br/><br/>
            
            Please confirm your acceptance of this offer by replying to this email.<br/><br/>
            
            Sincerely,<br/><br/>
            
            <b>MIT Internship Program</b><br/>
            Massachusetts Institute of Technology
            """
            story.append(Paragraph(body, styles['Normal']))
            
            doc.build(story)
            buffer.seek(0)
            return buffer
        except Exception as e:
            log.error(f"Error generating PDF: {str(e)}")
            raise