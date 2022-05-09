from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, get_list_or_404,render
from django.views import generic
import math

from .models import Profile, Work, Work_Language_Skill_RelationShip,Language_Skill

from utils.logger import Logger
log = Logger("mylog")

class IndexView():
    def index(request):
        prof = get_list_or_404(Profile)[-1]

        MAX_WORK = 6
        HALF_WORK = math.ceil(MAX_WORK/2)
        works = []

        prefetch = Prefetch('Lang_Works', queryset=Work_Language_Skill_RelationShip.objects.select_related('Language_Skill').order_by('sort'), to_attr='details')
        tmpworks=Work.objects.filter(private=0).order_by('sort').prefetch_related(prefetch)

        if tmpworks.count() >= HALF_WORK:
            tmpworks = tmpworks[:HALF_WORK]

        works += tmpworks
        works += Work.objects.exclude(private=0).order_by('sort').prefetch_related(prefetch)[:MAX_WORK - tmpworks.count()]

        context = {'profile': prof,'works': works, 'MAX_WORK' : MAX_WORK}
        return render(request, 'portfolio/index.html', context)
    
class WorkView:
    def get_work(request, pk):
        prof = get_list_or_404(Profile)[-1]
        work = get_object_or_404(Work, pk=pk)
        context = {'profile': prof,'work': work}
        return render(request, 'portfolio/work.html', context)
