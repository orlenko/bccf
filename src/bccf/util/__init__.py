
import random


def generate_transaction_id():
    """
    Create a unique transaction number of billing payments

    Transaction number format:
        XXXXXXXXXXXXXXXXXXXXXXXX
    """
    from cartridge.shop.models import Order

    transaction_id = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _i in range(25))
    if transaction_id and not Order.objects.filter(transaction_id=transaction_id).exists():
        return transaction_id
    else:
        return generate_transaction_id()