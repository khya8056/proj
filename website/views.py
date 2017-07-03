from django.shortcuts import render,redirect
from django.http.response import HttpResponse,HttpResponseRedirect,HttpResponseForbidden
from django.contrib.auth import authenticate,login,logout
from django.views.generic import View
from django.contrib.auth import logout as django_logout
from .models import *
from .forms import *
from PrjctMngr import settings
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from filetransfers.api import prepare_upload
from django.core.urlresolvers import reverse
from filetransfers.api import serve_file
import datetime
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.conf import settings
import re
from django.shortcuts import get_object_or_404
# Create your views here.
usertype=0
flag=0

def redir(request):
    return redirect('login')


class LoginFormView(View):
    form_class = LoginForm
    template_name='login.html'

    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form': form,'flag':flag})

    def post(self,request):
        flag=0
        form = self.form_class(None)
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)

        if user is not None :


            if user.is_active:
                login(request,user)
                if main_admin.objects.filter(u_id=user.id).exists():
                    curr_admin = main_admin.objects.get(u_id=user)
                    if projects.objects.filter(admin=curr_admin).exists():
                        project=projects.objects.filter(admin=curr_admin)[:1].get()
                        return redirect('/home/admin_home?p_id='+str(project.id))
                    else:
                        return redirect('/home/admin_home?p_id=-1')
                else:
                    curr_student = student.objects.get(u_id=user)
                    if role.objects.filter(s_id=curr_student).exists():
                        obj = role.objects.filter(s_id=curr_student)[:1].get()
                        project = obj.p_id
                        role_inst = role.objects.get(p_id=project,s_id=curr_student).role
                        return redirect('/home/student_home?p_id='+str(project.id))
                    else:
                        return redirect('/home/student_home?p_id=-1')

        return render(request,self.template_name, {'form': form})


def logout(request):
    django_logout(request)
    return redirect('login')


class RegisterFormView(View):
    form_class = RegisterForm
    template_name = 'register.html'
    flag1=0
    def get(self,request):
        form = self.form_class(None)
        flag1=0
        return render(request,self.template_name,{'form': form})

    def post(self,request):
        form = self.form_class(request.POST)
        err = "Username already exists. Please try again"
        flag1=1
        flag2=0
        flag3=0
        if form.is_valid():

            user = form.save(commit=False)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            print("first")
            password = form.cleaned_data['password']
            if len(password) < 8:
                err1 = "Password length is too short. Please try again"
                flag2=1
            cpassword = form.cleaned_data['cpassword']
            if(flag2 == 1):
                return render(request,'register.html',context={'err1':err1,'fname':first_name,'lname':last_name,'username':username})

            if password!=cpassword:
                str = "Passwords Don't match"
                return render(request,self.template_name,context={'err2':str,'fname':first_name,'lname':last_name,'username':username})
            user.set_password(password)
            user.save()
            stud1 = student()
            stud1.u_id = user
            stud1.save()

            user = authenticate(username=username,password=password)

            if user is not None :

                if user.is_active:
                    login(request,user)
                    return redirect('/home/student_home?p_id=-1')
        return render(request, self.template_name, {'form': form})

class AdminHomeView(View):
    template_name='homeadmin.html'

    def get(self,request):
        if not request.user.is_authenticated():
            return redirect('login')
        else:
            curr_admin = main_admin.objects.get(u_id=request.user)
            project_list = projects.objects.filter(admin=curr_admin)
            curr_project_id = request.GET['p_id']
            noti = notification.objects.filter(u_id=request.user.id).order_by("-date")[:5]
            if curr_project_id!=str(-1):
                curr_proj = projects.objects.get(id=curr_project_id)
                mngr = curr_proj.m_id
                mngr_user = mngr.u_id
                team_list = teams.objects.filter(p_id=curr_proj)
                temp = student.objects.all()
                usertype=0
                files = UploadModel.objects.filter(p_id=curr_proj).order_by("-date")[:4]
                return render(request,self.template_name,context={'files':files,'project':curr_proj,'currentuser':curr_admin,'usertype':usertype,'noti':noti,'choices':temp,'p_list': project_list , 'curr_proj':curr_proj , 'proj_mngr':mngr_user , 'team_list':team_list })
            else:
                temp = User.objects.all()
                return render(request,self.template_name,context={'currentuser':curr_admin,'noti':noti,'choices':temp})
