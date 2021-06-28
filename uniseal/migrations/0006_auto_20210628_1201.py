# Generated by Django 3.2.3 on 2021-06-28 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('uniseal', '0005_auto_20210628_1022'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=100, unique=True, verbose_name='Phone Number')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email Address')),
                ('address', models.CharField(max_length=250, verbose_name='Address')),
                ('message', models.TextField(verbose_name='Message')),
                ('website', models.URLField(verbose_name='Website')),
                ('facebook', models.URLField(verbose_name='Facebook')),
                ('twitter', models.URLField(verbose_name='Twitter')),
                ('linkedin', models.URLField(verbose_name='LinkedIn')),
                ('instagram', models.URLField(verbose_name='Instagram')),
            ],
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Solution Title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Solution Description')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='beneficiary',
            field=models.CharField(default='', max_length=100, verbose_name='Project Beneficiary'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='title',
            field=models.CharField(default='', max_length=120, verbose_name='Project Title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sellingpoint',
            name='area',
            field=models.CharField(choices=[('Om-Baddah', 'om-baddah'), ('Al-Saffyah', 'Al-Saffyah'), ('Hay Alarab', 'Hay Alarab'), ('Wad Nubawi', 'Wad Nubawi'), ('Al Mawrada', 'Al Mawrada'), ('Hay Al-Omda', 'Hay Al-Omda'), ('Al Mohandsin', 'Al Mohandsin'), ('Al Molazmin', 'Al Molazmin'), ('Al Arda', 'Al Arda'), ('Banat gharb', 'Banat gharb'), ('Al Hashmab', 'Al Hashmab'), ('Banat sharg', 'Banat sharg'), ('Hai Al nakhiel', 'Hai Al nakhiel'), ('Emtidad bait Al mal', 'Emtidad bait Al mal'), ('Al Sharfiya', 'Al Sharfiya'), ('Al Jarrafa', 'Al Jarrafa'), ('Al Thawra', 'Al Thawra'), ('Abu Roof', 'Abu Roof'), ('Wd Abu Halima', 'Wd Abu Halima'), ('Hay Al-umara Gharb', 'Hay Al-umara Gharb'), ('Bait Al Mal', 'Bait Al Mal'), ('Al Waaha', 'Al Waaha'), ('AL Kabajab', 'AL Kabajab'), ('Hay Al Bosta', 'Hay Al Bosta'), ('Hay Al Mostashfa', 'Hay Al Mostashfa'), ('Al Riyadh', 'Al Riyadh'), ('Al Msalmaa', 'Al Msalmaa'), ('Hay Al-Umara East', 'Hay Al-Umara East'), ('Al Dawha', 'Al Dawha'), ('Sug Al khalifa', 'Sug Al khalifa'), ('Om Bada', 'Om Bada'), ('Alamlaak', 'Alamlaak'), ('Cooper', 'Cooper'), ('Kafouri', 'Kafouri'), ('Bahri Industrial Area', 'Bahri Industrial Area'), ('Al Haj Yousif', 'Al Haj Yousif'), ('Al Sababi', 'Al Sababi'), ('Al Dnagla North', 'Al Dnagla North'), ('Al Dnagla South', 'Al Dnagla South'), ('Hilat Hamad', 'Hilat Hamad'), ('Hilat Khojali', 'Hilat Khojali'), ('Hilat Koko', 'Hilat Koko'), ('Alshabia North', 'Alshabia North'), ('Alshabia South', 'Alshabia South'), ('Almazad', 'Almazad'), ('Almugtaribin', 'Almugtaribin'), ('Almerghania', 'Almerghania'), ('Alsafia', 'Alsafia'), ('Shambat', 'Shambat'), ('AlKhoglab', 'AlKhoglab'), ('Alqadisia', 'Alqadisia'), ('Alhalfaya', 'Alhalfaya'), ('Dardoog', 'Dardoog'), ('Aldroshab', 'Aldroshab'), ('Alkadaro', 'Alkadaro'), ('Alezba', 'Alezba'), ('Alfaki Hashim', 'Alfaki Hashim'), ('Al Gayli', 'Al Gayli'), ('Al Riyadh', 'Al Riyadh'), ('Alamarat', 'Alamarat'), ('Khartoum2', 'Khartoum2'), ('Al-Hilla Al-Jadida', 'Al-Hilla Al-Jadida'), ('Al Diyum East', 'Al Diyum East'), ('khartoum3', 'khartoum3'), ('Burri Almahas', 'Burri Almahas'), ('Nasir Extension', 'Nasir Extension'), ('Al-LaMap', 'Al-LaMap'), ('Burri Al Daraisa', 'Burri Al Daraisa'), ('Burri Alsharif', 'Burri Alsharif'), ('Taha Elmahi', 'Taha Elmahi'), ('Al-Emtidad', 'Al-Emtidad'), ('Saria Residence', 'Saria Residence'), ('Al-Aushara', 'Al-Aushara'), ('Wad-Ageeb', 'Wad-Ageeb'), ('Kalakla Wad Amara', 'Kalakla Wad Amara'), ('Al Diyum West', 'Al Diyum West'), ('Alfirdous East', 'Alfirdous East'), ('Jabra Sharga', 'Jabra Sharga'), ('Al-Jerif West Al-Galaa', 'Al-Jerif West Al-Galaa'), ('Umm Haraz', 'Umm Haraz'), ('Nuzha', 'Nuzha'), ('Wad Husayn', 'Wad Husayn'), ('Al Zohur', 'Al Zohur'), ('Gabra 18', 'Gabra 18'), ('Burri Al Lamab', 'Burri Al Lamab'), ('Abu Dawm', 'Abu Dawm'), ('Garden City', 'Garden City'), ('Gabra 19', 'Gabra 19'), ('Gabra 15', 'Gabra 15'), ('Gabra AlDawha', 'Gabra AlDawha'), ('Gabra 10', 'Gabra 10'), ('Gabra 9', 'Gabra 9')], default=1, max_length=300, verbose_name='Area'),
        ),
        migrations.AddField(
            model_name='sellingpoint',
            name='city',
            field=models.CharField(choices=[('Al-Khartoum', 'Al-Khartoum'), ('Bahry', 'Bahry'), ('Om-Durman', 'Om-Durman')], default=1, max_length=350, verbose_name='City'),
        ),
        migrations.AddField(
            model_name='sellingpoint',
            name='email',
            field=models.EmailField(default='', max_length=255, unique=True, verbose_name='Email Address'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sellingpoint',
            name='phone_number',
            field=models.CharField(default='', max_length=100, unique=True, verbose_name='Phone Number'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='category',
            field=models.CharField(max_length=100, verbose_name='Project Category'),
        ),
        migrations.CreateModel(
            name='SolutionVideos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.URLField(verbose_name='Solution Video Url')),
                ('solution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uniseal.solution', verbose_name='Solution')),
            ],
        ),
        migrations.CreateModel(
            name='SolutionImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='solution_images', verbose_name='Solution Image')),
                ('solution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uniseal.solution', verbose_name='Solution')),
            ],
        ),
    ]
