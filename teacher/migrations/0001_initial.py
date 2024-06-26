# Generated by Django 5.0.4 on 2024-04-14 09:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paper_code', models.CharField(max_length=200)),
                ('std', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('admin_code', models.CharField(default='EXAM-Controller', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200)),
                ('answer', models.CharField(max_length=2000)),
                ('std', models.CharField(max_length=200)),
                ('question_num', models.PositiveIntegerField()),
                ('paper_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.paper')),
            ],
        ),
    ]