class CreateProjectView(View):
    template_name='addproject.html'
    form_class = ProjectForm
    def get(self,request):
        if not request.user.is_authenticated():
            return redirect('login')
        else:
            form = self.form_class(request.POST)
            temp = student.objects.all()
            curr_admin = main_admin.objects.get(u_id=request.user.id)
            if projects.objects.filter(admin=curr_admin).exists():
                project=projects.objects.filter(admin=curr_admin)[:1].get()
                return render(request,self.template_name,context={'currentuser':curr_admin,'project':project,'form':form , 'choices' : temp})
            else:
                return render(request,self.template_name,context={'currentuser':curr_admin,'form':form , 'choices' : temp})

    def post(self,request):
        form = self.form_class(request.POST)


        if form.is_valid():

            current_user = request.user
            admin_object = main_admin.objects.get(u_id=current_user)
            project = form.save(commit=False)
            project.admin = admin_object
            project.p_name = form.cleaned_data['p_name']
            project.m_id = form.cleaned_data['m_id']
            project.save()
            mngr = proj_mngr()
            student = project.m_id
            mngr.u_id = student.u_id
            mngr.admin=admin_object
            mngr.save()

            new_role = role()
            new_role.s_id = student
            new_role.p_id = project
            new_role.role = "Project Manager"
            new_role.save()

         #   manager = proj_mngr.objects.get(id=project.m_id)

          #  role1 = role()
           # role1.s_id =
            curr_admin = main_admin.objects.get(u_id=request.user)
            if projects.objects.filter(admin=curr_admin).exists():
                project = projects.objects.filter(admin=curr_admin)[:1].get()
                return redirect('/home/admin_home?p_id=' + str(project.id))
            else:
                return redirect('/home/admin_home?p_id=-1')

        return redirect('/home/admin_home/addproject')

