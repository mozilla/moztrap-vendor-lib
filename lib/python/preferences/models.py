from django.db import models
from django.dispatch import receiver

import preferences
from preferences.managers import SingletonManager


class Preferences(models.Model):
    singleton = SingletonManager()

    class Meta:
        abstract = True

    def __unicode__(self):
        return self._meta.verbose_name_plural.capitalize()



@receiver(models.signals.class_prepared)
def preferences_class_prepared(sender, *args, **kwargs):
    """
    Adds various preferences members to preferences.preferences,
    thus enabling easy access from code.
    """
    cls = sender
    if issubclass(cls, Preferences):
        # Add singleton manager to subclasses.
        cls.add_to_class('singleton', SingletonManager())
        # Add property for preferences object to preferences.preferences.
        setattr(preferences.Preferences, cls._meta.object_name,
                property(lambda x: cls.singleton.get()))
