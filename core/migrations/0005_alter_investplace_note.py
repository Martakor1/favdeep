# Generated by Django 5.0.6 on 2024-06-13 17:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_alter_investplace_owner_inn"),
    ]

    operations = [
        migrations.AlterField(
            model_name="investplace",
            name="note",
            field=models.TextField(null=True),
        ),
    ]
