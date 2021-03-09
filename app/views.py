from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib import messages

from guardian.decorators import permission_required_or_403
from guardian.shortcuts import get_objects_for_user

from .models import PlotlyDashApp
from .forms import PlotlyDashAppForm
from common.dash_validator import DashValidator

@login_required(login_url="/login/")
def index(request):
    context = {}
    context['segment'] = 'index'

    dash_apps = get_objects_for_user(request.user, 'app.view_plotlydashapp')
    context['dash_apps'] = dash_apps.order_by('-id')

    return render(request, 'index.html', context)

@login_required(login_url="/login/")
@staff_member_required(login_url="/login")
def dash_create(request):
    if request.method == 'POST':
        form = PlotlyDashAppForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dash Created Successfully')
            return redirect('app:home')
    else:
        form = PlotlyDashAppForm()
    return render(request, 'app/dash_create.html', {'form': form})

@login_required(login_url="/login/")
@permission_required_or_403('app.view_plotlydashapp', (PlotlyDashApp, 'unique_id', 'dash_uid'))
def dash_show(request, dash_uid):
    obj = get_object_or_404(PlotlyDashApp, unique_id=dash_uid)
    validator = DashValidator(obj.dash_file)

    context = {}
    context['segment'] = 'index'

    try:
        validator.load_module()
        context['app_name'] = obj.app_name
    except Exception as ex:
        messages.error(request, "An exception raised through dash app:\n" + str(ex))
    
    return render(request, 'app/dash_show.html', context)