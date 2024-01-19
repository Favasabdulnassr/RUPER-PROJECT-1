from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import cache_control
from datetime import timedelta,datetime
from django.utils import timezone
from order.models import Orders, OrdersItem
from django.db.models import Sum
from userAuthentication.models import CustomUser
from django.http import JsonResponse



# Create your views here.


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="adminlogin")


def Dashboard(request):
    period = request.GET.get('period')
    print(request.GET)

    # Define start and end dates based on the selected period
    end_date = datetime.now()
    print(end_date)
    if period == 'today':
        start_date = end_date - timedelta(days=1)
        print(start_date)
    elif period == 'this_week':
        start_date = end_date - timedelta(weeks=1)
    elif period == 'this_year':
        start_date = end_date - timedelta(days=365)
    else:
        # Default to daily if an invalid period is provided
        start_date = end_date - timedelta(days=1)

    # Filter orders based on the selected period
    orders = Orders.objects.filter(order_date__range=[start_date, end_date])

    revenue = orders.aggregate(total_revenue=Sum('total_purchase_amount'))['total_revenue']
    total_profit = revenue * 0.3
    users = orders.values('user').distinct().count()
    context = {
        'total_revenue': revenue,
        'total_users': users,
        'total_orders': orders.count(),
        'total_profit': total_profit,
        'start_date': start_date,
        'end_date': end_date,

    }

    return render(request, 'adminside/dashboard.html', context)