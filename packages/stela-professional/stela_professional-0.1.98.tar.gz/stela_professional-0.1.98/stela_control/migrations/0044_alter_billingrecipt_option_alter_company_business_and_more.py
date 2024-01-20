# Generated by Django 5.0.1 on 2024-01-16 19:29

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stela_control', '0043_taxreturn_type_alter_billingrecipt_option_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingrecipt',
            name='option',
            field=models.CharField(choices=[('Billing receipt', 'Billing receipt'), ('budget_development', 'Budget Development'), ('budget_design', 'Budget Design'), ('budget_marketing', 'Budget Marketing'), ('Others', 'Others'), ('Monthly charge', 'Monthly charge')], max_length=60, null=True, verbose_name='Case'),
        ),
        migrations.AlterField(
            model_name='company',
            name='business',
            field=models.CharField(blank=True, choices=[('Restaurants and Food Services', 'Restaurants and Food Services'), ('Repair and Maintenance Services', 'Repair and Maintenance Services'), ('E-commerce', 'E-commerce'), ('Marketing and Advertising Services', 'Marketing and Advertising Services'), ('IT Development Services', 'IT Development Services'), ('Education and Training', 'Education and Training'), ('Health and Wellness', 'Health and Wellness'), ('Logistics and Transportation Services', 'Logistics and Transportation Services'), ('Beauty and Personal Care Services', 'Beauty and Personal Care Services'), ('Consulting', 'Consulting'), ('Media Creators', 'Media Creators')], max_length=100, null=True, verbose_name='Business Type'),
        ),
        migrations.AlterField(
            model_name='content',
            name='card',
            field=models.CharField(blank=True, choices=[('card-tale', 'card-tale'), ('card-dark-blue', 'card-dark-blue'), ('card-light-danger', 'card-light-danger'), ('card-light-blue', 'card-light-blue')], max_length=50, null=True, verbose_name='Color Card'),
        ),
        migrations.AlterField(
            model_name='content',
            name='category',
            field=models.CharField(blank=True, choices=[('Stories', 'Stories'), ('Resources', 'Resources'), ('Interviews', 'Interviews'), ('Advices', 'Advices'), ('Events', 'Events'), ('News', 'News')], default='News', max_length=100),
        ),
        migrations.AlterField(
            model_name='facebookpagecomments',
            name='update_rate',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 16, 16, 29, 43, 370980)),
        ),
        migrations.AlterField(
            model_name='itemdiscount',
            name='field',
            field=models.CharField(choices=[('Promotional Discount', 'Promotional Discount'), ('Stela Payment Free Suscription', 'Stela Payment Free Suscription'), ('No Selected', 'No Selected'), ('Initial Payment', 'Initial Payment')], max_length=60),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='template',
            field=models.CharField(choices=[('Style Template 2', 'Style Template 2'), ('Style Template 1', 'Style Template 1'), ('Style Template 3', 'Style Template 3'), ('Style Template 4', 'Style Template 4')], max_length=60, null=True, verbose_name='Style'),
        ),
        migrations.AlterField(
            model_name='order',
            name='section',
            field=models.CharField(choices=[('Stela Design', 'Stela Design'), ('Store', 'Store'), ('Stela Websites', 'Stela Websites'), ('Cloud Domains', 'Cloud Domains'), ('Stela Marketing', 'Stela Marketing'), ('No Selected', 'No Selected'), ('Cloud Elastic Instance', 'Cloud Elastic Instance')], default='No Selected', max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=100),
        ),
        migrations.AlterField(
            model_name='pathcontrol',
            name='step',
            field=models.CharField(choices=[('Step 3', 'Step 3'), ('Step 4', 'Step 4'), ('Step 2', 'Step 2')], default='No Selected', max_length=50),
        ),
        migrations.AlterField(
            model_name='sendmoney',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=50),
        ),
        migrations.AlterField(
            model_name='sitepolicy',
            name='section',
            field=models.CharField(blank=True, choices=[('Privacy Policy', 'Privacy Policy'), ('Cookie Policy', 'Cookie Policy'), ('Return Policy', 'Return Policy'), ('budget_development_terms', 'Budget Development Terms'), ('monthly_terms', 'Billing Terms'), ('budget_marketing_terms', 'Budget Marketing Terms'), ('Disclaimer', 'Disclaimer'), ('billing_terms', 'Monthly Billing Terms'), ('Terms and Conditions', 'Terms and Conditions'), ('budget_design_terms', 'Budget Design Terms')], default='Terms and Conditions', max_length=150),
        ),
        migrations.AlterField(
            model_name='sociallinks',
            name='social',
            field=models.CharField(choices=[('Instagram', 'Instagram'), ('Tiktok', 'Tiktok'), ('Linkedin', 'Linkedin'), ('Github', 'Github'), ('Youtube', 'Youtube'), ('X', 'X'), ('Facebook', 'Facebook'), ('Wikipedia', 'Wikipedia')], default='No Selected', max_length=50),
        ),
        migrations.AlterField(
            model_name='support',
            name='option',
            field=models.CharField(choices=[('Others', 'Others'), ('Payments Issue', 'Payments Issue'), ('My account has an error', 'My account has an error'), ('I have a problem with my subscription', 'I have a problem with my subscription'), ('My delivery has been delayed', 'My delivery has been delayed'), ('I have a problem with my project', 'I have a problem with my project')], max_length=60, verbose_name='Case'),
        ),
        migrations.AlterField(
            model_name='support',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='type',
            field=models.CharField(choices=[('Paypal', 'Paypal'), ('Binance', 'Binance'), ('Zelle', 'Zelle')], max_length=100, verbose_name='Type of Wallet'),
        ),
        migrations.CreateModel(
            name='UserMessages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=60)),
                ('message', models.TextField(verbose_name='Brief description')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_messages', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
