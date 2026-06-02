from django.db.models import Q,F,Sum,Count,Avg,Subquery,OuterRef,Case,When,Value,CharField,Exists
from django.db.models.functions import TruncDate
from fin.models import User,Account,Transaction,Card,Merchant

# 1-- Get all the customers
def all_customers():
    return User.objects.filter(role='customer')
# 1-- Get all the user
def all_user():
    return User.objects.all()
# 1-- Get all the merchent
def all_marchent():
    return User.objects.filter(role='merchent')
# 1-- Get all agent
def all_agent():
    return User.objects.filter(role='agent')


# 2-- Top highest balance account 
def highest_balance():
    return Account.objects.order_by('-balance')[:2]


# 3---- Total balance sum(all)
def total_balance():
    return Account.objects.aggregate(total=Sum('balance'))

# 4-----  Count accounts by account_type (multiple account type then count it)
def accounts_by_type():
    return Account.objects.values('account_type').annotate(count=Count('id'))

# 5------ Add 20% interest to savings accounts using the F(update directlyusing F)
def add_interest():
    return Account.objects.filter(account_type='saving').update(balance=F('balance')*3.05)

# 6----- Find  the frozen acount or the low balance accounts using or (balance less than 1000)
def frozen_low_balance():
    return Account.objects.filter(Q(status='frozen')|Q(balance__lt=1000))

# 7---- Transaction with have  account & merchant using select method 
def transaction_with_accoutn_marchent():
    return Transaction.objects.select_related('account','merchant').all()[:5]

# 8---- Users with their account using the prefecth -- all account using the using the query
def all_customer_list():
    return User.objects.prefetch_related('accounts').filter(role='customer')[:5]

# 9----  transaction count to each accounts
def trans_count():
    return Account.objects.annotate(tran_count=Count('transactions'))

# 10 ---- Average transaction amount(only the successfull transactions)
def average_transaction():
    return Transaction.objects.filter(status='success').aggregate(average=Avg('amount'))

# 11--- Label up the transaction in category 
def trans_level_up():
    return Transaction.objects.annotate(
        size=Case(
            When(amount__lt=500,then=Value('Small')),
            When(amount__gte=500,then=Value('Large')),
            default=Value('Medium'),
            output_field=CharField(max_length=30),
        )
    )

# 12 ---  find the latest transaction amount for each account indidividual
def latest_trans():
    #sub query (using the outerRef)    -- sortred by the lated created and show the one value after sorting it 
    latest=Transaction.objects.filter(account=OuterRef('id')).order_by('-created_at').values('amount')[:1]
    return Account.objects.annotate(last=Subquery(latest))

# 13 ---- Users who have made trans is it ezist or not exist 
def exists_example():
    return User.objects.filter(Exists(Transaction.objects.filter(account__user=OuterRef('id'))))

# 14 ---  Daily transaction summary(using date,sum of the total amount and sort the latest date obe the earlier)
def daily_summary():
    return Transaction.objects.annotate(date=TruncDate('created_at')).values('date').annotate(total=Sum('amount'),count=Count('id')).order_by('-date')

#15 --  All active card
def all_active_card():
    return Card.objects.filter(status='active').count()



def run_all_the_query():
    print()
    print(f"\All customers: {all_customers().count()}")
    print(f"All users: {all_user().count()}")
    print(f"All merchants: {all_marchent().count()}")
    print(f"All agents: {all_agent().count()}")
    print(f"Top highest balance accounts: {list(highest_balance())}")
    print(f"Total balance sum: {total_balance()}")
    print(f"Account count by type:{list(accounts_by_type())}")
    print(f"Savings accounts updated with interest:{add_interest()}")
    print(f"Frozen or low-balance accounts:{frozen_low_balance().count()}")
    print(f"Transactions with account and merchant:{transaction_with_accoutn_marchent().count()}")
    print(f"Customers with accounts (prefetch_related):{all_customer_list().count()}")
    print(f"Transaction count for each account:{list(trans_count().values('id', 'tran_count'))}")
    print(f"Average successful transaction amount:{average_transaction()}")
    print(f"Transactions categorized by amount size:{trans_level_up().count()}")
    print(f"Latest transaction amount for each account:{list(latest_trans().values('id', 'last'))}")
    print(f"Users who have made trans exist or not:{exists_example().count()}")
    print(f"Daily transaction summary:{list(daily_summary())}")
    print(f"All active cards:{all_active_card()}")