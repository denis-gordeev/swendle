from api.models import Cluster


def menubar(request):
    return {'clusters': Cluster.objects.all()}
