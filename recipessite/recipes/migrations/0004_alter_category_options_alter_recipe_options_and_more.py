# Generated by Django 5.0.3 on 2024-03-25 06:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_recipe_author_alter_recipe_changed_at_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-id'], 'verbose_name': 'категория', 'verbose_name_plural': 'категории'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-changed_at'], 'verbose_name': 'рецепт', 'verbose_name_plural': 'рецепты'},
        ),
        migrations.AlterModelOptions(
            name='recipecategory',
            options={'ordering': ['-id'], 'verbose_name': 'связь рецепта и категории', 'verbose_name_plural': 'связи рецепта и категории'},
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(max_length=1000, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=255, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='recipecategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='recipecategory',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='Рецепт'),
        ),
    ]
