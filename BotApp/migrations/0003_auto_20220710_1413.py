# Generated by Django 3.2 on 2022-07-10 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BotApp', '0002_auto_20220708_2152'),
    ]

    operations = [
        migrations.CreateModel(
            name='login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('REDDIT_USERNAME', models.CharField(max_length=115)),
                ('REDDIT_PASSWORD', models.CharField(max_length=300)),
            ],
        ),
        migrations.AlterField(
            model_name='spec',
            name='REDDIT_PASSWORD',
            field=models.CharField(max_length=300),
        ),
    ]
