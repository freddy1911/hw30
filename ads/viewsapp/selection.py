from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import Selection
from ads.permissions import IsCreateBySelectionOwner
from ads.serializers import SelectionSerializer, SelectionCreateSerializer


class SelectionViewSet(ModelViewSet):
    queryset = Selection.objects.all()
    default_serializer = SelectionSerializer
    serializer_classes = {
        'create': SelectionCreateSerializer,
    }
    default_permission = [AllowAny(), ]
    permission_list = {'create': [IsAuthenticated()],
                       'update': [IsAuthenticated(), IsCreateBySelectionOwner()],
                       'partial_update': [IsAuthenticated(), IsCreateBySelectionOwner()],
                       'destroy': [IsAuthenticated(), IsCreateBySelectionOwner()],
                       }

    def get_permissions(self):
        return self.permission_list.get(self.action, self.default_permission)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer)