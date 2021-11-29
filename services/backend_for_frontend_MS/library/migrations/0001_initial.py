# Generated by Django 3.2.5 on 2021-07-30 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100, verbose_name='name')),
                ('date_birth', models.DateField(verbose_name='date_birth')),
            ],
            options={
                'verbose_name': 'author',
                'verbose_name_plural': 'authors',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('publication_date', models.DateField(verbose_name='publication_date')),
                ('language', models.CharField(choices=[('es', 'Spanish'), ('en', 'English'), ('fr', 'French')], max_length=2, verbose_name='language')),
                ('cathegory', models.CharField(choices=[('romantic', 'Romantic'), ('terror', 'Terror'), ('adventure', 'Adventure'), ('science_fiction', 'Science fiction')], max_length=15, verbose_name='cathegory')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='library.author')),
            ],
            options={
                'verbose_name': 'book',
                'verbose_name_plural': 'books',
            },
        ),
    ]