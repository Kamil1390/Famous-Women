# Generated by Django 5.0.3 on 2024-04-11 21:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("women", "0008_tagpost_step"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tagpost",
            name="step",
        ),
    ]