from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_permission(self,request,view):
        return request.user and request.user.is_authenticated

    def has_object(self,request,view,obj):
        #GET method 일 때는 허락
        if request.method in permissions.SAFE_METHODS:
            return True
        #PATCH, POST 등의 수정을 가하는 거면 작성자 일 때만 허락
        return request.user == obj.owner