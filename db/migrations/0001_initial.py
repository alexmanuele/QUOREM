# Generated by Django 2.1.3 on 2018-12-07 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BiologicalReplicate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='BiologicalReplicateMetadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=256)),
                ('value', models.CharField(max_length=256)),
                ('biological_replicate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.BiologicalReplicate')),
            ],
        ),
        migrations.CreateModel(
            name='BiologicalReplicateProtocol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('biological_replicate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.BiologicalReplicate')),
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
                ('md5_hash', models.CharField(max_length=256)),
                ('document', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Investigation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('institution', models.CharField(max_length=256)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='PipelineDeviation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='PipelineParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=256)),
                ('key', models.CharField(max_length=256)),
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
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='ProtocolParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('value', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='ProtocolParameterDeviation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('biological_replicate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.BiologicalReplicate')),
            ],
        ),
        migrations.CreateModel(
            name='ProtocolStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_name', models.CharField(max_length=256)),
                ('method', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('biological_replicate_protocol', models.ManyToManyField(to='db.BiologicalReplicateProtocol')),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('investigation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.Investigation')),
            ],
        ),
        migrations.CreateModel(
            name='SampleMetadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=256)),
                ('value', models.CharField(max_length=256)),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.Sample')),
            ],
        ),
        migrations.AddField(
            model_name='protocolparameterdeviation',
            name='protocol_step',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.ProtocolStep'),
        ),
        migrations.AddField(
            model_name='protocolparameter',
            name='protocol_step',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.ProtocolStep'),
        ),
        migrations.AddField(
            model_name='pipelineresult',
            name='pipeline_step',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.PipelineStep'),
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
            model_name='computationalpipeline',
            name='pipeline_step',
            field=models.ManyToManyField(to='db.PipelineStep'),
        ),
        migrations.AddField(
            model_name='biologicalreplicate',
            name='biological_replicate_protocol',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='db.BiologicalReplicateProtocol'),
        ),
        migrations.AddField(
            model_name='biologicalreplicate',
            name='sample',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.Sample'),
        ),
        migrations.AddField(
            model_name='biologicalreplicate',
            name='sequence_file',
            field=models.ManyToManyField(to='db.Document'),
        ),
    ]
