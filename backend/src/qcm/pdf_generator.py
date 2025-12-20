from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO

class PDFGenerator:
    @staticmethod
    def create_pdf(qcm_object):
        buffer = BytesIO()
        
        # 1. Setup the Document with margins (72 points = 1 inch)
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )
        
        story = [] # This list holds all the elements (paragraphs, spaces)
        styles = getSampleStyleSheet()
        
        # 2. Define Custom Styles
        
        # Title Style
        title_style = styles["Heading1"]
        title_style.alignment = 1 # Center alignment
        
        # Question Style (Bold & Bigger)
        question_style = ParagraphStyle(
            'QuestionStyle',
            parent=styles['Normal'],
            fontSize=12,
            leading=16,        # Space between lines of text
            spaceAfter=10,     # Space after the paragraph
            fontName='Helvetica-Bold' # <--- MAKES IT BOLD
        )

        # Choice Style (Indented)
        choice_style = ParagraphStyle(
            'ChoiceStyle',
            parent=styles['Normal'],
            fontSize=11,
            leading=14,
            leftIndent=20,     # <--- Indents the options
            spaceAfter=4
        )

        # 3. Build the Content
        
        # Add Title
        story.append(Paragraph(qcm_object.title, title_style))
        story.append(Spacer(1, 24)) # Add vertical space
        
        # Add Questions
        for i, q in enumerate(qcm_object.questions, 1):
            # --- Question Text ---
            # Paragraph automatically wraps text if it hits the right margin
            q_text = f"{i}. {q.text}"
            story.append(Paragraph(q_text, question_style))
            
            # --- Choices (A, B, C...) ---
            for idx, choice in enumerate(q.choices):
                # Convert index 0 -> A, 1 -> B, etc.
                letter_label = chr(65 + idx) 
                
                # Optional: Mark correct answer for Professor's version
                # prefix = "*" if choice.get('is_correct') else ""
                
                c_text = f"<b>{letter_label}.</b> {choice['text']}"
                story.append(Paragraph(c_text, choice_style))
            
            # Space between questions
            story.append(Spacer(1, 15))

        # 4. Generate PDF
        doc.build(story)
        buffer.seek(0)
        return buffer