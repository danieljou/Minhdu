from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate

class CustomDocTemplate(SimpleDocTemplate):
    def __init__(
        self,
        filename,
        right_margin=7,
        left_margin=7,
        top_margin=7,
        bottom_margin=7,
        pagesize=landscape(A4),
        **kw,
    ):
        super().__init__(filename, **kw)
        self.rightMargin = right_margin
        self.leftMargin = left_margin
        self.topMargin = top_margin
        self.bottomMargin = bottom_margin
        self.pagesize = pagesize


class A4Printer:
    def get_pdf(self, buffer):
        self.buffer = buffer
        styles = getSampleStyleSheet()
        doc = CustomDocTemplate(buffer)
        elements = []
        elements.append(Paragraph("Title of the PDF", style=styles["Heading2"]))
        elements.append(Paragraph("Heading", style=styles["Heading4"]))
        elements.append(Paragraph("Text inside the pdf", style=styles["BodyText"]))
        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf