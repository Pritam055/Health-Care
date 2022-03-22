from django.shortcuts import redirect

def onlyAllowNonAuthenticated(func):

    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('predict:index')
        return func(request, *args, **kwargs)

    return wrapper