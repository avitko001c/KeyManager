from __future__ import unicode_literals

from django import forms
import account.forms
from django.conf import settings
from django.utils.translation import get_language_bidi

__all__ = ['ChosenWidgetMixin', 'ChosenSelect', 'ChosenSelectMultiple',
	'ChosenGroupSelect', 'DateWidget', 'TimeWidget', 'SplitDateTime',
	'ArrayFieldSelectMultiple']

class ChosenWidgetMixin(object):

	class Media:
		js = ("%s%s" % (settings.STATIC_URL, "js/jquery.min.js"),
		      "%s%s?v=2" % (settings.STATIC_URL, "chosen/js/chosen.jquery.min.js"),
		      "%s%s?v=4" % (settings.STATIC_URL, "chosen/js/chosen.jquery_ready.js"))
		css = {"all": ("%s%s?v=1" % (settings.STATIC_URL, "chosen/css/chosen.css"), )}

	def __init__(self, attrs={}, *args, **kwargs):

		attrs['data-placeholder'] = kwargs.pop('overlay', None)
		attrs['class'] = "class" in attrs and self.add_to_css_class(
		attrs['class'], 'chosen-select') or "chosen-select"
		if get_language_bidi():
			attrs['class'] = self.add_to_css_class(attrs['class'], 'chosen-rtl')
		super(ChosenWidgetMixin, self).__init__(attrs, *args, **kwargs)

	def render(self, *args, **kwargs):
		if not self.is_required:
			self.attrs.update({'data-optional': True})
		return super(ChosenWidgetMixin, self).render(*args, **kwargs)

	def add_to_css_class(self, classes, new_class):
		new_classes = classes
		try:
			classes_test = u" " + unicode(classes) + u" "
			new_class_test = u" " + unicode(new_class) + u" "
			if new_class_test not in classes_test:
				new_classes += u" " + unicode(new_class)
		except TypeError:
			pass
		return new_classes


class ChosenSelect(ChosenWidgetMixin, forms.Select):
	pass


class ChosenSelectMultiple(ChosenWidgetMixin, forms.SelectMultiple):
	pass


class ChosenGroupSelect(ChosenSelect):

	def __init__(self, attrs={}, *args, **kwargs):
		super(ChosenGroupSelect, self).__init__(attrs, *args, **kwargs)
		attrs["class"] = "chosen-single chosen-with-drop"

class ArrayFieldSelectMultiple(forms.SelectMultiple):
	"""This is a Form Widget for use with a Postgres ArrayField. It implements
	a multi-select interface that can be given a set of `choices`.

	You can provide a `delimiter` keyword argument to specify the delimeter used.

	"""

	def __init__(self, *args, **kwargs):
		# Accept a `delimiter` argument, and grab it (defaulting to a comma)
		self.delimiter = kwargs.pop("delimiter", ",")
		super(ArrayFieldSelectMultiple, self).__init__(*args, **kwargs)

	def format_value(self, value):
		"""Return selected values as a list."""
		if isinstance(value, str):
			value = value.split(self.delimiter)
		return super(ArrayFieldSelectMultiple, self).format_value(value)

	def render_options(self, choices, value):
		# value *should* be a list, but it might be a delimited string.
		if isinstance(value, str):  # python 2 users may need to use basestring instead of str
			value = value.split(self.delimiter)
		return super(ArrayFieldSelectMultiple, self).render_options(choices, value)

	def value_from_datadict(self, data, files, name):
		if isinstance(data, MultiValueDict):
			# Normally, we'd want a list here, which is what we get from the
			# SelectMultiple superclass, but the SimpleArrayField expects to
			# get a delimited string, so we're doing a little extra work.
			return self.delimiter.join(data.getlist(name))
		return data.get(name, None)

class DateWidget(forms.DateInput):
	@property
	def media(self):
		js = ["/jsi18n/", "js/jquery.min.js", "admin/js/jquery.init.js", "admin/js/actions.js",
			"admin/js/core.js", "admin/js/admin/RelatedObjectLookups.js", "admin/js/calendar.js", 
			"admin/js/admin/DateTimeShortcuts.js"]
		return forms.Media(js=js)

	def __init__(self, attrs=None, format=None):
		final_attrs = {'class': 'vDateField', 'size': '10'}
		if attrs is not None:
			final_attrs.update(attrs)
		super(DateWidget, self).__init__(attrs=final_attrs, format=format)


class TimeWidget(forms.TimeInput):
	@property
	def media(self):
		js = ["calendar.js", "admin/DateTimeShortcuts.js"]
		return forms.Media(js=["admin/js/%s" % path for path in js])

	def __init__(self, attrs=None, format=None):
		final_attrs = {'class': 'vTimeField', 'size': '8'}
		if attrs is not None:
			final_attrs.update(attrs)
		super(TimeWidget, self).__init__(attrs=final_attrs, format=format)

class SplitDateTime(forms.SplitDateTimeWidget):
	"""
	A SplitDateTime Widget that has some admin-specific styling.
	"""
	template_name = 'widgets/split_datetime.html'

	def __init__(self, attrs=None):
		widgets = [DateWidget, TimeWidget]
		# Note that we're calling MultiWidget, not SplitDateTimeWidget, because
		# we want to define widgets.
		forms.MultiWidget.__init__(self, widgets, attrs)

	def get_context(self, name, value, attrs):
		context = super(SplitDateTime, self).get_context(name, value, attrs)
		context['date_label'] = _('Date:')
		context['time_label'] = _('Time:')
		return context