class StudentHomeView(View):
    template_name = 'home.html'
    form_class = WorkForm

    def get(self, request):
        if not request.user.is_authenticated():
            return redirect('login')
        else:
            usertype=1
            form = self.form_class(request.POST)
            current_student = student.objects.get(u_id=request.user.id)
            roles = role.objects.filter(s_id=current_student)
            curr_proj_id = request.GET['p_id']
            noti = notification.objects.filter(u_id=request.user.id).order_by("-date")[:5]
            usee = User.objects.all()
            if curr_proj_id != str(-1):
                curr_proj = projects.objects.get(id=curr_proj_id)
                curr_role = role.objects.get(p_id=curr_proj,s_id=current_student)
                project_list = list()
                files = UploadModel.objects.filter(p_id=curr_proj).order_by("-date")[:4]
                for role1 in roles:
                   proj = role1.p_id
                   project_list.append(proj)
                if curr_role.role == "Team Member":
                    template_name="home.html"
                    team_obj = team_student_map.objects.filter(p_id=curr_proj, s_id=current_student )[:1].get()
                    team = team_obj.t_id
                    te = teams.objects.get(p_id = curr_proj,t_name = team)
                    print(te.t_leader)
                    work_list = work_log.objects.filter(s_id=current_student, t_id=team).order_by("-date")[:5]
                    return render(request, template_name, context={'te':te,'usertype':usertype,'project':curr_proj,'currentuser':current_student,'usee':usee,'noti':noti,'files':files , 'form' : form , 'roles':roles , 'project_list':project_list , 'work_list':work_list , 'team':team_obj , 'curr_proj':curr_proj , 'curr_role':curr_role})
                if curr_role.role == "Project Manager":
                    template_name="projectmanagerhome.html"
                    team_list = teams.objects.filter(p_id=curr_proj)
                    print(usertype)
                    print("####################")
                    return render(request, template_name , context={'usertype':usertype,'project':curr_proj,'currentuser':current_student,'usee':usee,'noti':noti,'files':files , 'form' : form ,'roles': roles, 'project_list': project_list, 'curr_proj': curr_proj, 'curr_role': curr_role , 'team_list':team_list})
                if curr_role.role == "Team Leader":
                    template_name="teamleaderhome.html"
                    leader_student = student.objects.get(u_id=request.user)
                    team = teams.objects.get(t_leader=leader_student,p_id=curr_proj)
                    work_log_list = work_log.objects.filter(t_id=team).order_by("-date")[:5]
                    print (work_log_list)
                    return render(request, template_name , context={'usertype':usertype,'project':curr_proj,'currentuser':current_student,'usee':usee,'noti':noti,'files':files , 'form' : form ,'curr_team':team ,'roles': roles, 'project_list': project_list, 'curr_proj': curr_proj, 'curr_role': curr_role  , 'work_log_list' : work_log_list  })
            else:
                    return render(request,'home.html',context={'usertype':usertype,'currentuser':current_student,'usee':usee,'noti':noti})
    def post(self,request):
        usertype=1
        form = WorkForm(request.POST)
        form_valid = form.is_valid()
        curr_proj_id = request.GET['p_id']
        if form_valid:

                current_user = request.user
                current_student = student.objects.get(u_id=current_user)
                curr_proj_id = request.GET['p_id']
                curr_proj = projects.objects.get(id=curr_proj_id)
                team_obj = team_student_map.objects.filter(p_id=curr_proj, s_id=current_student)[:1].get()
                team = team_obj.t_id
                work_log = form.save(commit=False)
                work_log.s_id = current_student
                work_log.t_id = team
                work_log.desc = form.cleaned_data['desc']
                now = datetime.datetime.now()
                print (now)
                work_log.date = now

             #   manager = proj_mngr.objects.get(id=project.m_id)

              #  role1 = role()
               # role1.s_id =

                work_log.save()

                return redirect('/home/student_home?p_id='+str(curr_proj_id))

        return redirect('/home/student_home?p_id=' + str(curr_proj_id))


class ProjectView(View):
    template_name = 'project.html'

    def get(self,request):
        if not request.user.is_authenticated():
            return redirect('login')
        else:
            p_id = request.GET['id']
            project = projects.objects.get(id=p_id)
            team_list = teams.objects.filter(p_id=project)

            return render(request, self.template_name,context={'project' : project , 'team_list':team_list})


class AddTeamView(View):
    template_name ='addteam.html'
    form_class = TeamForm
    def get(self,request):
        if not request.user.is_authenticated():
            return redirect('login')
        else:
            noti = notification.objects.filter(u_id=request.user.id).order_by("-date")[:5]
            p_id = request.GET['p_id']
            currentuser = student.objects.get(u_id=request.user.id)
            form = self.form_class(request.POST,proj=p_id)
            choices = student.objects.all()
            usertype=1
            curr_student = student.objects.get(u_id=request.user.id)
            if role.objects.filter(s_id=curr_student).exists():
                obj = role.objects.filter(s_id=curr_student)[:1].get()
                project = obj.p_id
            return render(request,self.template_name,context={'noti':noti,'usertype':usertype,'project':project,'currentuser':currentuser,'choices':choices , 'form':form})

    def post(self,request):

        p_id = request.GET['p_id']
        form = self.form_class(request.POST, proj=p_id)
        if form.is_valid():

            team = form.save(commit=False)
            team.t_name = form.cleaned_data['t_name']
            team.t_leader = form.cleaned_data['t_leader']
            curr_proj = projects.objects.get(id=p_id)
            for i in proj_mngr.objects.filter(u_id=request.user):
                curr_mngr = i
            curr_student = student.objects.get(u_id=request.user)
            team.p_id = curr_proj
            leader = team_leader()
            student_user = team.t_leader.u_id
            leader.u_id = student_user
            leader.m_id = curr_mngr
            team.save()
            leader.save()

            tsmap = team_student_map()
            tsmap.p_id = curr_proj
            tsmap.s_id = team.t_leader
            tsmap.t_id = team

            tsmap.save()

            role_obj = role()
            role_obj.role="Team Leader"
            role_obj.s_id = team.t_leader
            role_obj.p_id = curr_proj

            role_obj.save()

            return redirect('/home/student_home?p_id='+str(p_id))

        return redirect('/home/student_home/add_team?p_id=?'+str(p_id))

