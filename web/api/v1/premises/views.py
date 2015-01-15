from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from premises.models import Contention
from .serializers import ContentionSerializer, PremisesSerializer


class ContentionViewset(viewsets.ModelViewSet):
    queryset = Contention.objects.filter(is_published=True)\
                                 .prefetch_related('premises')\
                                 .select_related('user', 'premises__parent',
                                                 'premises__user')
    permission_classes = (permissions.AllowAny,)
    serializer_class = ContentionSerializer
    paginate_by = 20

    @detail_route()
    def premises(self, request, pk=None):
        contention = self.get_object()
        serializer = PremisesSerializer(contention.premises.all(), many=True)
        return Response(serializer.data)


contention_list = ContentionViewset.as_view({'get': 'list'})
contention_detail = ContentionViewset.as_view({'get': 'retrieve'})
premises_list = ContentionViewset.as_view({'get': 'premises'})
