from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import cache_control
from datetime import timedelta,datetime
from django.utils import timezone
from order.models import Orders, OrdersItem
from django.db.models import Sum
from userAuthentication.models import CustomUser
from django.http import JsonResponse
from io import BytesIO
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from .models import *
import xlwt
import datetime




# Create your views here.


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="adminlogin")
def Dashboard(request):
    period = request.GET.get('period')
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')

    # Define start and end dates based on the selected period
    end_date = datetime.datetime.now()
    if period == 'today':
        start_date = end_date - timedelta(days=1)
    elif period == 'this_week':
        start_date = end_date - timedelta(weeks=1)
    elif period == 'this_year':
        start_date = end_date - timedelta(days=365)
    else:
        # Default to daily if an invalid period is provided
        start_date = end_date - timedelta(days=365*3)

    # Filter orders based on the selected period
    orders = Orders.objects.filter(order_date__range=[start_date, end_date])
    print(orders)

    revenue = orders.aggregate(total_revenue=Sum('total_purchase_amount'))['total_revenue'] or 0
    total_profit = revenue * 0.3
    users = orders.values('user').distinct().count()


    
    items = OrdersItem.objects.all().order_by("-order__order_date")

    if start and end:

        items = items.filter(order__order_date__range=[start,end])
    else:
        messages.error(request,'choose start date and end date')    
        

    
    context = {
        'total_revenue': revenue,
        'total_users': users,
        'total_orders': orders.count(),
        'total_profit': total_profit,
        'start_date': start_date,
        'end_date': end_date,
        'items': items,

    }

    return render(request, 'adminside/dashboard.html', context)



def excel_report(request):
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = (
        "attachment; filename=SalesReport-" + str(datetime.datetime.now()) + "-.xls"
    )
    work_b = xlwt.Workbook(encoding="utf-8")
    work_s = work_b.add_sheet("SalesReport")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = [
        "Order ID",
        "User",
        "Date",
        "Time",
        "Product",
        "Quantity",
        "Price",
        "Payment Mode",
        "Total Price",  # Add the "Total Price" column
    ]

    for column_num in range(len(columns)):
        work_s.write(row_num, column_num, columns[column_num], font_style)
    font_style = xlwt.XFStyle()

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if not start_date:
        start_date = datetime.datetime.now() - timedelta(days=3 * 365)

    if not end_date:
        end_date = datetime.datetime.now()

    orders = (
        Orders.objects.all()
        .order_by("-order_date")
        .filter(order_date__range=[start_date, end_date])
        .values_list(
            # Use the correct field name here (e.g., "orderitem__variant__product__products_name")
            "order_id",
            "user__first_name",
            "order_date__date",
            "order_date__time",
            "ordersitem__product__products_name",  # Assuming the correct field is "orderitem"
            "ordersitem__quantity",
            "ordersitem__price",
            "payment_method",
            "total_purchase_amount",
        )
    )

    total_price = 0  # Initialize total price
    for order in orders:
        row_num += 1
        for col_num in range(len(order)):
            work_s.write(row_num, col_num, str(order[col_num]), font_style)

        total_price += order[6]  # Add the price of each order to the total
        

    # Write the total price in the last row
    work_s.write(row_num + 1, 8, str(total_price), font_style)

    work_b.save(response)

    return response

    
 
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None   


class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
            start_date = request.GET.get("start_date")
            end_date = request.GET.get("end_date")
            if start_date == "":
                start_date = datetime.datetime.now() - timedelta(days=3 * 365)
            if end_date == "":
                end_date = datetime.datetime.now()
                print(end_date)

            orders = Orders.objects.all().order_by("-order_date").filter(order_date__range=[start_date, end_date])

            # Calculate the total price
            total_price = sum(order.total_purchase_amount for order in orders)

        
            data = {
                "company": "RUPER",
                "address": start_date,
                "city": "Calicut",
                "state": "Kerala",
                "zipcode": "673006",
                "orders": orders,
                "phone": end_date,
                "email": "favasabdulnassar@gmail.com",
                "website": "ruper.com",
                "total_price": total_price,  # Pass the total price to the context
            }
            pdf = render_to_pdf("adminside/sales_report_pdf.html",data)


            response = HttpResponse(pdf, content_type="application/pdf")
            filename = f"Sales_report_{datetime.datetime.now()}.pdf"
            content = "attachment; filename=%s" % (filename)
            response["Content-Disposition"] = content
            return response







