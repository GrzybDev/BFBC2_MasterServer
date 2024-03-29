# Generated by Django 4.1.3 on 2022-12-02 17:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Plasma", "0004_persona"),
    ]

    operations = [
        migrations.CreateModel(
            name="Assocation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.IntegerField(
                        choices=[
                            (0, "Unknown"),
                            (1, "Mute"),
                            (2, "Block"),
                            (3, "Friends"),
                            (4, "Recent Players"),
                            (5, "Dogtags"),
                        ],
                        default=0,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Association",
                "verbose_name_plural": "Associations",
                "ordering": ("id",),
            },
        ),
        migrations.CreateModel(
            name="AssociationMember",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "persona",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="Plasma.persona"
                    ),
                ),
                (
                    "target",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Plasma.assocation",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="assocation",
            name="members",
            field=models.ManyToManyField(
                related_name="association_members",
                through="Plasma.AssociationMember",
                to="Plasma.persona",
            ),
        ),
        migrations.AddField(
            model_name="assocation",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="Plasma.persona"
            ),
        ),
    ]
