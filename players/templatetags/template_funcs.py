from django.template import Library
import copy

register = Library()

@register.filter
def adjust_left(lineup,location):
	first=int(location)-1
	second=int(location)
	tmp = copy.deepcopy(lineup)
	lineup[first] = tmp[second]
	lineup[second] = tmp[first]

@register.filter
def num_range(value):
	return range(int(value))

@register.filter
def get_num(value):
	return int(value)

@register.filter
def getArrayElement(value,id):
	return value[int(id)]

@register.filter
def count(value):
	return len(value)


@register.filter
def splitGame(value):
	return str(value).split("], [")
