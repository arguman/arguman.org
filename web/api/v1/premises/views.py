from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import filters, status

from premises.models import Contention, Premise
from .serializers import (ContentionSerializer, PremisesSerializer,
                          PremiseReportSerializer)
from premises.utils import int_or_default
from premises.signals import supported_a_premise
from api.v1.account.serializers import UserProfileSerializer


class ContentionViewset(viewsets.ModelViewSet):
    queryset = Contention.objects.filter(is_published=True)\
                                 .prefetch_related('premises')\
                                 .select_related('user', 'premises__parent',
                                                 'premises__user')
    permission_classes = (permissions.AllowAny,)
    serializer_class = ContentionSerializer
    paginate_by = 20
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)

    @detail_route()
    def premises(self, request, pk=None):
        contention = self.get_object()
        serializer = PremisesSerializer(contention.premises.all(), many=True)
        return Response(serializer.data)


class PremiseDetailView(viewsets.ModelViewSet):
    queryset = Premise.objects.filter(is_approved=True)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = PremisesSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'premise_id'

    def filter_queryset(self, queryset):
        argument_id = int_or_default(self.kwargs.get('pk'), default=0)
        return queryset.filter(argument__id=argument_id,
                               argument__is_published=True)

    @detail_route(methods=['post'])
    def report(self, request, pk=None, premise_id=None):
        premise = self.get_object()
        serializer = PremiseReportSerializer(
            data=request.DATA, initial={'reporter': request.user,
                                        'premise': premise,
                                        'contention': premise.argument})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


    @detail_route(methods=['post'])
    def support(self, request, pk=None, premise_id=None):
        premise = self.get_object()
        if premise.supporters.filter(id=request.user.id).exists():
            return Response({'message': "Onermeyi Zaten destekliyorsun"},
                            status=status.HTTP_400_BAD_REQUEST)
        premise.supporters.add(request.user)
        supported_a_premise.send(sender=self, premise=premise,
                                 user=self.request.user)
        return Response(status=status.HTTP_201_CREATED)

    @detail_route(methods=['get'])
    def supporters(self, request, pk=None, premise_id=None):
        premise = self.get_object()
        page = self.paginate_queryset(premise.supporters.all())
        serializer = self.get_pagination_serializer(page)
        return Response(serializer.data)

    @detail_route(methods=['delete'])
    def unsupport(self, request, pk=None, premise_id=None):
        premise = self.get_object()
        if not premise.supporters.filter(id=request.user.id).exists():
            return Response({'message': "Once onermeyi desteklemen gerekiyor"},
                            status=status.HTTP_400_BAD_REQUEST)
        premise.supporters.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


contention_list = ContentionViewset.as_view({'get': 'list'})
contention_detail = ContentionViewset.as_view({'get': 'retrieve'})
premises_list = ContentionViewset.as_view({'get': 'premises'})
premise_detail = PremiseDetailView.as_view({'get': 'retrieve'})
premise_report = PremiseDetailView.as_view({'post': 'report'})
premise_support = PremiseDetailView.as_view({'post': 'support',
                                             'delete': 'unsupport'})
premise_supporters = PremiseDetailView.as_view(
    {'get': 'supporters'},
    serializer_class=UserProfileSerializer)
