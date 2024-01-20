# Generated by Django 4.2.1 on 2023-12-08 18:14

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stela_control', '0006_facebookpageevent_lang_facebookpageevent_location_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='user',
        ),
        migrations.AddField(
            model_name='booking',
            name='address',
            field=models.CharField(default='no address', max_length=250, verbose_name='billing_address'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='email',
            field=models.EmailField(default='no email', max_length=254, verbose_name='email'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='name',
            field=models.CharField(default='no name', max_length=250, verbose_name='name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='service',
            field=models.CharField(default='no service', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='type',
            field=models.CharField(default='none', max_length=250),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='billingrecipt',
            name='option',
            field=models.CharField(choices=[('Monthly charge', 'Monthly charge'), ('budget_marketing', 'Budget Marketing'), ('Billing receipt', 'Billing receipt'), ('budget_design', 'Budget Design'), ('Others', 'Others'), ('budget_development', 'Budget Development')], max_length=60, null=True, verbose_name='Case'),
        ),
        migrations.AlterField(
            model_name='company',
            name='business',
            field=models.CharField(blank=True, choices=[('IT Development Services', 'IT Development Services'), ('Repair and Maintenance Services', 'Repair and Maintenance Services'), ('Health and Wellness', 'Health and Wellness'), ('Media Creators', 'Media Creators'), ('Education and Training', 'Education and Training'), ('E-commerce', 'E-commerce'), ('Beauty and Personal Care Services', 'Beauty and Personal Care Services'), ('Consulting', 'Consulting'), ('Marketing and Advertising Services', 'Marketing and Advertising Services'), ('Logistics and Transportation Services', 'Logistics and Transportation Services'), ('Restaurants and Food Services', 'Restaurants and Food Services')], max_length=100, null=True, verbose_name='Business Type'),
        ),
        migrations.AlterField(
            model_name='content',
            name='card',
            field=models.CharField(blank=True, choices=[('card-light-danger', 'card-light-danger'), ('card-tale', 'card-tale'), ('card-light-blue', 'card-light-blue'), ('card-dark-blue', 'card-dark-blue')], max_length=50, null=True, verbose_name='Color Card'),
        ),
        migrations.AlterField(
            model_name='content',
            name='category',
            field=models.CharField(blank=True, choices=[('Inspiration', 'Inspiration'), ('Tutorials', 'Tutorials'), ('Events and Conferences', 'Events and Conferences'), ('Interviews', 'Interviews'), ('News', 'News'), ('Tips and Tricks', 'Tips and Tricks'), ('Guides and Manuals', 'Guides and Manuals')], default='News', max_length=100),
        ),
        migrations.AlterField(
            model_name='facebookpagecomments',
            name='update_rate',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 8, 15, 12, 37, 913144)),
        ),
        migrations.AlterField(
            model_name='itemdiscount',
            name='field',
            field=models.CharField(choices=[('Promotional Discount', 'Promotional Discount'), ('Initial Payment', 'Initial Payment'), ('No Selected', 'No Selected'), ('Stela Payment Free Suscription', 'Stela Payment Free Suscription')], max_length=60),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='status',
            field=models.CharField(choices=[('Draft', 'Draft'), ('Send', 'Send')], max_length=20),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='template',
            field=models.CharField(choices=[('Style Template 4', 'Style Template 4'), ('Style Template 1', 'Style Template 1'), ('Style Template 3', 'Style Template 3'), ('Style Template 2', 'Style Template 2')], max_length=60, null=True, verbose_name='Style'),
        ),
        migrations.AlterField(
            model_name='order',
            name='section',
            field=models.CharField(choices=[('Stela Websites', 'Stela Websites'), ('Stela Marketing', 'Stela Marketing'), ('Cloud Domains', 'Cloud Domains'), ('Stela Design', 'Stela Design'), ('Store', 'Store'), ('Cloud Elastic Instance', 'Cloud Elastic Instance'), ('No Selected', 'No Selected')], default='No Selected', max_length=50),
        ),
        migrations.AlterField(
            model_name='pathcontrol',
            name='step',
            field=models.CharField(choices=[('Step 3', 'Step 3'), ('Step 4', 'Step 4'), ('Step 2', 'Step 2')], default='No Selected', max_length=50),
        ),
        migrations.AlterField(
            model_name='sitepolicy',
            name='section',
            field=models.CharField(blank=True, choices=[('Cookie Policy', 'Cookie Policy'), ('billing_terms', 'Monthly Billing Terms'), ('Terms and Conditions', 'Terms and Conditions'), ('budget_design_terms', 'Budget Design Terms'), ('Disclaimer', 'Disclaimer'), ('budget_marketing_terms', 'Budget Marketing Terms'), ('Return Policy', 'Return Policy'), ('Privacy Policy', 'Privacy Policy'), ('budget_development_terms', 'Budget Development Terms'), ('monthly_terms', 'Billing Terms')], default='Terms and Conditions', max_length=150),
        ),
        migrations.AlterField(
            model_name='sociallinks',
            name='social',
            field=models.CharField(choices=[('Tiktok', 'Tiktok'), ('Youtube', 'Youtube'), ('X', 'X'), ('Facebook', 'Facebook'), ('Instagram', 'Instagram'), ('Linkedin', 'Linkedin'), ('Github', 'Github')], default='No Selected', max_length=50),
        ),
        migrations.AlterField(
            model_name='support',
            name='option',
            field=models.CharField(choices=[('My account has an error', 'My account has an error'), ('I have a problem with my subscription', 'I have a problem with my subscription'), ('Others', 'Others'), ('I have a problem with my project', 'I have a problem with my project'), ('My delivery has been delayed', 'My delivery has been delayed'), ('Payments Issue', 'Payments Issue')], max_length=60, verbose_name='Case'),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='type',
            field=models.CharField(choices=[('Zelle', 'Zelle'), ('Paypal', 'Paypal'), ('Binance', 'Binance')], max_length=100, verbose_name='Type of Wallet'),
        ),
    ]
