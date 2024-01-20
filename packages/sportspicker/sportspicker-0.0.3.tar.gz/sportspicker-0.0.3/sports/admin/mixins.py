# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.urls import reverse
from django.utils.html import mark_safe
from django.utils.translation import gettext as _


class ReadOnlyAdminMixin(object):
    read_write_fields = []
    explicit_readonly_fields = []

    # def get_readonly_fields(self, request, obj=None):
    #     fields = [f.name for f in self.model._meta.fields if f.name not in self.read_write_fields]
    #     return list(set(fields + list(self.explicit_readonly_fields)))
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False
    # #
    # def has_add_permission(self, request, obj=None):
    #     return False
    # #
    # def get_actions(self, request, obj=None):
    #     actions = super(ReadOnlyAdminMixin, self).get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions


class LinkedRelatedInlineMixin(object):
    """
    This InlineAdmin mixin links the first field to the row object's own admin
    change form.

    NOTE: If the first field is editable, it is undefined what will happen.
    For best results, consider making all fields readonly (since they can be
    edited with ease by following the link), and disabling the ability to add
    new objects by overriding has_add_permission() on the inline to always
    return false.
    """

    extra = 0

    class ReverseLink:

        allow_tags = True

        def __init__(self, display_link="link"):
            self.display_link = display_link
            self.short_description = display_link

        def __call__(self, obj):
            model_name = obj.__class__.__name__.lower()
            admin_link = reverse(
                "admin:{app_label}_{model_name}_change".format(
                    app_label=obj._meta.app_label.lower(),
                    model_name=model_name,
                ), args=(obj.id, ))
            return '<a href="{admin_link}" title="{title}">{link}</a>'.format(
                admin_link=admin_link,
                title=_('Click to view or edit this {0}').format(
                    obj._meta.verbose_name),
                link=getattr(obj, self.display_link))

    def __init__(self, parent_model, admin_site):
        self.original_fields = self.get_fields_list(None)
        if len(self.original_fields):
            self.fields = ["reverse_link", ] + self.original_fields[1:]
        else:
            self.fields = ["reverse_link"]
        self.reverse_link = self.ReverseLink(self.original_fields[0])
        super(LinkedRelatedInlineMixin, self).__init__(parent_model, admin_site)

    def get_fields_list(self, request, obj=None):
        """
        Returns a list of the AdminModel's declared `fields`, or, constructs it
        from the object, then, removes any `exclude`d items.
        """
        if self.fields:
            fields = self.fields
        else:
            fields = [f.name for f in self.model._meta.local_fields]
        if fields and self.exclude:
            fields = [f for f in fields if f not in self.exclude]
        if fields:
            return list(fields)
        else:
            return []

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(
            LinkedRelatedInlineMixin, self).get_readonly_fields(request, obj)
        if "reverse_link" not in readonly_fields:
            readonly_fields = list(readonly_fields) + ["reverse_link", ]
        # We want all fields to be readonly for this inline
        return readonly_fields


class LinkedFieldsMixin(object):
    """
    This mixin will link fields to their respective change-form. This should
    only be used on a ModelAdmin. For similar functionality for Inlines see:
    LinkedRelatedInlineMixin.

    if linked_fields is None, then all FK or O2O fields are used.

    To use, merely add the class property `linked_fields` with a list of FK fields.
    """
    linked_fields = None
    prefix = 'linked_'

    @classmethod
    def add_new_method(cls, model, field):
        """
        Creates a new method on the AdminModel class that returns the field as
        a link to its change form.

        :return: The name of the new method
        """
        method_name = '{0}{1}'.format(cls.prefix, field)
        fld_model = model._meta.get_field(field).remote_field.model.__name__.lower().replace('_', '')
        app_label = model._meta.get_field(field).remote_field.model._meta.app_label

        def new_method(self, obj):
            pattern = 'admin:{0}_{1}_change'.format(app_label, fld_model)
            url = reverse(pattern, args=(getattr(obj, field).pk, ))
            return mark_safe('{value} &nbsp;<a href="{url}" class="inlinechangelink"></a>'.format(url=url, value=getattr(obj, field)))
        new_method.short_description = field

        setattr(cls, method_name, new_method)
        return method_name

    def __init__(self, model, admin_site):
        super(LinkedFieldsMixin, self).__init__(model, admin_site)
        if self.linked_fields is None:
            self.linked_fields = [
                f.name for f in model._meta.get_fields()
                if (f.one_to_one or f.many_to_one) and f.related_model
            ]
        for field in self.linked_fields:
            self.add_new_method(model, field)

    def get_readonly_fields(self, request, obj=None):
        """
        Ensures that the new linked_fields are in readonly_fields.
        """
        readonly_fields = super(LinkedFieldsMixin, self).get_readonly_fields(request, obj=obj) or []
        readonly_fields = list(readonly_fields)
        return readonly_fields + [self.prefix + fld for fld in self.linked_fields]

    @classmethod
    def mapped(cls, mapping, field):
        if not isinstance(field, str) and hasattr(field, '__iter__'):
            # Recurse!
            return [cls.mapped(mapping, fld) for fld in field]
        else:
            if field in mapping:
                return mapping[field]
            else:
                return field

    def get_fieldsets(self, request, obj=None):
        """
        Replaces any occurrence of a field in linked_fields with its
        method counterpart.
        """
        mapping = {fld: self.prefix + fld for fld in self.linked_fields}

        fieldsets = []
        for fieldset in super(LinkedFieldsMixin, self).get_fieldsets(request, obj=obj):
            fields = fieldset[1]['fields']
            fieldset[1]['fields'] = [self.mapped(mapping, f) for f in fields]
            fieldsets.append(fieldset)
        return fieldsets

    @staticmethod
    def uniq(seq):
        """
        Removes duplicates from list whilst preserving order.
        """
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

    def get_fields(self, request, obj=None):
        """
        Replaces any occurrence of a field in linked_fields with its
        method counterpart.
        """
        # TODO: Figure out why we have to de-dupe the list!
        fields = super(LinkedFieldsMixin, self).get_fields(request, obj=obj)
        mapping = {fld: self.prefix + fld for fld in self.linked_fields}
        return self.uniq(self.mapped(mapping, fields))
