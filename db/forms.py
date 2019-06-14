from django import forms
from django.conf import settings
from django.db import models
from django.forms.widgets import HiddenInput
from django.forms.utils import flatatt
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    BiologicalReplicate, BiologicalReplicateMetadata, BiologicalReplicateProtocol,
    ComputationalPipeline, PipelineStep, PipelineStepParameter, PipelineResult,
    Investigation, ProtocolStep, ProtocolStepParameter, Sample, SampleMetadata,
    UploadInputFile, UserProfile, ErrorMessage
)

from django_jinja_knockout.forms import (
    DisplayModelMetaclass, FormWithInlineFormsets, RendererModelForm,
    ko_inlineformset_factory, ko_generic_inlineformset_factory, WidgetInstancesMixin,
    BootstrapModelForm
)
from django_jinja_knockout.widgets import ForeignKeyGridWidget, DisplayText

from django.forms import inlineformset_factory, ModelForm


'''
Django-Jinja-Knockout Forms
'''

#Base Forms and Display Forms

class UserProfileForm(RendererModelForm):
    #ModelForm will auto-generate fields which dont already exist
    #Therefore, creating fields prevents auto-generation.
    class Meta:
        model = UserProfile
        fields = ['user']



class UploadForm(WidgetInstancesMixin, BootstrapModelForm):
    class Meta:
        model = UploadInputFile
        fields = ['upload_file']

UserUploadFormset = ko_inlineformset_factory(UserProfile,
                                             UploadInputFile,
                                             form=UploadForm,
                                             extra=0,
                                             min_num=1)
################Experiment
class NewUploadForm(ModelForm):
    class Meta:
        model = UploadInputFile
        #exclude = ('userprofile', )
        fields = ('upload_file',)
    def __init__(self, *args, **kwargs):
        self.userprofile = kwargs.pop('userprofile')
        super(NewUploadForm, self).__init__(*args, **kwargs)


##########################


#This form used only for display purposes
class UploadInputFileDisplayForm(WidgetInstancesMixin,
                                RendererModelForm,
                                metaclass=DisplayModelMetaclass):
        class Meta:
            model=UploadInputFile
            fields = '__all__'

class ErrorDisplayForm(WidgetInstancesMixin, RendererModelForm,
                        metaclass=DisplayModelMetaclass):
    class Meta:
        model = ErrorMessage
        fields = '__all__'



UploadInputFileDisplayErrorFormset = ko_inlineformset_factory(
                                                UploadInputFile,
                                                ErrorMessage,
                                                form=ErrorDisplayForm,
                                                extra=0,
                                                min_num=0,
                                                can_delete=False)

class UploadInputFileDisplayWithInlineErrors(FormWithInlineFormsets):
    FormClass = UploadInputFileDisplayForm
    FormsetClasses =[UploadInputFileDisplayErrorFormset]
    def get_formset_inline_title(self, formset):
        return "Error Messages"

class UserWithInlineUploads(FormWithInlineFormsets):
    FormClass = UserProfileForm
    FormsetClasses = [UserUploadFormset]
    def get_formset_inline_title(self, formset):
        return "User Uploads"


class InvestigationForm(RendererModelForm):
    class Meta:
        model = Investigation
        #fields = '__all__'
        exclude = ['search_vector']

class InvestigationDisplayForm(RendererModelForm,
                               metaclass=DisplayModelMetaclass):
    class Meta:
        model = Investigation
        #fields = '__all__'
        exclude = ['search_vector']


class NameLabelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name,)

class SampleForm(RendererModelForm):
    investigation = NameLabelChoiceField(queryset = Investigation.objects.all())
    class Meta:
        model = Sample
        exclude = ['search_vector']

class SampleDisplayForm(WidgetInstancesMixin, RendererModelForm, metaclass=DisplayModelMetaclass):
    class Meta:
        def get_name(self, value):
            return format_html('<a{}>{}</a>', flatatt({'href': reverse('sample_detail', kwargs={'sample_id': self.instance.pk})}), self.instance.name)
        def get_investigation(self, value):
            return format_html('<a{}>{}</a>', flatatt({'href': reverse('investigation_detail', kwargs={'investigation_id': self.instance.investigation.pk})}), self.instance.investigation.name)

        model = Sample
        exclude = ['search_vector']
        widgets = {'name': DisplayText(get_text_method=get_name),
                   'investigation': DisplayText(get_text_method=get_investigation)}

class ReplicateForm(RendererModelForm):
    class Meta:
        model = BiologicalReplicate
        exclude = ['search_vector']

class ReplicateDisplayForm(RendererModelForm, metaclass=DisplayModelMetaclass):
    class Meta:
        model = BiologicalReplicate
        #fields = '__all__'
        exclude = ['search_vector']

class SampleMetadataForm(RendererModelForm):
    class Meta:
        model = SampleMetadata
        #fields = '__all__'
        exclude = ['search_vector']

class SampleMetadataDisplayForm(RendererModelForm, metaclass=DisplayModelMetaclass):
    class Meta:
        model = SampleMetadata
        exclude = ['search_vector']