class AddMemberView(View):
    template_name ='addteammem.html'
    def get(self,request):
        if not request.user.is_authenticated():
            return redirect('login')
        else:
            noti = notification.objects.filter(u_id=request.user.id).order_by("-date")[:5]
            currentuser = student.objects.get(u_id=request.user.id)
            p_id = request.GET['p_id']
            curr_proj = projects.objects.get(id=p_id)
            form_class = MemberForm
            form = form_class(proj=curr_proj)
            choices = student.objects.all()
            teams_list = teams.objects.filter(p_id=p_id)
            usertype = 1
            curr_student = student.objects.get(u_id=request.user.id)
            if role.objects.filter(s_id=curr_student).exists():
                obj = role.objects.filter(s_id=curr_student)[:1].get()
                project = obj.p_id
            return render(request,self.template_name,context={'noti': noti, 'usertype': usertype, 'project': project, 'currentuser': currentuser,'choices':choices , 'form':form , 'team_list':teams_list})

    def post(self,request):
        p_id = request.GET['p_id']
        curr_proj = projects.objects.get(id=p_id)
        form_class = MemberForm
        form = form_class(request.POST , proj=curr_proj)
        if form.is_valid():

            member = form.save(commit=False)
            member.mem_id = form.cleaned_data['mem_id']
            member.u_id = member.mem_id.u_id


            team = form.cleaned_data['team']
            member.l_id = team_leader.objects.get(u_id=team.t_leader.u_id)
            member.save()
            team.t_members.add(member)



            mem_student = member.mem_id

            tsmap = team_student_map()
            tsmap.p_id = curr_proj
            tsmap.s_id = mem_student
            tsmap.t_id = team

            role_obj = role()
            role_obj.role="Team Member"
            role_obj.s_id = mem_student
            role_obj.p_id = curr_proj


            team.save()
            tsmap.save()
            role_obj.save()

            return redirect('/home/student_home?p_id='+str(p_id))

        return redirect('/home/student_home/add_member?p_id='+str(p_id))

class AddMemberAsLeaderView(View):
    template_name ='addteammemasleader.html'
    def get(self,request):
        if not request.user.is_authenticated():
            return redirect('login')
        else:
            noti = notification.objects.filter(u_id=request.user.id).order_by("-date")[:5]
            currentuser = student.objects.get(u_id=request.user.id)
            p_id = request.GET['p_id']
            t_id = request.GET['t_id']
            curr_proj = projects.objects.get(id=p_id)
            form_class = MemberForm_Leader
            form = form_class(request.POST,proj=curr_proj)
            choices = student.objects.all()
            teams_list = teams.objects.filter(p_id=p_id)
            usertype = 1
            curr_student = student.objects.get(u_id=request.user.id)
            if role.objects.filter(s_id=curr_student).exists():
                obj = role.objects.filter(s_id=curr_student)[:1].get()
                project = obj.p_id
            return render(request,self.template_name,context={'noti': noti, 'usertype': usertype, 'project': project, 'currentuser': currentuser,'choices':choices , 'form':form , 'team_list':teams_list})

    def post(self,request):
        p_id = request.GET['p_id']
        t_id = request.GET['t_id']
        curr_proj = projects.objects.get(id=p_id)
        form_class = MemberForm_Leader
        form = form_class(request.POST,proj=curr_proj)
        if form.is_valid():

            member = form.save(commit=False)
            member.mem_id = form.cleaned_data['mem_id']
            member.u_id = member.mem_id.u_id


            user = request.user

            team = teams.objects.get(id=t_id)
            member.l_id = team_leader.objects.get(u_id=team.t_leader.u_id)
            member.save()
            team.t_members.add(member)


            mem_student = member.mem_id

            tsmap = team_student_map()
            tsmap.p_id = curr_proj
            tsmap.s_id = mem_student
            tsmap.t_id = team

            role_obj = role()
            role_obj.role="Team Member"
            role_obj.s_id = mem_student
            role_obj.p_id = curr_proj


            team.save()
            tsmap.save()
            role_obj.save()

            return redirect('/home/student_home?p_id='+str(p_id))

        return redirect('/home/student_home/add_member?p_id='+str(p_id))

