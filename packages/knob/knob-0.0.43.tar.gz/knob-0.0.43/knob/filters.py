__all__ = ['InputFilter']

from django.contrib import admin


class InputFilter(admin.FieldListFilter):
    template = 'knob/input_filter.html'

    def expected_parameters(self):
        return [self.lookup_kwarg]