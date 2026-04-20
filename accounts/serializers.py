from rest_framework import serializers
from django.db import transaction
from .models import Account, Transaction

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


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['sender', 'receiver', 'amount', 'transaction_type']

    # Validate that sender and receiver are not the same account
    def validate(self, data):
        user = self.context['request'].user
        sender = data.get('sender')
        receiver = data.get('receiver')
        transaction_type = data.get('transaction_type')

        # prevent self-transfers
        if sender and receiver and sender == receiver:
            raise serializers.ValidationError('Sender and receiver cannot be the same account')
        
        # Logic for Transfers transactions
        if transaction_type == 'TRANSFER' and (not sender or not receiver):
            raise serializers.ValidationError('A transfer requires both sender and receiver')
        
        # Check ownership of sender account
        if sender and sender.user != user:
            raise serializers.ValidationError('You are not the owner of the sender account')
        
        # Check ownership of receiver account
        if transaction_type == 'DEPOSIT' and receiver and receiver.user != user:
            raise serializers.ValidationError('You are not the owner of the receiver account')
        
        return data

    # Override the create method to handle the transaction logic
    def create(self, validated_data):
        sender = validated_data.get('sender')
        receiver = validated_data.get('receiver')
        amount = validated_data.get('amount')

        # Start the Lock
        with transaction.atomic():
            # Money Out
            if sender:
                sender_acc = Account.objects.select_for_update().get(id=sender.id)
                # Check fo sufficient balance
                if sender_acc.balance < amount:
                    raise serializers.ValidationError('Insufficient balance')
                sender_acc.balance -= amount
                sender_acc.save()

            # Money In
            if receiver:
                receiver_acc = Account.objects.select_for_update().get(id=receiver.id)
                receiver_acc.balance += amount 
                receiver_acc.save()

            # create record after the whole validation
            return super().create(validated_data)
