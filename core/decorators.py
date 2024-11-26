from django.http import JsonResponse

# Decorator to restrict access based on user roles (groups)
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({"message": "You are not authenticated"}, status=401)

            user_groups = [group.name for group in request.user.groups.all()]
            if not any(group in allowed_roles for group in user_groups):
                return JsonResponse({"message": "You are not authorized"}, status=403)
            return view_func(request, *args, **kwargs)
        return wrapper_func
    return decorator
