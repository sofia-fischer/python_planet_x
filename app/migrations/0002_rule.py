# Generated by Django 5.1.2 on 2024-11-02 11:44

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(max_length=50)),
                ('origin', models.CharField(max_length=50)),
                ('icon', models.PositiveSmallIntegerField(choices=[(1, 'ASTEROID'), (2, 'MOON'), (4, 'NEBULA'), (8, 'DWARF_PLANET'), (16, 'PLANET_X'), (32, 'EMPTY_SPACE')])),
                ('other_icon', models.PositiveSmallIntegerField(choices=[(1, 'ASTEROID'), (2, 'MOON'), (4, 'NEBULA'), (8, 'DWARF_PLANET'), (16, 'PLANET_X'), (32, 'EMPTY_SPACE')], null=True)),
                ('sector', models.PositiveSmallIntegerField(null=True)),
                ('start', models.PositiveSmallIntegerField(null=True)),
                ('end', models.PositiveSmallIntegerField(null=True)),
                ('count', models.PositiveSmallIntegerField(null=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.game')),
            ],
        ),
    ]
