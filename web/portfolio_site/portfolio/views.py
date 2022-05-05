from gc import callbacks
from django.shortcuts import get_object_or_404, get_list_or_404,render

from .models import Profile, Work

from utils.logger import Logger
log = Logger("mylog")

def index(request):
    prof = get_list_or_404(Profile)[-1]
    works = Work.objects.filter(private=0).order_by('sort')[:3]
    pworks = Work.objects.exclude(private=0).order_by('sort')[:3]
    context = {'profile': prof,'works': works,'private_works': pworks}
    return render(request, 'portfolio/index.html', context)