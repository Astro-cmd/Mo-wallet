from django import template
from decimal import Decimal
import math

register = template.Library()

@register.filter
def abs(value):
    """Return the absolute value."""
    try:
        # Handle Decimal objects directly
        if isinstance(value, Decimal):
            return value.copy_abs()
        # Handle floats and integers
        if isinstance(value, (float, int)):
            return math.fabs(value)
        # Try to convert string to float
        if isinstance(value, str):
            return math.fabs(float(value))
        return value
    except (TypeError, ValueError):
        return value