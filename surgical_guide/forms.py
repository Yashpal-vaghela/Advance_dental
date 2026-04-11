from django import forms
from .models import SurgicalGuide


class SurgicalGuideForm(forms.ModelForm):
    jaw_information = forms.MultipleChoiceField(
        choices=[
            ('maxilla', 'Maxilla'),
            ('mandible', 'Mandible')
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = SurgicalGuide
        fields = '__all__'

    def clean_immediate_extractions(self):
        val = self.data.get('immediate_extractions')
        if val == 'True':
            return True
        elif val == 'False':
            return False
        return None

    def clean_bone_grafting(self):
        val = self.data.get('bone_grafting')
        if val == 'True':
            return True
        elif val == 'False':
            return False
        return None

    def clean_bone_reduction(self):
        val = self.data.get('bone_reduction')
        if val == 'True':
            return True
        elif val == 'False':
            return False
        return None