def upload_handler(request):
    view_url = reverse('website.views.upload_handler')
    pr_id = request.GET['p_id']
    curr_proj = projects.objects.get(id=pr_id)
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        upload_form = form.save(commit=False)
        upload_form.p_id = curr_proj
        now = datetime.datetime.now()
        upload_form.date = now

        team_member_role = role.objects.filter(p_id=curr_proj)
        mail_list = list()
        for roles in team_member_role:
            curr_student = roles.s_id
            student_user = curr_student.u_id
            student_mail = student_user.email
            mail_list.append(student_mail)
        curr_admin = curr_proj.admin
        admin_user = curr_admin.u_id
        admin_mail = admin_user.email
        mail_list.append(admin_mail)
        upload_form.save()

        user = request.user
        sender = user

        subject = 'Promanager : File Upload : ' + sender.first_name + ' ' + sender.last_name
        body = sender.first_name + ' ' + sender.last_name + ' Uploaded '+ str(upload_form.file)  + ' check now http://localhost:8000/home/login'
        email = EmailMultiAlternatives(subject, body, '', mail_list)
        email.send()
        if main_admin.objects.filter(u_id=user.id).exists():
            curr_admin = main_admin.objects.get(u_id=user)
            if projects.objects.filter(admin=curr_admin).exists():
                return redirect('/home/admin_home?p_id=' + str(curr_proj.id))
            else:
                return redirect('/home/admin_home?p_id=-1')
        else:
            curr_student = student.objects.get(u_id=user)
            if role.objects.filter(s_id=curr_student).exists():
                obj = role.objects.filter(s_id=curr_student)[:1].get()
                project = obj.p_id
                role_inst = role.objects.get(p_id=project, s_id=curr_student).role
                return redirect('/home/student_home?p_id=' + str(curr_proj.id))
            else:
                return redirect('/home/student_home?p_id=-1')
    else:
        if not request.user.is_authenticated():
            return redirect('login')
        else:
            noti = notification.objects.filter(u_id=request.user.id).order_by("-date")[:5]
            if main_admin.objects.filter(u_id=request.user.id).exists():
                usertype = 0
                curr_admin = main_admin.objects.get(u_id=request.user.id)
                if projects.objects.filter(admin=curr_admin).exists():
                    project = projects.objects.filter(admin=curr_admin)[:1].get()
                curruser = curr_admin
            else:
                usertype = 1
                curr_student = student.objects.get(u_id=request.user.id)
                if role.objects.filter(s_id=curr_student).exists():
                    obj = role.objects.filter(s_id=curr_student)[:1].get()
                    project = obj.p_id
                curruser = curr_student
            upload_url, upload_data = prepare_upload(request, view_url)
            upload_url+="?p_id="+str(pr_id)
            form = UploadForm()
            return render(request, 'simple_upload.html',{'currentuser': curruser, 'project': curr_proj, 'usertype': usertype, 'noti': noti,'form': form, 'upload_url': upload_url, 'upload_data': upload_data})


