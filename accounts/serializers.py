from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ['balance', 'account_number']
    

    def validate(self, data):
        user = self.context['request'].user
        if Account.objects.filter(user=user).count() >= 5:
            raise serializers.ValidationError("You cannot have more than 5 accounts.")
        
        return data