# Generated by Django 4.0.2 on 2022-03-01 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('approvals', '0008_alter_approval_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approval',
            name='slug',
            field=models.SlugField(blank=True, default='7tfzdvgndohjscvf0vjn', null=True, verbose_name='Approval Slug'),
        ),
        migrations.AlterField(
            model_name='approvalimage',
            name='approval',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approval_images', to='approvals.approval', verbose_name='Approval'),
        ),
    ]
