# Generated by Django 5.2.1 on 2025-06-25 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_rename_authon_recipe_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='servings_time',
            new_name='servings',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='servings_time_unit',
            new_name='servings_unit',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cover',
            field=models.ImageField(blank=True, default='', upload_to='recipes/covers/%Y/%m/%d/'),
        ),
    ]
