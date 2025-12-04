from weasyprint import HTML
import os
from datetime import datetime

class PDFGenerator:

    @staticmethod
    def html_to_pdf(html_content, save_path=None):
        """Genera un PDF desde HTML y lo guarda en una ruta."""
        
        # Si no se pasa ruta → generar una automáticamente
        if not save_path:
            folder = "static/certificates"
            os.makedirs(folder, exist_ok=True)
            filename = f"cert_{datetime.now().strftime('%Y%m%d')}.pdf"
            save_path = os.path.join(folder, filename)

        # Convertir HTML → PDF
        HTML(string=html_content).write_pdf(save_path)

        return save_path
