from django.db import models
import json

class Role(models.Model):
    name = models.CharField(max_length=255)  # Stores the name of the role
    description = models.TextField()  # Role description
    permissions = models.JSONField(default=dict)  # Store permissions as a JSON string

    def __str__(self):
        return self.name

    # Method to set permissions as a JSON string
    def set_permissions(self, permissions_dict):
        self.permissions = json.dumps(permissions_dict)

    # Method to get permissions as a dictionary
    def get_permissions(self):
        return json.loads(self.permissions)
