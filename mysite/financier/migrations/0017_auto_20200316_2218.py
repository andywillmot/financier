# Generated by Django 3.0.4 on 2020-03-16 22:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financier', '0016_auto_20200316_2217'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='transaction',
            unique_together={('account', 'date', 'title', 'ttype', 'value', 'count')},
        ),
    ]