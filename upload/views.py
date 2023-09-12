import logging
import json
from pprint import pprint

from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .statement_parser.parser import get_pdf_text, parse_statement_text

# Initialize logger
logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class ProcessPdfView(View):

    def post(self, request, *args, **kwargs):
        try:
            uploaded_file = request.FILES.get('statement', None)
            password = request.POST.get('password', None)

            if not password and upload_file:
                response = {'status': 'error', 'message': 'Payload is not valid'}
                return JsonResponse(response)

            pdf_data = get_pdf_text(uploaded_file, password)

            if (pdf_data.get('error', None)):
                response = {'status': 'error', 'message': pdf_data['error']}
                return JsonResponse(response)

            text_content = pdf_data.get('text', None)
            print(f"Text is {len(text_content)} words long")
            statement_list = text_content.split("\n")
            parsed_statement = parse_statement_text(statement_list)

            response = {
                'status': 'success',
                'message': 'PDF processed successfully',
                'results': parsed_statement
            }

            return JsonResponse(response)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'An error occurred: {str(e)}'})
