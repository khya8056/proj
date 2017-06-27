from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


#
ROLE_CHOICES = (
    ('Team Member' , 'TM'),
    ('Team Leader' , 'TL'),
    ('Project Manager' , 'PM')
)

def get_name(self):
    return self.first_name+" "+self.last_name

User.add_to_class("__str__", get_name)

class main_admin(models.Model):
    u_id = models.ForeignKey(User)
    photo = models.FileField(blank=True)

    def __str__(self):
        user = self.u_id
        name = user.first_name+" "+user.last_name
        return name


class student(models.Model):
    u_id = models.ForeignKey(User)
    photo = models.FileField(blank=True)
    def __str__(self):
        user = self.u_id
        name = user.first_name+" "+user.last_name
        return name

class proj_mngr(models.Model):
    u_id=models.ForeignKey(User)
    m_id = models.CharField(max_length=250,blank=True)
    admin = models.ForeignKey(main_admin)

    def __str__(self):
        user = self.u_id
        name = user.first_name+" "+user.last_name
        return name


class projects(models.Model):
    p_id = models.CharField(max_length=250,blank=True)
    m_id = models.ForeignKey(student)
    admin = models.ForeignKey(main_admin,blank=True)
    p_name = models.CharField(max_length=250)

    def __str__(self):
        return self.p_name

class role(models.Model):
    s_id = models.ForeignKey(student)
    p_id = models.ForeignKey(projects)
    role = models.CharField(max_length=250,choices=ROLE_CHOICES)



class team_leader(models.Model):
    u_id = models.ForeignKey(User)
    l_id = models.CharField(max_length=250)
    m_id = models.ForeignKey(proj_mngr)


    def __str__(self):
        user = self.u_id
        name = user.first_name+" "+user.last_name
        return name

class team_member(models.Model):
    u_id = models.ForeignKey(User,blank=True)
    mem_id = models.ForeignKey(student)
    l_id = models.ForeignKey(team_leader,blank=True)

    def __str__(self):
        user = self.u_id
        name = user.first_name+" "+user.last_name
        return name


class teams(models.Model):
    t_id = models.CharField(max_length=250,blank=True)
    t_leader = models.ForeignKey(student)
    t_members = models.ManyToManyField(team_member,blank=True)
    p_id = models.ForeignKey(projects,blank=True)
    t_name = models.CharField(max_length=250)

    def __str__(self):
        return self.t_name

class work_log(models.Model):
    w_id = models.CharField(max_length=250 , blank=True)
    s_id = models.ForeignKey(student , blank=True)
    t_id = models.ForeignKey(teams, default="0" , blank=True)
    date = models.DateTimeField(default=datetime.now,blank=True)
    desc = models.CharField(max_length=1000)

    def __str__(self):
        return self.desc


class team_student_map(models.Model):
    t_id= models.ForeignKey(teams)
    s_id= models.ForeignKey(student)
    p_id=models.ForeignKey(projects)

class UploadModel(models.Model):
    file = models.FileField(upload_to='uploads/cms')
    p_id = models.ForeignKey(projects, blank="True")
    date = models.DateTimeField(default=datetime.now,blank=True)


class notification(models.Model):
    u_id = models.ForeignKey(User)
    note = models.CharField(max_length=1000,blank=True)
    sender = models.CharField(max_length=100,blank=True)
    date = models.DateTimeField(default=datetime.now,blank=True)
    valid = models.IntegerField(default=1,blank=True)
    def __str__(self):
        sender = self.sender
        receiver = self.u_id
        date = self.date
        name = sender+" to "+str(receiver)+" on "+str(date)
        return name