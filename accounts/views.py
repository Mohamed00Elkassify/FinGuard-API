from rest_framework import viewsets, permissions
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from django.db.models import Q
from accounts.serializers import AccountSerializer, TransactionSerializer
from accounts.models import Account, Transaction

# Create your views here.
class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)
    

class TransactionViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    '''
    POST: Create a new transaction
    GET: List only my transactions
    GET {id}: Retrieve a specific transaction detail
    DENIED: PUT, PATCH, or DELETE (Immutable records)
    '''
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(
            Q(sender__user=user) | Q(receiver__user=user)
        ).order_by('-timestamp')