class ReplicateMetadataForm(RendererModelForm):
    class Meta:
        model = BiologicalReplicateMetadata
        fields = '__all__'

class ReplicateMetadataDisplayForm(RendererModelForm, metaclass=DisplayModelMetaclass):
    class Meta:
        model = BiologicalReplicateMetadata
        exclude = ['search_vector']


class ProtocolForm(RendererModelForm):
    class Meta:
        model = BiologicalReplicateProtocol
        exclude = ['search_vector']

class ProtocolDisplayForm(RendererModelForm, metaclass=DisplayModelMetaclass):
    class Meta:
        model = BiologicalReplicateProtocol
        exclude = ['search_vector']

class PipelineForm(RendererModelForm):
    class Meta:
        model = ComputationalPipeline
        fields = '__all__'

class PipelineDisplayForm(RendererModelForm, metaclass=DisplayModelMetaclass):
    class Meta:
        model = ComputationalPipeline
        fields = '__all__'

class PipelineResultDisplayForm(RendererModelForm, metaclass=DisplayModelMetaclass):
    class Meta:
        model = PipelineResult
        fields = '__all__'

class ProtocolStepForm(RendererModelForm):
    protocolstep = NameLabelChoiceField(queryset=ProtocolStep.objects.all())
    protocolstep.label = "Protocol Step"
    class Meta:
        model = ProtocolStep
        #fields = '__all__'
        exclude = ['search_vector']
    def __init__(self, *args, **kwargs):
        super(ProtocolStepForm, self).__init__(*args, **kwargs)
        if 'biological_replicate_protocols' in self.fields:
            self.fields.pop('biological_replicate_protocols')
            self.fields.pop('protocolstep')

class ProtocolStepDisplayForm(RendererModelForm, metaclass=DisplayModelMetaclass):
    class Meta:
        model = ProtocolStep
        #fields = '__all__'
        exclude = ['search_vector']

class ProtocolStepParameterForm(RendererModelForm):
    class Meta:
        model = ProtocolStepParameter
        #fields = '__all__'
        exclude = ['search_vector']

class ProtocolStepParameterDisplayForm(RendererModelForm, metaclass=DisplayModelMetaclass):
    class Meta:
        model = ProtocolStepParameter
        #fields = '__all__'
        exclude = ['search_vector']

class PipelineStepForm(RendererModelForm):
    pipelinestep = NameLabelChoiceField(queryset=PipelineStep.objects.all())
    pipelinestep.label = "Pipeline Step"
    class Meta:
        model = PipelineStep
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(PipelineStepForm, self).__init__(*args, **kwargs)
        if 'pipelines' in self.fields:
            self.fields.pop('pipelines')
            self.fields.pop('pipelinestep')

class PipelineStepDisplayForm(RendererModelForm, metaclass=DisplayModelMetaclass):
    class Meta:
        model = PipelineStep
        fields = '__all__'

class PipelineStepParameterForm(RendererModelForm):
    class Meta:
        model = PipelineStepParameter
        fields = '__all__'

class PipelineStepParameterDisplayForm(RendererModelForm, metaclass=DisplayModelMetaclass):
    class Meta:
        model = PipelineStepParameter
        fields = '__all__'

# Inline/Compound Forms

InvestigationSampleFormset = ko_inlineformset_factory(Investigation,
                                                      Sample,
                                                      form=SampleForm,
                                                      extra=0,
                                                      min_num=0)
InvestigationDisplaySampleFormset = ko_inlineformset_factory(
                                                 Investigation,
                                                 Sample,
                                                 form=SampleDisplayForm)



class InvestigationWithInlineSamples(FormWithInlineFormsets):
    FormClass = InvestigationForm
    FormsetClasses = [InvestigationSampleFormset]
    def get_formset_inline_title(self, formset):
        return "Sample"


class InvestigationDisplayWithInlineSamples(FormWithInlineFormsets):
     FormClass = InvestigationDisplayForm
     FormsetClasses = [InvestigationDisplaySampleFormset]
     def get_formset_inline_title(self, formset):
         return "Samples"

SampleDisplayMetadataFormset = ko_inlineformset_factory(Sample,
                                                 SampleMetadata,
                                                 form=SampleMetadataDisplayForm)

SampleDisplayReplicateFormset = ko_inlineformset_factory(Sample,
                                                      BiologicalReplicate,
                                                      form=ReplicateDisplayForm)

SampleMetadataFormset = ko_inlineformset_factory(Sample, SampleMetadata,
                                                 form=SampleMetadataForm,
                                                 extra=0,
                                                 min_num=0)

SampleReplicateFormset = ko_inlineformset_factory(Sample, BiologicalReplicate,
                                                  form=ReplicateForm,
                                                  extra=0, min_num=0)

class SampleWithInlineMetadata(FormWithInlineFormsets):
    FormClass = SampleForm
    FormsetClasses = [SampleMetadataFormset]
    def get_formset_inline_title(self, formset):
        return "Sample Metadata"

