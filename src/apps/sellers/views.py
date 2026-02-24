from rest_framework.viewsets import ModelViewSet
from .models import Seller


class SellerViewSet(ModelViewSet):
    queryset = Seller.objects.all()
    # serializer_class = SellerSerializer  # TODO
