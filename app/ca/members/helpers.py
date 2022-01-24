from app.models import Member, Roles, Team, School, Department


def filter_members(filter_args):
    all_members = Member.query.filter(Member.is_verified == 1).all()
    roles = Roles.query.all()
    teams = Team.query.all()
    schools = School.query.all()
    departments = Department.query.all()

    members_list = {}
    if filter_args is None:
        return {'Current': Member.query.filter(Member.is_verified == 1, Member.is_active == 1).all()}, roles, teams, schools, departments

    filter_args = filter_args.split('_')
    member_filter = filter_args[0]
    entity_id = None
    if len(filter_args) > 1:
        entity_id = filter_args[1]

    if not entity_id:
        if member_filter == 'role':
            for role in roles:
                members_list[role.name] = [m for m in all_members if role in m.roles]
        elif member_filter == 'status':
            members_list['Active'] = [m for m in all_members if m.is_active]
            members_list['Inactive'] = [m for m in all_members if not m.is_active]
        elif member_filter == 'team':
            for team in teams:
                members_list[team.name] = [m for m in all_members if team in m.teams]
        elif member_filter == 'school':
            for school in schools:
                members_list[school.name] = [m for m in all_members if m.department.school.name == school.name]
        elif member_filter == 'department':
            for department in departments:
                members_list[department.name] = [m for m in all_members if m.department.name == department.name]
        else:
            members_list = {'Current': Member.query.filter(Member.is_verified == 1, Member.is_active == 1).all()}
    elif entity_id and entity_id.isnumeric():
        entity_id = int(entity_id)
        if member_filter == 'role':
            role = [r for r in roles if r.id == entity_id][0]
            members_list[role.name] = [m for m in all_members if role in m.roles]
        elif member_filter == 'team':
            team = [t for t in teams if t.id == entity_id][0]
            members_list[team.name] = team.members
        elif member_filter == 'school':
            school = [s for s in schools if s.id == entity_id][0]
            members_list[school.name] = [m for m in all_members if school == m.department.school]
        elif member_filter == 'department':
            department = [d for d in departments if d.id == entity_id][0]
            members_list[department.name] = [m for m in all_members if department == m.department]
        else:
            members_list = {'Current': Member.query.filter(Member.is_verified == 1, Member.is_active == 1).all()}

    return members_list, roles, teams, schools, departments
