# Generated by Django 4.0.6 on 2023-12-27 14:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog_Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog_image', models.ImageField(upload_to='blog')),
                ('blog_name', models.CharField(max_length=500)),
                ('blog_detail', models.CharField(max_length=300)),
                ('blog_date', models.DateField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Our_Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_image', models.ImageField(upload_to='product')),
                ('product_name', models.CharField(max_length=500)),
                ('product_detail', models.CharField(max_length=300)),
                ('product_price', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Top_Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_image', models.ImageField(upload_to='top')),
                ('product_name', models.CharField(max_length=500)),
                ('product_detail', models.CharField(max_length=300)),
                ('product_price', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=255)),
                ('phone_number', models.CharField(blank=True, max_length=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),

    ]
