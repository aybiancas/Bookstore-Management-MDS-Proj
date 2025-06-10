from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.utils.timezone import now
from .models import Book, Category, Sale
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import timedelta
from .forms import SaleForm, StockForm, BookForm
from .models import Sale, Book
import plotly.graph_objs as go
import plotly.offline as opy


# chartul bar pentru totalul de carti dintr o luna
def monthly_sales_chart():
    six_months_ago = now().date() - timedelta(days=90)
    monthly_sales = (Sale.objects
                     .filter(date__date__gte=six_months_ago)
                     .extra(select={'month': "DATE_TRUNC('month', date)"})
                     .values('month')
                     .annotate(total_qty=Sum('qty'))
                     .order_by('month'))
    months = [entry['month'].strftime('%Y-%m') for entry in monthly_sales]
    qtys = [entry['total_qty'] for entry in monthly_sales]

    colors = {
        'qtys': '#6184F5'
    }
    bar_chart = go.Bar(x=months, y=qtys, name='Vanzari lunare', marker_color=colors['qtys'])
    layout = go.Layout(xaxis=dict(title='Luna'), yaxis=dict(title='Cantitate'), width=700, height=320)
    fig = go.Figure(data=[bar_chart], layout=layout)
    div_bar = opy.plot(fig, auto_open=False, output_type='div')
    return div_bar

# chart ul pie pentru top 5 carti vandute
def top_books_chart():
    top_books = (Sale.objects
                 .values('book__title')
                 .annotate(total_qty=Sum('qty'))
                 .order_by('-total_qty')[:5])
    book_titles = [b['book__title'] for b in top_books]
    book_qtys = [b['total_qty'] for b in top_books]

    pie_chart = go.Pie(labels=book_titles, values=book_qtys)
    layout_pie = go.Layout(width=700, height=320)
    fig_pie = go.Figure(data=[pie_chart], layout=layout_pie)
    div_pie = opy.plot(fig_pie, auto_open=False, output_type='div')
    return div_pie


@login_required
def index(request):
    # total vanzari din tabela de sales
    total_qty = Sale.objects.aggregate(total=Sum('qty'))['total'] or 0
    div_bar = monthly_sales_chart()
    div_pie = top_books_chart()

    context = {
        'total_qty': total_qty,
        'div_bar': div_bar,
        'div_pie': div_pie,
    }
    return render(request, 'index.html', context)

# pentru form ul de adaugat carti noi in tabela de carti
@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = BookForm()

    context = {
        'book_form': form,
    }
    return render(request, 'products.html', context)

# render pentru products, aici este si form ul pentru adaugat stoc nou la carti
@login_required
def products(request):
    books = Book.objects.all().order_by('title')
    form = StockForm(request.POST)
    book_form = BookForm(request.POST)

    if request.method == 'POST' and form.is_valid():
        book = form.cleaned_data['book']
        qty = form.cleaned_data['stock']
        book.stock += qty
        book.save()
        return redirect('products')

    context = {
        'books': books,
        'form': form,
        'book_form': book_form,
    }
    return render(request, 'products.html', context)

# render la vanzari, aici e si form ul pentru a adauga o vanzare noua in tabela
@login_required
def sales(request):
    sales = Sale.objects.order_by('-date')[:20]
    books = Book.objects.all()

    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.date = now()
            sale.save()
            return redirect('sales')
    else:
        form = SaleForm()

    context = {
        'sales': sales,
        'form': form,
        'books': books,
    }
    return render(request, 'sales.html', context)

# afiseaza user ii
@login_required
def users(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})

# view pentru a nu da display la sidebar in pagina de login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("dashboard")
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
        'hide_sidebar': True
    }
    return render(request, "login.html", context)

# redirect inapoi dupa logout
@login_required
def logout_view(request):
    logout(request)
    return redirect('/')