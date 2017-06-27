from django import template
from website.models import *

register = template.Library()

@register.filter("get_team_leader")
def get_team_leader(value , team):
    team_leader = team.t_leader
    leader_user = team_leader.u_id
    return leader_user.first_name
