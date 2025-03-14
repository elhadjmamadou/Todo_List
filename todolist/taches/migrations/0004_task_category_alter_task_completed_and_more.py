# Generated by Django 5.1 on 2024-09-04 19:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_task"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="category",
            field=models.CharField(
                choices=[
                    ("Personnel", "Personnel"),
                    ("Travail", "Travail"),
                    ("Autre", "Autre"),
                ],
                default="Autre",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="completed",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="task",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="due_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="priority",
            field=models.CharField(
                choices=[
                    ("Haute", "Haute"),
                    ("Moyenne", "Moyenne"),
                    ("Basse", "Basse"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="title",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="task",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
