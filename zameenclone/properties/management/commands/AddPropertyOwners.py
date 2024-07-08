from django.core.management.base import BaseCommand
from users.models import User
from properties.models import Property

class Command(BaseCommand):
    help = "Add users foreign key to existing records"
        
    def handle(self, *args, **kwargs):
        users = User.objects.all()
        if not users:
            self.stdout.write(self.style.ERROR("No users found"))
            return
        
        properties = Property.objects.all()
        if not properties:
            self.stdout.write(self.style.ERROR("No properties found"))
            return
        
        num_users = len(users)
        num_properties = len(properties)
        
        properties_per_user = num_properties // num_users
        
        start_index = 0
        for i, user in enumerate(users):
            if i == num_users - 1:
                end_index = num_properties
            else:
                end_index = start_index + properties_per_user
                
            user_properties = properties[start_index:end_index]
            self.set_properties_owner(user, user_properties)
            start_index = end_index
    
    def set_properties_owner(self, user, properties):
        for property in properties:
            property.owner = user
            property.save()
            self.stdout.write(self.style.SUCCESS(f"Assigned {user.username} as owner of property {property.id}"))

