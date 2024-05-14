def user_authenticated(request):
    return {
        'is_authenticated': 'username' in request.COOKIES
    }