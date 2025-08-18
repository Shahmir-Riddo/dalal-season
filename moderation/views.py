from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import AdminLoginForm
from django.contrib import messages
from archive.models import Dalal, District
from django.contrib.auth.decorators import user_passes_test
from .forms import DalalForm, DalalFilterForm
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import logout

def is_superuser_check(user):
    return user.is_authenticated and user.is_superuser


# Create your views here.

def ds_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        form = AdminLoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            if user is not None and user.is_superuser:
                login(request, user)
                messages.success(request, "Login Successful")
                return redirect('/ds-admin/dashboard')
            else:
                messages.error(request, "Invalid username or password.")
                return render(request, 'admin_login.html', context={'form': form})

        else:
            messages.error(request, "Invalid Credentials.")
            return render(request, 'admin_login.html', context={'form': form})

    else:
        form = AdminLoginForm()
        return render(request, 'admin_login.html', context={'form': form})

@user_passes_test(is_superuser_check)
def admin_dashboard(request):
    dalal_list = Dalal.objects.all().only('name', 'status', 'shoe_count')
    ranking = dalal_list.order_by('-shoe_count')
    total_dalal_count = len(dalal_list)
    fugitive_count = Dalal.objects.filter(status='fugitive').count()
    captured_count = Dalal.objects.filter(status='captured').count()
    terminated_count = Dalal.objects.filter(status='terminated').count()
    
    context = {'dalal_list': dalal_list,
               'ranking': ranking,
               'total_dalal_count': total_dalal_count,
               'fugitive_count': fugitive_count,
               'captured_count': captured_count,
               'terminated_count': terminated_count,

               }
    return render(request, 'admin_dashboard.html', context)


@user_passes_test(is_superuser_check)
def add_dalal(request):
    if request.method == "POST":
        form = DalalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dalal_list')

    else:
        form = DalalForm()
        
    context = {'form': form}
    return render(request, 'add_dalal.html', context)




@user_passes_test(is_superuser_check)
def dalal_list(request):
    form = DalalFilterForm(request.GET)
    dalals = Dalal.objects.all()

    if form.is_valid():
            
        search = form.cleaned_data['search']
        status = form.cleaned_data['status']
        district = form.cleaned_data['district']
        date_from = form.cleaned_data['date_from']
        date_to = form.cleaned_data['date_to']

        if search:
            dalals = dalals.filter(name__icontains=search)

        if status:
            dalals = dalals.filter(status=status)

        if district:
            dalals = dalals.filter(district=district)

        if date_from:
            dalals = dalals.filter(date_added__gte=date_from)

        if date_to:
            dalals = dalals.filter(date_added__lte=date_to)


        paginator = Paginator(dalals, 12)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)


    context = {'page_obj': page_obj,
               'form': form}

    return render(request, 'dalal_list.html', context)

@require_POST
@user_passes_test(is_superuser_check)
def delete_dalal(request):
    dalal_id = request.POST.get('dalal_id')
    dalal = get_object_or_404(Dalal, id=dalal_id)
    dalal.delete()
    return redirect('admin_dashboard')



@user_passes_test(is_superuser_check)
def edit_dalal(request, id):
    dalal_id = id
    dalal = get_object_or_404(Dalal, id=dalal_id)
    if request.method == "POST":
        form = DalalForm(request.POST, request.FILES, instance=dalal)
        if form.is_valid():
            form.save()
            return redirect('dalal_list')
        else:
            return render(request, 'edit_dalal.html', context={'form': form})

    else:
        form = DalalForm(instance=dalal)
        return render(request, 'edit_dalal.html', context={'form': form})




def logout_view(request):
    logout(request)
    return redirect('ds_login')