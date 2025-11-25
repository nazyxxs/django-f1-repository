from django.shortcuts import render, get_object_or_404, redirect
from f1.models import Principals
from .forms import PrincipalForm


def principal_list(request):
    principals = Principals.objects.all()
    return render(request, 'frontend/principal_list.html', {'principals': principals})


def principal_detail(request, pk):
    principal = get_object_or_404(Principals, pk=pk)

    # DELETE
    if request.method == 'POST':
        principal.delete()
        return redirect('principal_list')

    return render(request, 'frontend/principal_detail.html', {'principal': principal})


def principal_add(request):
    if request.method == 'POST':
        form = PrincipalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('principal_list')
    else:
        form = PrincipalForm()

    return render(request, 'frontend/principal_form.html', {'form': form})


def principal_edit(request, pk):
    principal = get_object_or_404(Principals, pk=pk)

    if request.method == 'POST':
        form = PrincipalForm(request.POST, instance=principal)
        if form.is_valid():
            form.save()
            return redirect('principal_detail', pk=pk)
    else:
        form = PrincipalForm(instance=principal)

    return render(request, 'frontend/principal_form.html', {'form': form})

def principal_delete(request, pk):
    principal = get_object_or_404(Principals, pk=pk)

    if request.method == 'POST':
        principal.delete()
        return redirect('principal_list')

    return render(request, 'frontend/principal_confirm_delete.html', {
        'principal': principal
    })
