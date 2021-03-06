# Generated by Django 3.0.5 on 2020-09-23 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=1000, verbose_name='Descriptions')),
                ('path', models.ImageField(default='images/default.png', upload_to='images/', verbose_name='Image')),
                ('name', models.CharField(max_length=200, verbose_name='Title')),
                ('main', models.BooleanField(default=False, verbose_name='Main?')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Publication date')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_set', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
