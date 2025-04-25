import decimal
from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def div(value, arg):
    """Divide the value by the argument."""
    try:
        return Decimal(str(value)) / Decimal(str(arg))
    except (ValueError, TypeError, decimal.InvalidOperation, ZeroDivisionError):
        return 0

@register.filter
def mul(value, arg):
    """Multiply the value by the argument."""
    try:
        return Decimal(str(value)) * Decimal(str(arg))
    except (ValueError, TypeError, decimal.InvalidOperation):
        return 0