class SampleDisplayWithInlineMetadata(FormWithInlineFormsets):
    FormClass = SampleDisplayForm
    FormsetClasses = [SampleDisplayReplicateFormset, \
                      SampleDisplayMetadataFormset]
    def get_formset_inline_title(self, formset):
        if formset.model == BiologicalReplicate:
            return "Biological Replicates"
        return "Sample Metadata"

ReplicateDisplayMetadataFormset = ko_inlineformset_factory(BiologicalReplicate,
                                                 BiologicalReplicateMetadata,
                                                 form=ReplicateMetadataDisplayForm)

ReplicateMetadataFormset = ko_inlineformset_factory(BiologicalReplicate, BiologicalReplicateMetadata,
                                                 form=ReplicateMetadataForm,
                                                 extra=0,
                                                 min_num=0)

class ReplicateWithInlineMetadata(FormWithInlineFormsets):
    FormClass = ReplicateForm
    FormsetClasses = [ReplicateMetadataFormset]
    def get_formset_inline_title(self, formset):
        return "Replicate Metadata"

class ReplicateDisplayWithInlineMetadata(FormWithInlineFormsets):
    FormClass = ReplicateDisplayForm
    FormsetClasses = [ReplicateDisplayMetadataFormset]
    def get_formset_inline_title(self, formset):
        if formset.model == BiologicalReplicate:
            return "Biological Replicates"
        return "Sample Metadata"

ProtocolStepDisplayFormset = ko_inlineformset_factory(BiologicalReplicateProtocol,
                                                      ProtocolStep.biological_replicate_protocols.through,
                                                      form=ProtocolStepDisplayForm)

ProtocolStepFormset = ko_inlineformset_factory(BiologicalReplicateProtocol,
                                               ProtocolStep.biological_replicate_protocols.through,
                                               form=ProtocolStepForm,
                                               extra=0, min_num=0)

class ProtocolDisplayWithInlineSteps(FormWithInlineFormsets):
    FormClass = ProtocolDisplayForm
    FormsetClasses = [ProtocolStepDisplayFormset]
    def get_formset_inline_title(self, formset):
        return "Protocol Step"

class ProtocolWithInlineSteps(FormWithInlineFormsets):
    FormClass = ProtocolForm
    FormsetClasses = [ProtocolStepFormset]
    def get_formset_inline_title(self, formset):
        return "Protocol Steps"

ProtocolStepParameterDisplayFormset = ko_inlineformset_factory(ProtocolStep,
                                                      ProtocolStepParameter,
                                                      form = ProtocolStepParameterDisplayForm)

ProtocolStepParameterFormset = ko_inlineformset_factory(ProtocolStep,
                                                        ProtocolStepParameter,
                                                        form = ProtocolStepParameterForm,
                                                        extra=0, min_num=0)

class ProtocolStepWithInlineParameters(FormWithInlineFormsets):
    FormClass = ProtocolStepForm
    FormsetClasses = [ProtocolStepParameterFormset]
    def get_formset_inline_title(self, formset):
        return "Protocol Step Parameter"

class ProtocolStepDisplayWithInlineParameters(FormWithInlineFormsets):
    FormClass = ProtocolStepDisplayForm
    FormsetClasses = [ProtocolStepParameterDisplayFormset]
    def get_formset_inline_title(self, formset):
        return "Protocol Step Parameters"


PipelineStepDisplayFormset = ko_inlineformset_factory(ComputationalPipeline,
                                                      PipelineStep.pipelines.through,
                                                      form=PipelineStepDisplayForm)

PipelineStepFormset = ko_inlineformset_factory(ComputationalPipeline,
                                               PipelineStep.pipelines.through,
                                               form=ProtocolStepForm,
                                               extra=0, min_num=0)

class PipelineDisplayWithInlineSteps(FormWithInlineFormsets):
    FormClass = PipelineDisplayForm
    FormsetClasses = [PipelineStepDisplayFormset]
    def get_formset_inline_title(self, formset):
        return "Pipeline Step"

class PipelineWithInlineSteps(FormWithInlineFormsets):
    FormClass = PipelineForm
    FormsetClasses = [PipelineStepFormset]
    def get_formset_inline_title(self, formset):
        return "Pipeline Steps"

PipelineStepParameterDisplayFormset = ko_inlineformset_factory(PipelineStep,
                                                      PipelineStepParameter,
                                                      form = PipelineStepParameterDisplayForm)

PipelineStepParameterFormset = ko_inlineformset_factory(PipelineStep,
                                                        PipelineStepParameter,
                                                        form = PipelineStepParameterForm,
                                                        extra=0, min_num=0)

class PipelineStepWithInlineParameters(FormWithInlineFormsets):
    FormClass = PipelineStepForm
    FormsetClasses = [PipelineStepParameterFormset]
    def get_formset_inline_title(self, formset):
        return "Pipeline Step Parameter"

class PipelineStepDisplayWithInlineParameters(FormWithInlineFormsets):
    FormClass = PipelineStepDisplayForm
    FormsetClasses = [PipelineStepParameterDisplayFormset]
    def get_formset_inline_title(self, formset):
        return "Pipeline Step Parameters"

##### Search form
class SearchBarForm(forms.Form):
    search = forms.CharField(max_length=100)
