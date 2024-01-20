# Generated by Django 4.2 on 2023-12-08 15:27

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('zippy_form', '0011_remove_form_created_by_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentGatewayWebhook',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('payment_gateway', models.CharField(max_length=255)),
                ('payment_mode', models.CharField(max_length=255)),
                ('webhook_reference_id', models.CharField(max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='formfield',
            name='slug',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='formpaymentsettings',
            name='stripe_tax_rate_id',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='formpaymentsettings',
            name='tax_display_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='formpaymentsettings',
            name='tax_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='form',
            name='primary_payment_mode',
            field=models.CharField(default='test', max_length=255),
        ),
        migrations.AlterField(
            model_name='formpaymentsettings',
            name='payment_mode',
            field=models.CharField(default='test', max_length=255),
        ),
        migrations.CreateModel(
            name='WebhookForm',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('event_new_form_created', models.BooleanField(default=False)),
                ('event_form_submit', models.BooleanField(default=False)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zippy_form.form')),
                ('webhook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='webhook_form', to='zippy_form.webhook')),
            ],
        ),
    ]
