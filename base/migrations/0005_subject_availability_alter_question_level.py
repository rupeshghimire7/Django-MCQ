# Generated by Django 4.1.5 on 2023-05-20 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_user_attempted_alter_question_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='availability',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='question',
            name='level',
            field=models.CharField(blank=True, choices=[('M', 'Medium'), ('E', 'Easy'), ('H', 'Hard')], default='E', max_length=1),
        ),
    ]