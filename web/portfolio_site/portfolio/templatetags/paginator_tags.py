"""This module is a custom tag to pagenate.
"""
from django import template
from django.core.paginator import Paginator

register = template.Library()

@register.simple_tag
def get_proper_elided_page_range(paginator:Paginator, num:int, on_each_side:int=3, on_ends:int=2):
    """This calls Paginator.get_elided_page_range of the Django method.

    Args:
        paginator (Paginator): Paginator object.
        num (int): Page number on a current page.
        on_each_side (int, optional): number of pages to show on each side. Defaults to 3.
        on_ends (int, optional): number of pages to show on ends. Defaults to 2.

    Returns:
        Iterator[str | int]: Return a 1-based range of pages with some values elided.
    """
    paginator = Paginator(paginator.object_list, paginator.per_page)
    return paginator.get_elided_page_range(number=num, on_each_side=on_each_side, on_ends=on_ends)