def files_view(request):
    if not request.user.is_authenticated():
        return redirect('login')
    else:
        p_id = request.GET['p_id']
        curr_proj = projects.objects.get(id=p_id)
        files = UploadModel.objects.filter(p_id=curr_proj).order_by("-date")
        noti = notification.objects.filter(u_id=request.user.id).order_by("-date")[:5]
        if main_admin.objects.filter(u_id=request.user.id).exists():
            usertype=0
            curr_admin = main_admin.objects.get(u_id=request.user.id)
            if projects.objects.filter(admin=curr_admin).exists():
                project = projects.objects.filter(admin=curr_admin)[:1].get()
            curruser = curr_admin
        else:
            usertype=1
            curr_student = student.objects.get(u_id=request.user.id)
            if role.objects.filter(s_id=curr_student).exists():
                obj = role.objects.filter(s_id=curr_student)[:1].get()
                project = obj.p_id
            curruser = curr_student
        return render(request,'files.html',context={'files':files,'currentuser':curruser,'project':curr_proj,'usertype':usertype,'noti':noti})


def download_handler(request):
    if not request.user.is_authenticated():
        return redirect('login')
    else:
        pk = request.GET['pk']
        upload = UploadModel.objects.get(id=pk)
        return serve_file(request, upload.file , save_as=True)



def send(request):
    if not request.user.is_authenticated():
        return redirect('login')
    else:
        if request.method == "POST":
            note = request.POST['note']
            user1 = request.POST['user']
            now = datetime.datetime.now()
            print("##################")
            print(now)
            print(user1)
            usee = User.objects.all()
            for pr in usee:
                print("as")
                print(pr)
                if str(pr) == str(user1):
                    x = pr
            print(note)
            noti = notification()
            noti.note = note
            noti.u_id = x
            noti.sender  = request.user
            noti.date = now
            print(noti.sender)
            noti.save()
            sender = noti.sender
            receiver = x
            rec_mail = receiver.email

            subject = 'Promanager : Message from '+sender.first_name+' '+sender.last_name
            body = 'You have a new notification from '+sender.first_name+' '+sender.last_name+' check now http://localhost:8000/home/login'
            email = EmailMultiAlternatives(subject , body , '', [rec_mail])
            email.send()


            if main_admin.objects.filter(u_id=request.user.id).exists():
                curr_admin = main_admin.objects.get(u_id=request.user.id)
                if projects.objects.filter(admin=curr_admin).exists():
                    project = projects.objects.filter(admin=curr_admin)[:1].get()
                    return redirect('/home/admin_home?p_id=' + str(project.id))
                else:
                    return redirect('/home/admin_home?p_id=-1')
            else:
                curr_student = student.objects.get(u_id=request.user.id)
                if role.objects.filter(s_id=curr_student).exists():
                    obj = role.objects.filter(s_id=curr_student)[:1].get()
                    project = obj.p_id
                    role_inst = role.objects.get(p_id=project, s_id=curr_student).role
                    return redirect('/home/student_home?p_id=' + str(project.id))
                else:
                    return redirect('/home/student_home?p_id=-1')


def notif(request):
    if not request.user.is_authenticated():
        return redirect('login')
    else:
        fl=0
        noti = notification.objects.filter(u_id=request.user.id).order_by("-date")[:5]
        if main_admin.objects.filter(u_id=request.user.id).exists():
            usertype=0
            curr_admin = main_admin.objects.get(u_id=request.user.id)
            if projects.objects.filter(admin=curr_admin).exists():
                project = projects.objects.filter(admin=curr_admin)[:1].get()
                fl = 1
            curruser = curr_admin
        else:
            usertype=1
            curr_student = student.objects.get(u_id=request.user.id)
            if role.objects.filter(s_id=curr_student).exists():
                obj = role.objects.filter(s_id=curr_student)[:1].get()
                project = obj.p_id
                fl = 1
            curruser = curr_student
        print("########")
        print(usertype)
        if fl == 1:
            return render(request,'notification.html',context={'currentuser':curruser,'project':project,'usertype':usertype,'noti':noti})
        else:
            return render(request,'notification.html',context={'currentuser':curruser,'usertype':usertype,'noti':noti})

