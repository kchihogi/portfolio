from django.shortcuts import get_object_or_404, get_list_or_404,render

from .models import Profile, Work

from utils.logger import Logger
log = Logger("mylog")

def index(request):
    prof = get_list_or_404(Profile)[-1]
    works = Work.objects.all()

    log.logger.info("profile title:%s" % prof.title)

    for work in works:
        log.logger.info("work title:%s" % work.title)


    context = {'profile': prof,'works': works}
    return render(request, 'portfolio/index.html', context)