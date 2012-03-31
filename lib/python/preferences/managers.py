from django.db import models



class SingletonManager(models.Manager):
    """
    Returns only a single preferences object per site.
    """
    def get_query_set(self):
        """
        Return the first preferences object.
        If preferences do not exist create it.
        """
        queryset = super(SingletonManager, self).get_query_set()

        if not queryset.exists():
            # Create object if it doesn't exist.
            self.model._base_manager.create()

        return queryset
