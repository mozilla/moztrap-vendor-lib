from django import template
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template import RequestContext, Template
from django.test import TestCase
from django.test.client import RequestFactory

from preferences import context_processors, preferences
from preferences.admin import PreferencesAdmin
from preferences.tests.models import MyPreferences


class AdminTestCase(TestCase):
    def test_changelist_view(self):
        request = RequestFactory().get('/')
        request.user = User.objects.create(username='name', password='pass',\
                is_superuser=True)
        admin_obj = PreferencesAdmin(MyPreferences, admin.site)

        # With only one preferences object redirect to its change view.
        response = admin_obj.changelist_view(request)
        self.failUnlessEqual(
            response.items()[1][1],
            '/admin/preferences/mypreferences/1/',
            'Should redirect to change view if only one \
preferences object available'
        )

        # With multiple preferences display listing view.
        MyPreferences.singleton.create()
        response = admin_obj.changelist_view(request)
        self.failUnless('changelist-form' in response.content, 'Should \
display listing if multiple preferences objects are available.')



class ContextProcessorsTestCase(TestCase):
    def test_preferences_cp(self):
        request = RequestFactory().get('/')
        context = context_processors.preferences_cp(request)

        # context should have preferences.
        preferences = context['preferences']

        # preferences should have test MyPreferences object member.
        my_preferences = preferences.MyPreferences
        self.failUnless(isinstance(my_preferences, MyPreferences), \
                "%s should be instance of MyPreferences." % my_preferences)

        # With preferences_cp is loaded as a TEMPLATE_CONTEXT_PROCESSORS
        # templates should have access to preferences object.
        context_instance = RequestContext(request)
        context = template.Context({
            'request': RequestFactory,
        })
        t = Template("{% if preferences %}{{ preferences }}{% endif %}")
        self.failUnless(t.render(context_instance), "preferences should be \
available in template context.")

        t = Template("{% if preferences.MyPreferences %}{{ \
preferences.MyPreferences }}{% endif %}")
        self.failUnless(t.render(context_instance), "MyPreferences should be \
available as part of preferences var in template context.")



class ModelsTestCase(TestCase):
    def test_preferences_class_prepared(self):
        """
        Regardless of what happens in the background, after startup and model
        preperation the preferences.preferences object should have members for
        each of the various preferences models. When accessing the member the
        appropriate object for the current site should be returned (or
        unassociated with a site if not using sites).
        """

        # Should have MyPreferences member without
        # sites since we are not using sites.
        my_preferences = preferences.MyPreferences



class SingeltonManagerTestCase(TestCase):
    def test_get_query_set(self):
        # Should return preferences.
        # Shouldn't fail on duplicates.
        MyPreferences.singleton.get()
