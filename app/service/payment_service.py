from app.data_access.payment_repository import PaymentRepository
from app.models.Payment import *

class PaymentService:
    """! PaymentService class for business logic.
    This class contains methods to interact with the PaymentRepository class.
    """
    def __init__(self, payment_repository: PaymentRepository):
        self.payment_repository = payment_repository

    def get_payment(self, customer_id=None, id=None):
        """! Get a payment by customer ID or ID or all payments.
        @param customer_id: Customer ID.
        @param id: Payment ID.
        @return: Payment object or list of Payment objects.
        """
        try:
            return self.payment_repository.get_payment(customer_id, id)
        except Exception as e:
            return str(e)

    def create_payment(self, **kwargs):
        """! Create a payment.
        @param kwargs: Payment details.
        @return: Payment object or error message.
        """
        try:
            if kwargs.get('payment_method') == 'Credit':
                payment = CreditCardPayment(
                    paymentID=self.payment_repository.generate_payment_id(),
                    cardNumber=kwargs.get('cardNumber'),
                    cardExpiryDate=kwargs.get('cardExpiryDate'),
                    cardHolder=kwargs.get('cardHolder'),
                    cardType=kwargs.get('cardType'),
                    cardCVV=kwargs.get('cardCVV'),
                    paymentAmount=kwargs.get('paymentAmount'),
                    paymentType=kwargs.get('paymentType'),
                    customer_id=kwargs.get('customer_id')
                    )
            elif kwargs.get('payment_method') == 'Debit':
                payment = DebitCardPayment(
                    paymentID=self.payment_repository.generate_payment_id(),
                    bankName=kwargs.get('bankName'),
                    debitCardNumber=kwargs.get('debitCardNumber'),
                    paymentAmount=kwargs.get('paymentAmount'),
                    paymentType=kwargs.get('paymentType'),
                    customer_id=kwargs.get('customer_id')
                    )
            else:
                rlt = 'Invalid payment method'
                return rlt
            return self.payment_repository.create_payment(payment)
        except Exception as e:
            return str(e)
        
   