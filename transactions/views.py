from django.shortcuts import render, get_object_or_404
from .models import Transaction, Category
from django.db.models import Sum, Q, Count

def index(request):
    search = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    sort_by = request.GET.get('sort', '-created_at')
    transaction_type = request.GET.get('type', '')
    
    transactions = Transaction.objects.all()
    
    if search:
        transactions = transactions.filter(description__icontains=search)
    if category_id:
        transactions = transactions.filter(category_id=category_id)
    if transaction_type:
        transactions = transactions.filter(transaction_type=transaction_type)
    
    transactions = transactions.order_by(sort_by)
    categories = Category.objects.all()
    
    return render(request, 'transactions/index.html', {
        'transactions': transactions,
        'categories': categories,
        'search': search,
        'category_id': category_id,
        'sort_by': sort_by,
        'transaction_type': transaction_type
    })

def categories(request):
    categories = Category.objects.annotate(
        transaction_count=Count('transaction'),
        total_amount=Sum('transaction__amount')
    )
    return render(request, 'transactions/categories.html', {'categories': categories})

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    transactions = Transaction.objects.filter(category=category)
    return render(request, 'transactions/category_detail.html', {
        'category': category,
        'transactions': transactions
    })

def budget(request):
    income = Transaction.objects.filter(transaction_type='credit').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    expenses = Transaction.objects.filter(transaction_type='debit').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    balance = income - expenses
    
    categories = Category.objects.annotate(
        expense_sum=Sum('transaction__amount', filter=Q(transaction__transaction_type='debit')),
        income_sum=Sum('transaction__amount', filter=Q(transaction__transaction_type='credit'))
    )
    
    return render(request, 'transactions/budget.html', {
        'income': income,
        'expenses': expenses,
        'balance': balance,
        'categories': categories
    })