# Generated by Django 3.1.4 on 2021-11-15 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0006_auto_20211115_2019'),
    ]

    operations = [
        migrations.RenameField(
            model_name='host',
            old_name='Marks_per_question',
            new_name='No_of_questions',
        ),
    ]
