from rest_framework import renderers
import json
from rest_framework import status

class ResponseData:
    @staticmethod
    def custom_render(errors):
        formatted_errors = []
        for error in errors:
            field_name, error_message = error.split(' ', 1)
            formatted_errors.append(f"{field_name} field {error_message.lower()}")
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "hasError": True,
            "message": "Failed",
            "error": ", ".join(formatted_errors)
        }
    @staticmethod
    def get_success_data(serializer_data):
        return {
            'code': status.HTTP_200_OK,
            'hasError': False,
            'message': 'Success',
            'list': serializer_data
        }
    @staticmethod
    def get_success_view(serializer_data):
        return {
            'code': status.HTTP_200_OK,
            'hasError': False,
            'message': 'Success',
            'view': serializer_data
        }
    @staticmethod
    def get_success_login_view(accessToken,refreshToken,serializer_data):
        return {
            'code': status.HTTP_200_OK,
            'hasError': False,
            'message': 'Login successfully',
            'accessToken': accessToken,
            'refreshToken': refreshToken,
            'view':serializer_data
        }
    @staticmethod
    def get_success_message(serializer_data):
        return {
            'code': status.HTTP_200_OK,
            'hasError': False,
            'message': serializer_data
        }
    @staticmethod
    def get_error_data(error_message):
        return {
            'code': status.HTTP_400_BAD_REQUEST,
            'hasError': True,
            'message': 'Failed',
            'error': error_message
        }
    @staticmethod 
    def get_logout_message(success_message):
        return {
            'code': status.HTTP_200_OK,
            'hasError': False,
            'message': success_message
        }
    @staticmethod
    def get_created_data(serializer_data):
        return {
            'code': status.HTTP_201_CREATED,
            'hasError': False,
            'message': 'Resource created successfully',
            'data': serializer_data
        }
    @staticmethod
    def get_updated_data(serializer_data):
        return {
            'code': status.HTTP_200_OK,
            'hasError': False,
            'message': 'Resource updated successfully',
            'data': serializer_data
        }
    @staticmethod
    def get_updated_list(serializer_data):
        return {
            'code': status.HTTP_200_OK,
            'hasError': False,
            'message': 'Resource updated successfully',
            'list': serializer_data
        }
    @staticmethod
    def get_created_view(serializer_data):
        return {
            'code': status.HTTP_201_CREATED,
            'hasError': False,
            'message': 'Resource created successfully',
            'view': serializer_data
        }
    @staticmethod
    def get_no_content_data():
        return {
            'code': status.HTTP_204_NO_CONTENT,
            'hasError': False,
            'message': 'No content'
        }
    @staticmethod
    def get_bad_request_data(error_message):
        return {
            'code': status.HTTP_400_BAD_REQUEST,
            'hasError': True,
            'message': 'Bad request',
            'error': error_message
        }
    @staticmethod
    def get_unauthorized_data(error_message):
        return {
            'code': status.HTTP_401_UNAUTHORIZED,
            'hasError': True,
            'message': 'Unauthorized',
            'error': error_message
        }
    @staticmethod
    def get_forbidden_data():
        return {
            'code': status.HTTP_403_FORBIDDEN,
            'hasError': True,
            'message': 'Forbidden',
            'error': 'You do not have permission to perform this action'
        }
    @staticmethod
    def get_not_found_data(error_message):
        return {
            'code': status.HTTP_404_NOT_FOUND,
            'hasError': True,
            'message': 'Not found',
            'error': error_message
        }
    @staticmethod
    def get_method_not_allowed_data():
        return {
            'code': status.HTTP_405_METHOD_NOT_ALLOWED,
            'hasError': True,
            'message': 'Method not allowed',
            'error': 'The requested method is not allowed for this resource'
        }
    @staticmethod
    def get_internal_server_error_data():
        return {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'hasError': True,
            'message': 'Internal server error',
            'error': 'An unexpected error occurred on the server'
        }
    @staticmethod
    def get_empty_list_data():
        return {
            'code': status.HTTP_200_OK,
            'hasError': False,
            'message': 'Empty list retrieved',
            'list': []
        }
    @staticmethod
    def get_deleted_data():
        return {
            'code': status.HTTP_200_OK,
            'hasError': False,
            'message': 'Resource deleted successfully'
        }
    @staticmethod
    def get_success_booking_cancel_view(serializer_data):
        return {
            'code': status.HTTP_200_OK,
            'hasError': False,
            'message': 'Your Booking has been cancelled successfully',
            'view': serializer_data
        }

### Account 
class UserRenderer(renderers.JSONRenderer):
    charset='utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if 'ErrorDetail' in str(data):
            response = json.dumps({'errors':data})
        else:
            response = json.dumps(data)
        return response
    
### User Token Renderer
class UserTokenRenderer(renderers.JSONRenderer):
    charset = 'utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if 'code' in data and data['code'] == 'token_not_valid':
            error_messages = data.get('messages', [])
            if error_messages:
                error_message = error_messages[0].get('message', 'Token is invalid or expired')
            else:
                error_message = 'Token is invalid or expired'
            response = json.dumps(ResponseData.get_unauthorized_data(error_message))
        else:
            response = json.dumps(data)
        return response