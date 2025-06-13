from rest_framework.response import Response

class BaseResponseMixin:
    def custom_response(self, data, message="Success", status=True):
        return Response({
            "status": status,
            "message": message,
            "data": data
        })

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return self.custom_response(response.data, message="Created successfully")

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return self.custom_response(response.data, message="Retrieved successfully")

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return self.custom_response(response.data, message="Updated successfully")

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return self.custom_response(None, message="Deleted successfully")
