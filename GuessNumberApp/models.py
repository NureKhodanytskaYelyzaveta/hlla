from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")
    description = models.TextField(blank=True, verbose_name="Опис")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('debit', 'Дебет'),
        ('credit', 'Кредит'),
    ]
    
    description = models.CharField(max_length=200, verbose_name="Опис")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сума")
    transaction_type = models.CharField(
        max_length=10, 
        choices=TRANSACTION_TYPES, 
        verbose_name="Тип"
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Категорія"
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата створення")

    def __str__(self):
        return f"{self.description} - {self.amount}"
    
    class Meta:
        verbose_name = "Транзакція"
        verbose_name_plural = "Транзакції"
        ordering = ['-created_at']