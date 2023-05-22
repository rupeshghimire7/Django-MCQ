# Generated by Django 4.1.5 on 2023-05-22 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_question_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='level',
            field=models.CharField(blank=True, choices=[('M', 'Medium'), ('H', 'Hard'), ('E', 'Easy')], default='E', max_length=1),
        ),
    ]
