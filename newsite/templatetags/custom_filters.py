from django import template

register = template.Library()


@register.filter
def add_class(value, css_class):
    value.field.widget.attrs["class"] = css_class
    return value


def add_id(value, css_id):
    value.field.widget.attrs["id"] = css_id
    return value
