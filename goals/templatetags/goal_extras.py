import decimal
from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def sub(value, arg):
    """Subtract the arg from the value."""
    try:
        return Decimal(str(value)) - Decimal(str(arg))
    except (ValueError, TypeError, decimal.InvalidOperation):
        return value

@register.filter
def percentage(value, arg):
    """Calculate percentage of value to arg."""
    try:
        return (Decimal(str(value)) / Decimal(str(arg)) * 100) if Decimal(str(arg)) != 0 else 0
    except (ValueError, TypeError, decimal.InvalidOperation):
        return 0