def profile(request):
    if not request.user.is_authenticated():
        return redirect('login')
    else:
        noti = notification.objects.filter(u_id=request.user.id).order_by("-date")[:5]
        u_id = request.user.id
        user = User.objects.get(id = u_id)
        user_email = user.email
        username = user.username
        usertype = 0
        if main_admin.objects.filter(u_id=request.user.id).exists():
            curr_admin = main_admin.objects.get(u_id=request.user.id)
            curruser = curr_admin
            photo = curr_admin.photo
            if projects.objects.filter(admin=curr_admin).exists():
                project = projects.objects.filter(admin=curr_admin)[:1].get()
                return render(request, 'profile.html', context={'photo': photo, 'user_email': user_email, 'username': username,'currentuser': curruser, 'project': project, 'usertype': usertype, 'noti': noti}, context_instance=RequestContext(request))
            else:
                return render(request, 'profile.html', context={'photo': photo, 'user_email': user_email, 'username': username,'currentuser': curruser, 'usertype': usertype, 'noti': noti}, context_instance=RequestContext(request))

        else:
            usertype=1
            curr_student = student.objects.get(u_id=request.user.id)
            curruser = curr_student
            photo = curr_student.photo
            print(photo)
            if role.objects.filter(s_id=curr_student).exists():
                obj = role.objects.filter(s_id=curr_student)[:1].get()
                project = obj.p_id
                return render(request,'profile.html',context={'photo':photo,'user_email':user_email,'username':username,'currentuser':curruser,'project':project,'usertype':usertype,'noti':noti})
            else:
                return render(request,'profile.html',context={'photo':photo,'user_email':user_email,'username':username,'currentuser':curruser,'usertype':usertype,'noti':noti})

