# Generated by Django 5.0.6 on 2024-06-13 16:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="investplace",
            name="municipality",
            field=models.CharField(default="", max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="investplace",
            name="sewage_cost",
            field=models.CharField(null=True),
        ),
        migrations.AlterField(
            model_name="investplace",
            name="sewage_cost_transportation",
            field=models.CharField(null=True),
        ),
        migrations.AlterField(
            model_name="investplace",
            name="water_cost",
            field=models.CharField(null=True),
        ),
        migrations.AlterField(
            model_name="investplace",
            name="water_cost_transportation",
            field=models.CharField(null=True),
        ),
    ]