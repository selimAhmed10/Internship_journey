import time
# Used to inspect executed sql queries
from django.db import connection
# Captures all queries executed inside a block
from django.test.utils import CaptureQueriesContext
from fin.models import Transaction


def report():
    with CaptureQueriesContext(connection) as total_executed_query:
        start=time.time()
        trans=Transaction.objects.all()[:5]
        for t in trans:
            t.account.account_number #access related account with accounht number for each transaction
        end=time.time()

    before_query=len(total_executed_query)
    before_time=(end-start)

    with CaptureQueriesContext(connection) as total_executed_query_after:
        starta=time.time()
        transa=(Transaction.objects.select_related("account")[:5])
        for t in transa:
            t.account.account_number
        enda=time.time()

    after_query=len(total_executed_query_after)
    after_time=(enda-starta)

    print(f"Before Optimization:{before_query} queries and time {before_time:.2f}")
    print(f"After Optimization:{after_query} queries and time {after_time:.2f}")