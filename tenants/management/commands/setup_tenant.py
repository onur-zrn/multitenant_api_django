import os
import sys
from django.core.management.base import BaseCommand
from django.core.management import call_command
from tenants.models import Center, Domain

class Command(BaseCommand):
    help = 'Setup a new tenant with domain'

    def add_arguments(self, parser):
        parser.add_argument('--name', type=str, help='Center name', required=True)
        parser.add_argument('--schema', type=str, help='Schema name (optional)')
        parser.add_argument('--domain', type=str, help='Domain name (optional)')

    def handle(self, *args, **options):
        name = options['name']
        schema_name = options.get('schema') or name.lower().replace(' ', '_')
        domain_name = options.get('domain') or f"{schema_name}.localhost"

        # Create center
        center, created = Center.objects.get_or_create(
            schema_name=schema_name,
            defaults={'name': name}
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created center "{name}" with schema "{schema_name}"')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Center with schema "{schema_name}" already exists')
            )

        # Create domain
        domain, created = Domain.objects.get_or_create(
            domain=domain_name,
            defaults={'tenant': center, 'is_primary': True}
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created domain "{domain_name}"')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Domain "{domain_name}" already exists')
            )