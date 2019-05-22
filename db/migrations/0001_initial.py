# Generated by Django 2.1.3 on 2019-05-21 17:00

from django.conf import settings
import django.contrib.postgres.search
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BiologicalReplicate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('search_vector', django.contrib.postgres.search.SearchVectorField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BiologicalReplicateMetadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('search_vector', django.contrib.postgres.search.SearchVectorField(null=True)),
                ('biological_replicate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.BiologicalReplicate')),
            ],
        ),
        migrations.CreateModel(
            name='BiologicalReplicateProtocol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('citation', models.TextField()),
                ('search_vector', django.contrib.postgres.search.SearchVectorField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ComputationalPipeline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('md5_hash', models.CharField(max_length=255)),
                ('document', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='ErrorMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('error_message', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Investigation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('institution', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('search_vector', django.contrib.postgres.search.SearchVectorField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PipelineDeviation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PipelineParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('key', models.CharField(max_length=255)),
                ('computational_pipeline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.ComputationalPipeline')),
            ],
        ),
        migrations.CreateModel(
            name='PipelineResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('computational_pipeline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.ComputationalPipeline')),
                ('document', models.ManyToManyField(to='db.Document')),
            ],
        ),
        migrations.CreateModel(
            name='PipelineStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ProtocolParameterDeviation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('value', models.TextField()),
                ('biological_replicate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.BiologicalReplicate')),
            ],
        ),
        migrations.CreateModel(
            name='ProtocolStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('method', models.CharField(max_length=255)),
                ('biological_replicate_protocols', models.ManyToManyField(blank=True, to='db.BiologicalReplicateProtocol')),
            ],
        ),
        migrations.CreateModel(
            name='ProtocolStepParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('protocol_step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.ProtocolStep', verbose_name='Protocol Step')),
            ],
        ),
        migrations.CreateModel(
            name='ProtocolStepParameterDeviation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_value', models.CharField(max_length=255)),
                ('comment', models.TextField(blank=True)),
                ('biological_replicate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.BiologicalReplicate')),
                ('protocol_step_parameter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.ProtocolStepParameter')),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('search_vector', django.contrib.postgres.search.SearchVectorField(null=True)),
                ('investigation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.Investigation')),
            ],
        ),
        migrations.CreateModel(
            name='SampleMetadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('search_vector', django.contrib.postgres.search.SearchVectorField(null=True)),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.Sample')),
            ],
        ),
        migrations.CreateModel(
            name='UploadInputFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_file', models.FileField(upload_to='upload/')),
                ('upload_status', models.CharField(choices=[('P', 'Processing'), ('S', 'Success'), ('E', 'Error')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='uploadinputfile',
            name='userprofile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.UserProfile', verbose_name='Uploader'),
        ),
        migrations.AddField(
            model_name='protocolparameterdeviation',
            name='protocol_step',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.ProtocolStep'),
        ),
        migrations.AddField(
            model_name='pipelineresult',
            name='pipeline_step',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.PipelineStep'),
        ),
        migrations.AddField(
            model_name='pipelineresult',
            name='replicates',
            field=models.ManyToManyField(to='db.BiologicalReplicate'),
        ),
        migrations.AddField(
            model_name='pipelineparameter',
            name='pipeline_step',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.PipelineStep'),
        ),
        migrations.AddField(
            model_name='pipelinedeviation',
            name='pipeline_parameter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.PipelineParameter'),
        ),
        migrations.AddField(
            model_name='pipelinedeviation',
            name='pipeline_result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.PipelineResult'),
        ),
        migrations.AddField(
            model_name='errormessage',
            name='uploadinputfile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.UploadInputFile', verbose_name='Uploaded File'),
        ),
        migrations.AddField(
            model_name='computationalpipeline',
            name='pipeline_step',
            field=models.ManyToManyField(to='db.PipelineStep'),
        ),
        migrations.AddField(
            model_name='biologicalreplicate',
            name='biological_replicate_protocol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.BiologicalReplicateProtocol'),
        ),
        migrations.AddField(
            model_name='biologicalreplicate',
            name='investigation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.Investigation'),
        ),
        migrations.AddField(
            model_name='biologicalreplicate',
            name='sample',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sample', to='db.Sample'),
        ),
        migrations.AddField(
            model_name='biologicalreplicate',
            name='sequence_file',
            field=models.ManyToManyField(to='db.Document'),
        ),
    ]
