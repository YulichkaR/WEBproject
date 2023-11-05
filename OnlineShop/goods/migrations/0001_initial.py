# Generated by Django 2.2.7 on 2019-12-02 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Good',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Short description')),
                ('content', models.TextField(verbose_name='Additional information')),
                ('price', models.FloatField(db_index=True, verbose_name='Price')),
                ('price_acc', models.FloatField(blank=True, null=True, verbose_name='Price with discount')),
                ('in_stock', models.BooleanField(db_index=True, default=True, verbose_name='In stock')),
                ('featured', models.BooleanField(db_index=True, default=False, verbose_name='Recommended')),
                ('image', models.ImageField(upload_to='goods/list', verbose_name='Main image')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.Category', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Good',
                'verbose_name_plural': 'Goods',
            },
        ),
        migrations.CreateModel(
            name='GoodImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='goods/detail', verbose_name='Additional image')),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Good', verbose_name='Good')),
            ],
            options={
                'verbose_name': 'Good image',
                'verbose_name_plural': 'Good images',
            },
        ),
    ]
