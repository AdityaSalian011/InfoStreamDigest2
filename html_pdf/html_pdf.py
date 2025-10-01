import os
from weasyprint import HTML

class HTMLPdf:
    def html_to_pdf(self, html_file, pdf_file):
        """A method that converts html file -> pdf file."""
        if not os.path.exists(html_file):
            return None, f'HTML file: {html_file} Not found.'
        try:
            HTML(html_file).write_pdf(pdf_file)
            return f'Sucessfully created PDF: {pdf_file}', None
            
        except Exception as exc:
            return None, f'Got unexpected error while creating pdf.\n{exc}'