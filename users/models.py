import json

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    search_methods = models.TextField(blank=True, null=True)

    def add_search_method(self, method_name):
        if self.search_methods is None or self.search_methods == '':
            search_methods = [method_name]
            self.search_methods = json.dumps(search_methods)
        else:
            search_methods = json.loads(str(self.search_methods))
            search_methods.append(method_name)
            self.search_methods = json.dumps(search_methods)
        self.save()

    def get_search_methods(self):
        if self.search_methods is None or self.search_methods == '':
            return []
        else:
            return json.loads(str(self.search_methods))

    def __str__(self):
        return self.username
