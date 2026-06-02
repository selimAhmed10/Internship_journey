from django.core.management.base import BaseCommand
from datetime import date, timedelta
from fin.models import User, Account, Card, Merchant, Transaction

class Command(BaseCommand):
    help='Seed database with test data'

    def handle(self, *args, **options):
        self.stdout.write("Seeding data")

        # Create Admin
        User.objects.create_superuser(
            username='admin',
            password='admin123',
            name='Admin User',
            email='admin@example.com',
            phone='01999999999',
            role='admin'
        )

        # Create Customers
        customer1=User.objects.create_user(
            username='rahim',
            password='pass123',
            name='Rahim',
            email='rahim@gmail.com',
            phone='0170000',
            role='customer'
        )
        customer2=User.objects.create_user(
            username='sultana',
            password='pass123',
            name='Sultana',
            email='sultana@gmail.com',
            phone='0171888888',
            role='customer'
        )
        customer3=User.objects.create_user(
            username='karim', 
            password='pass123',
            name='Karim Uddin', 
            email='karim@gmail.com',
            phone='01710000003', 
            role='customer'
        )

        # Create Merchant User
        merchant_user=User.objects.create_user(
            username='merchant1', 
            password='pass123',
            name='ABC Shop', 
            email='merchant@gmail.com',
            phone='01810000001', 
            role='merchant'
        )

        # Create Agent User
        User.objects.create_user(
            username='agent1',
            password='pass123',
            name='Hasan Agent',
            email='agent@gmail.com',
            phone='01610000001',
            role='agent'
        )

        # Create Accounts
        acc1 = Account.objects.create(
            user=customer1,
            account_number='SAV1001',
            account_type='saving', 
            balance=50000
        )
        acc2=Account.objects.create(
            user=customer1, 
            account_number='STU1001',
            account_type='student',
            balance=10000
        )
        acc3=Account.objects.create(
            user=customer2,
            account_number='SAV1002',
            account_type='saving',
            balance=35000
        )
        acc4=Account.objects.create(
            user=customer3,
            account_number='SAV1003',
            account_type='saving',
            balance=25000
        )
        
        Account.objects.create(
            user=merchant_user, 
            account_number='MRCH001',
            account_type='saving', 
            balance=0
        )

        # Create Cards
        Card.objects.create(
            account=acc1,
            card_number='4111111111111111',
            card_type='debit',
            expiry_date=date.today() + timedelta(days=365*4)
        )
        Card.objects.create(
            account=acc3,
            card_number='4222222222222222',
            card_type='debit',
            expiry_date=date.today() + timedelta(days=365*4)
        )

        # Create Merchants
        Merchant.objects.create(name='ABC Shop', merchant_id='MERCH001',category='ecommerce')
        Merchant.objects.create(name='Local Grocery',merchant_id='MERCH002',category='grocery')
        Merchant.objects.create(name='City Utility',merchant_id='MERCH003',category='utility')

        # Create Transactions
        merchants=list(Merchant.objects.all())

        Transaction.objects.create(
            account=acc1,
            merchant=None,
            card=None,
            amount=5000, 
            transaction_type='debit', 
            status='success',
            reference_id='TXN1001'
        )
        Transaction.objects.create(
            account=acc3, 
            merchant=None, 
            card=None,
            amount=5000, 
            transaction_type='credit', 
            status='success',
            reference_id='TXN1002'
        )
        Transaction.objects.create(
            account=acc1, 
            merchant=merchants[0], 
            card=None,
            amount=1500, 
            transaction_type='debit', 
            status='success',
            reference_id='TXN1003'
        )
        Transaction.objects.create(
            account=acc3,
            merchant=merchants[1], 
            card=None,
            amount=2000, 
            transaction_type='debit', 
            status='failed',
            reference_id='TXN1004'
        )
        Transaction.objects.create(
            account=acc2, 
            merchant=None, 
            card=None,
            amount=1000, 
            transaction_type='debit', 
            status='pending',
            reference_id='TXN1005'
        )
        Transaction.objects.create(
            account=acc4,
            merchant=merchants[2], 
            card=None,
            amount=3000, 
            transaction_type='debit', 
            status='success',
            reference_id='TXN1006'
        )

        # Update balances
        acc1.balance -= 5000
        acc1.balance -= 1500
        acc1.save()
        acc3.balance += 5000
        acc3.save()
        acc4.balance -= 3000
        acc4.save()

        self.stdout.write(self.style.SUCCESS("\nDatabase seeded successfully!"))