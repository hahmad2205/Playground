from django.core.management.base import BaseCommand

from users.models import User
from properties.models import Property

from faker import Faker
fake = Faker()

class Command(BaseCommand):
    help = "Add users foreign key to existing records"
        
    def handle(self, *args, **kwargs):
        self.generate_fake_users()
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
    
    def generate_fake_users(self):
        for _ in range(9):
            first_name = fake.first_name()
            User.objects.create(
                username=f"{first_name}123",
                first_name=first_name,
                last_name=fake.last_name(),
                email=fake.email(),
                password="cogent123"
            )
        
    def set_properties_owner(self, user, properties):
        for property in properties:
            property.owner = user
            property.save()
            self.stdout.write(self.style.SUCCESS(f"Assigned {user.username} as owner of property {property.id}"))
