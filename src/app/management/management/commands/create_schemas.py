from django.core.management.base import BaseCommand
from django.db import ProgrammingError, connection


class Command(BaseCommand):
    help = "Create schemas"

    def handle(self, *args, **options):
        schema_names = [
            "gallery",
            "adminuses"
        ]
        self.stdout.write(
            self.style.SUCCESS(
                f"Attempting to create schema {', '.join(schema_names)} in db"
            )
        )
        with connection.cursor() as cursor:
            for schema_name in schema_names:
                try:
                    cursor.execute(f'CREATE SCHEMA "{schema_name}"')
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Schema "{schema_name}" created successfully'
                        )
                    )
                except ProgrammingError:
                    self.stdout.write(
                        self.style.WARNING(f'Schema "{schema_name}" already exists')
                    )