from django.shortcuts import render

# Create your views here.
def index(request):
    active_link = 'index'
    return render(
        request = request,
        template_name = 'core/index.html',
        context = {
            'active_link':active_link
        }
    )

    
