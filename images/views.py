import redis
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .forms import ImageCrateForm
from .models import Image
from django.http import HttpRequest, HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from actions.utils import create_action


r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

@login_required
def image_list(request: HttpRequest):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)

    if images_only:
        return render(
            request,
            'images/image/list_images.html',
            {'section': 'images', 'images': images}
        )
    return render(
        request,
        'images/image/list.html',
        {'section': 'images', 'images': images}
    )


@login_required
def image_like(request: HttpRequest):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})

@login_required
def image_create(request: HttpRequest):
    if request.method == 'POST':
        form = ImageCrateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_image: Image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            create_action(request.user, 'bookmarked image', new_image)
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
    # increment total image views by 1
    total_views = r.incr(f'image:{image.id}:views')
    r.zincrby('image_ranking', 1, image.id)
    print(image.title)
    return render(
        request,
        'images/image/detail.html',
        {'section': 'images',
         'image': image,
         'total_views': total_views}
    )

@login_required
def image_ranking(request: HttpRequest):
    image_ranking = r.zrange('image_ranking', 0 , -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    most_viewd = list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewd.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(
        request,
        'images/image/ranking.html',
        {
            'section': 'images',
            'most_viewd': most_viewd
        }
    )
