from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .forms import ImageCrateForm
from .models import Image
from django.http import HttpRequest


@login_required
def image_create(request: HttpRequest):
    if request.method == 'POST':
        form = ImageCrateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_image: Image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            messages.success(request, 'Image added successfully')
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCrateForm(data=request.GET)

    return render(
        request,
        'images/image/create.html',
        {
            'section': 'images',
            'form': form
        }
    )

def image_detail(request: HttpRequest, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(
        request,
        'images/image/detail.html',
        {'section': 'images', 'image': image}
    )
