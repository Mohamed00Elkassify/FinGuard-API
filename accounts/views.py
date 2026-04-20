from rest_framework import viewsets, permissions
from accounts.serializers import AccountSerializer
from accounts.models import Account

# Create your views here.
class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)
    

