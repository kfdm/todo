# Generated by Django 3.0.6 on 2020-05-18 11:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('color', models.CharField(max_length=7)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('summary', models.CharField(max_length=128)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(max_length=128)),
                ('calendar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todo.Calendar')),
            ],
        ),
    ]
