import math
from django import template

register = template.Library()

@register.filter
def humanize_revenue(value):
    if value is None:
        return "N/A"
    value = int(value)
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.1f} billion"
    elif value >= 1_000_000:
        return f"${value / 1_000_000:.1f} million"
    elif value >= 1_000:
        return f"${value / 1_000:.1f} thousand"
    else:
        return f"${value:,}"
