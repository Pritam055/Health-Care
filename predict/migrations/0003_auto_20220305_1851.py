# Generated by Django 3.2.4 on 2022-03-05 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0002_historymodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historymodel',
            old_name='predicted_disease',
            new_name='max_prob_disease',
        ),
        migrations.AddField(
            model_name='historymodel',
            name='percentage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=2),
            preserve_default=False,
        ),
    ]