def upload_pic(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            if main_admin.objects.filter(u_id = request.user.id).exists():
                m = main_admin.objects.get(u_id=request.user.id)
            else:
                m = student.objects.get(u_id = request.user.id)
            m.photo.delete(False)
            m.photo = form.cleaned_data['image']
            m.save()
            return redirect('profile')
    return HttpResponseForbidden('allowed only via POST')


def changepass(request):
    if not request.user.is_authenticated():
        return redirect('login')
    else:
        i=0
        noti = notification.objects.filter(u_id=request.user.id).order_by("-date")[:5]
        if main_admin.objects.filter(u_id=request.user.id).exists():
            usertype=0
        else:
            usertype=1
        flag =1
        u_id = request.user.id
        user = User.objects.get(id = u_id)
        user_email = user.email
        username = user.username
        print("START")
        err = "Please try again"
        if request.method == "POST":
            newpass = request.POST['newpass']
            cpass = request.POST['cpass']
            if len(newpass) < 8:
                err = "Password length is too short. Please try again"
                flag2 = 1
            elif newpass == cpass:
                user.set_password(newpass)
                user.save()
                print("success")
                return render(request, 'changedone.html')
            else:
                print("passwords not same")
                err = "Passwords do not match"
        if usertype==0:
            curr_admin = main_admin.objects.get(u_id=request.user.id)
            curruser = curr_admin
            photo = curr_admin.photo
            print(photo)
            if projects.objects.filter(admin=curr_admin).exists():
                project = projects.objects.filter(admin=curr_admin)[:1].get()
                return render(request, 'profile.html', context={'i':i,'flag':flag,'err':err,'photo': photo, 'user_email': user_email, 'username': username,'currentuser': curruser, 'project': project, 'usertype': usertype, 'noti': noti})
            else:
                return render(request, 'profile.html', context={'i':i,'flag':flag,'err':err,'photo': photo, 'user_email': user_email, 'username': username,'currentuser': curruser, 'usertype': usertype, 'noti': noti})

        else:
            curr_student = student.objects.get(u_id=request.user.id)
            curruser = curr_student
            photo = curr_student.photo
            print(photo)
            if role.objects.filter(s_id=curr_student).exists():
                obj = role.objects.filter(s_id=curr_student)[:1].get()
                project = obj.p_id
                return render(request,'profile.html',context={'flag':flag,'err':err,'photo':photo,'user_email':user_email,'username':username,'currentuser':curruser,'project':project,'usertype':usertype,'noti':noti})
            else:
                return render(request,'profile.html',context={'flag':flag,'err':err,'photo':photo,'user_email':user_email,'username':username,'currentuser':curruser,'usertype':usertype,'noti':noti})


def del_team(request):
    if not request.user.is_authenticated():
        return redirect('login')
    else:
        t_id = request.GET['t_id']
        p_id = request.GET['p_id']
        curr_team = teams.objects.get(id=t_id)
        curr_proj = projects.objects.get(id=p_id)
        for member in curr_team.t_members.all():
            curr_student = member.mem_id
            curr_role = role.objects.get(s_id=curr_student,p_id=curr_proj)
            member.delete()
            curr_role.delete()

        curr_leader =curr_team.t_leader
        curr_leader_user = curr_leader.u_id
        curr_lead_role = role.objects.get(s_id=curr_leader,p_id=curr_proj)
        curr_lead_role.delete()
        leader_inst = team_leader.objects.get(u_id=curr_leader_user)
        leader_inst.delete()
        tsmap = team_student_map.objects.filter(t_id=curr_team)
        tsmap.delete()

        curr_team.delete()

        return redirect('/home/student_home?p_id='+str(p_id))

def del_team_mem(request):
    if not request.user.is_authenticated():
        return redirect('login')
    else:
        t_id = request.GET['t_id']
        p_id = request.GET['p_id']
        mem_id = request.GET['mem_id']
        curr_team = teams.objects.get(id=t_id)
        curr_proj = projects.objects.get(id=p_id)
        curr_member = team_member.objects.get(id=mem_id)
        curr_student = curr_member.mem_id
        curr_role = role.objects.get(s_id=curr_student,p_id=curr_proj)
        curr_role.delete()
        tsmap = team_student_map.objects.filter(t_id=curr_team,s_id=curr_student)
        tsmap.delete()

        curr_member.delete()
        curr_team.t_members.remove(curr_member)

        return redirect('/home/student_home?p_id='+str(p_id))


class delproj(View):
    template_name='delproj.html'
    def get(self,request):
        if not request.user.is_authenticated():
            return redirect('login')
        else:
            noti = notification.objects.filter(u_id=request.user.id).order_by("-date")[:5]
            curr_admin = main_admin.objects.get(u_id=request.user.id)
            if projects.objects.filter(admin=curr_admin).exists():
                project=projects.objects.filter(admin=curr_admin)[:1].get()
                proj=projects.objects.filter(admin=curr_admin)
                return render(request,self.template_name,context={'noti':noti,'proj':proj,'currentuser':curr_admin,'project':project})
            else:
                return render(request,self.template_name,context={'noti':noti,'currentuser':curr_admin})

    def post(self,request):
        pro = request.POST['project1']
        aa = projects.objects.get(p_name=pro)
        curr_admin = main_admin.objects.get(u_id=request.user)
        proj_mngr_stud = aa.m_id
        proj_mngr_user = proj_mngr_stud.u_id
        curr_proj_mngr = proj_mngr.objects.get(u_id=proj_mngr_user,admin=curr_admin)
        curr_proj_mngr.delete()

        aa.delete()
        curr_admin = main_admin.objects.get(u_id=request.user)
        if projects.objects.filter(admin=curr_admin).exists():
            project = projects.objects.filter(admin=curr_admin)[:1].get()
            return redirect('/home/admin_home?p_id=' + str(project.id))
        else:
            return redirect('/home/admin_home?p_id=-1')

        return redirect('/home/admin_home/addproject')

