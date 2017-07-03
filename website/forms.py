from django.contrib.auth.models import User
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.widgets import CheckboxChoiceInput
from .models import *


USER_TYPE = (
    ('Student','Student'),
    ('Admin','Admin')
)

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'type' : 'password','name':'p','placeholder':'Password'}))

    class Meta:
        model = User
        fields = ['username','password']


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'type': 'password', 'name': 'p', 'placeholder': 'Password'}))
    cpassword = forms.CharField(
        widget=forms.PasswordInput(attrs={'type': 'password', 'name': 'p', 'placeholder': 'Password'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(u'Username "%s" is already in use.' % username)

    def clean_password(self):
        value_password = self.cleaned_data.get('password')
        if len(str(self.cleaned_data['password'])) < 8:
            raise forms.ValidationError("Password too short")
        elif len(str(self.cleaned_data['password'])) > 45:
            raise forms.ValidationError("Password too long")
        return value_password

    def clean_cpassword(self):
        value_password2 = self.cleaned_data.get('cpassword')
        if len(str(self.cleaned_data['cpassword'])) < 8:
            raise forms.ValidationError("Password too short")
        elif len(str(self.cleaned_data['cpassword'])) > 45:
            raise forms.ValidationError("Password too long")
        return value_password2

    class Meta:
        model = User
        fields = ['username', 'password','cpassword','first_name','last_name','email']

class ProjectForm(forms.ModelForm):

    m_id = forms.ModelChoiceField(queryset=student.objects.all())

    class Meta:
        model =  projects
        fields = ['p_name','m_id']

class WorkForm(forms.ModelForm):

    class Meta:
        model = work_log
        fields = ['desc']

class TeamForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        proj = kwargs.pop('proj')
        super(TeamForm, self).__init__(*args, **kwargs)
        students_in_proj_role = role.objects.filter(p_id=proj)
        students_in_proj = list()
        for student_role in students_in_proj_role:
            student_inst = student_role.s_id
            students_in_proj.append(student_inst)
        self.fields['t_leader'] = forms.ModelChoiceField(queryset=student.objects.all().exclude(id__in=[o.id for o in students_in_proj]))

    t_leader = forms.ModelChoiceField(queryset=student.objects.all())

    class Meta:
        model=teams
        fields = ['t_name','t_leader']

class MemberForm_Leader(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        proj = kwargs.pop('proj')
        super(MemberForm_Leader, self).__init__(*args, **kwargs)
        students_in_proj_role = role.objects.filter(p_id=proj)
        students_in_proj = list()
        for student_role in students_in_proj_role:
            student_inst = student_role.s_id
            students_in_proj.append(student_inst)
        self.fields['mem_id'] = forms.ModelChoiceField(queryset=student.objects.all().exclude(id__in=[o.id for o in students_in_proj]))


    class Meta:
        model=team_member
        fields = ['mem_id']


class MemberForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        proj = kwargs.pop('proj')
        super(MemberForm, self).__init__(*args, **kwargs)
        self.fields['team']=forms.ModelChoiceField(queryset=teams.objects.filter(p_id=proj))
        students_in_proj_role = role.objects.filter(p_id=proj)
        students_in_proj = list()
        for student_role in students_in_proj_role:
            student_inst = student_role.s_id
            students_in_proj.append(student_inst)
        self.fields['mem_id'] = forms.ModelChoiceField(queryset=student.objects.all().exclude(id__in=[o.id for o in students_in_proj]))

    class Meta:
        model=team_member
        fields = ['mem_id']


class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadModel
        exclude = ('p_id','date',)

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()