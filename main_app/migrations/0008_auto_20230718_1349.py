# Generated by Django 3.2 on 2023-07-18 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_auto_20230718_1210'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberprofile',
            name='bio',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='memberprofile',
            name='category',
            field=models.CharField(choices=[('all', 'ALL Member Categories'), ('1', 'Attorney/Legal'), ('2', 'Author/Publisher'), ('3', 'Course Designer'), ('4', 'CPA'), ('5', 'Education Director'), ('6', 'Inspirational'), ('7', 'National Speaker'), ('8', 'Online Real Estate School/Educator'), ('9', 'Online Training'), ('10', 'Professor/Educator'), ('11', 'Real Estate Association'), ('12', 'Real Estate Regulator'), ('13', 'Real Estate School'), ('14', 'Real Estate School Owner/Administrator'), ('15', 'Trainer/Educator/Instructor'), ('16', 'Training Consultant/Coach')], default='all', max_length=255),
        ),
        migrations.AddField(
            model_name='memberprofile',
            name='certificate',
            field=models.CharField(choices=[('any', 'ANY Certifications'), ('drei', 'Distinguished Real Estate Instructors (REEA DREI)'), ('gsl', 'Gold Standard Leader Certification (REEA GSL)'), ('gsi', 'Gold Standard Instructors (GSI)')], default='any', max_length=255),
        ),
        migrations.AddField(
            model_name='memberprofile',
            name='company_organization',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='memberprofile',
            name='display_email',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='memberprofile',
            name='display_number',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='memberprofile',
            name='first_name',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='memberprofile',
            name='is_member',
            field=models.BooleanField(default='False'),
        ),
        migrations.AddField(
            model_name='memberprofile',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='memberprofile',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='memberprofile',
            name='office_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='memberprofile',
            name='office_number',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='memberprofile',
            name='personal_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='memberprofile',
            name='state',
            field=models.CharField(choices=[('all', 'All States'), ('alabama', 'AL - Alabama'), ('alaska', 'AK - Alaska'), ('arizona', 'AZ - Arizona'), ('arkansas', 'AR - Arkansas'), ('california', 'CA - California'), ('colorado', 'CO - Colorado'), ('connecticut', 'CT - Connecticut'), ('delaware', 'DE - Delaware'), ('florida', 'FL - Florida'), ('georgia', 'GA - Georgia'), ('hawaii', 'HI - Hawaii'), ('idaho', 'ID - Idaho'), ('illinois', 'IL - Illinois'), ('indiana', 'IN - Indiana'), ('iowa', 'IA - Iowa'), ('kansas', 'KS - Kansas'), ('kentucky', 'KY - Kentucky'), ('louisiana', 'LA - Louisiana'), ('maine', 'ME - Maine'), ('maryland', 'MD - Maryland'), ('massachusetts', 'MA - Massachusetts'), ('michigan', 'MI - Michigan'), ('minnesota', 'MN - Minnesota'), ('mississippi', 'MS - Mississippi'), ('missouri', 'MO - Missouri'), ('montana', 'MT - Montana'), ('nebraska', 'NE - Nebraska'), ('nevada', 'NV - Nevada'), ('new_hampshire', 'NH - New Hampshire'), ('new_jersey', 'NJ - New Jersey'), ('new_mexico', 'NM - New Mexico'), ('new_york', 'NY - New York'), ('north_carolina', 'NC - North Carolina'), ('north_dakota', 'ND - North Dakota'), ('ohio', 'OH - Ohio'), ('oklahoma', 'OK - Oklahoma'), ('oregon', 'OR - Oregon'), ('pennsylvania', 'PA - Pennsylvania'), ('rhode_island', 'RI - Rhode Island'), ('south_carolina', 'SC - South Carolina'), ('south_dakota', 'SD - South Dakota'), ('tennessee', 'TN - Tennessee'), ('texas', 'TX - Texas'), ('utah', 'UT - Utah'), ('vermont', 'VT - Vermont'), ('virginia', 'VA - Virginia'), ('washington', 'WA - Washington'), ('west_virginia', 'WV - West Virginia'), ('wisconsin', 'WI - Wisconsin'), ('wyoming', 'WY - Wyoming')], default='all', max_length=255),
        ),
        migrations.AddField(
            model_name='memberprofile',
            name='website',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
