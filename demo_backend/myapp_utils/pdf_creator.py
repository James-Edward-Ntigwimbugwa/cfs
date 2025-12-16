import base64
import io
import os

from django.conf import settings
from django.template.loader import get_template
from dotenv import dotenv_values
from weasyprint import CSS, HTML
from weasyprint.text.fonts import FontConfiguration

from myapp_dto.enums import FileVisibiltyChoices
from myapp_files.models import FileKeys

from .file_utils import UploadFile

config = dotenv_values('.env')


class PDF:
    @classmethod
    def pdf_generator(cls, data_context, html_template, configuration=None, saved_file='temp.pdf', image_dir = None):
        """
            This method is for PDF generation only.\n
            Data to be passed for this method.
                    `data_context`:str
                    `saved_file`:str
                    `html_template`: str `path/to/html/file.html`
                    `configuration`:dict
            The output of this method/function if file path to which a pdf file is generated,`saved_file`
        """
        template = get_template(html_template)
        html = template.render({"data": data_context, "configuration": configuration, "IMAGE_URL": image_dir if image_dir is not None else config['IMAGE_URL']})

        font_config = FontConfiguration()
        css = CSS(string=''' @page { 'size': 'A4', 'margin-top': '0.20in', 'margin-right': '0.20in', 'margin-bottom': '0.20in', 'margin-left': '0.20in', 'encoding': "UTF-8", 'enable-local-file-access': None } body { font-family: "Times New Roman", Times, serif; !important;font-size: 13px; } ''', font_config=font_config)

        file_path = 'myapp_media/' + str(saved_file)

        html = HTML(string=html)
        html.write_pdf(file_path, stylesheets=[css], font_config=font_config)

        read_path = os.path.join(settings.BASE_DIR, file_path)

        file_text = open(read_path, 'rb')
        file_read = file_text.read()
        file_encode = base64.b64encode(file_read)
        base64_contents = file_encode.decode("utf-8")

        success, key, file_id, relative_file_path = UploadFile.base64_handler(base64_contents, '.pdf', 'documents', FileVisibiltyChoices.PUBLIC.value)
        if success:
            FileKeys.objects.create(key_name=key, key_file_id=file_id)

        return relative_file_path

    @classmethod
    def base64_pdf_generator(cls, data_context, html_template):
        template = get_template(html_template)
        html = template.render({"data": data_context, "IMAGE_URL": config['IMAGE_URL'] + settings.MEDIA_URL})

        font_config = FontConfiguration()
        css = CSS(string=''' @page { 'size': 'A4', 'encoding': "UTF-8", 'enable-local-file-access': None } body { font-family: "Times New Roman", Times, serif; !important;font-size: 13px; } ''', font_config=font_config)
        
        pdf_buffer = io.BytesIO()
        HTML(string=html).write_pdf(pdf_buffer, stylesheets=[css])

        pdf_buffer.seek(0)

        base64_contents = base64.b64encode(pdf_buffer.getvalue()).decode('utf-8')

        return base64_contents