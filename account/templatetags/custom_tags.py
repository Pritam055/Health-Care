from django import template

register = template.Library()

@register.filter(name = "addclass")
def addclass(tag_name, class_name):
    tag_name.field.widget.attrs["class"] = class_name 
    return tag_name 