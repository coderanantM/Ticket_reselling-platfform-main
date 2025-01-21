# Generated by Django 5.0.6 on 2025-01-15 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0005_adminsettings_sellerprofile_whatsapp_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('sold', 'Sold'), ('unsold', 'Unsold')], default=1, max_length=10),
            preserve_default=False,
        ),
    ]
