# Requirement: pip install reportlab
from reportlab.pdfgen import canvas
from io import BytesIO

class PDFGenerator:
    @staticmethod
    def create_pdf(qcm_object):
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        
        p.drawString(100, 800, f"Exam: {qcm_object.title}")
        
        y = 750
        for i, q in enumerate(qcm_object.questions, 1):
            p.drawString(40, y, f"{i}. {q.text}")
            y -= 20
            for choice in q.choices:
                p.drawString(60, y, f"- {choice['text']}")
                y -= 15
            y -= 10 # Extra space between questions
            
            if y < 50: # New page if at bottom
                p.showPage()
                y = 800

        p.save()
        buffer.seek(0)
        return buffer