from sqlalchemy import exists, and_

from app import db
from app.models import Team, Member, Announcement, Activity, TeamActivities, File, TeamFiles, TeamAnnouncements, MemberTeams, Department, Role, MemberRoles, Treasury, Transaction


def filter_members(filter_args, all_members, teams, roles, departments, schools, has_permission):
    members_list = {}

    if filter_args is None or filter_args == 'current':
        members_list['Current'] = [m for m in all_members if m.is_active]
        for key in members_list:
            members_list[key].sort(key=lambda e: e.create_date, reverse=True)
        return members_list

    filter_args = filter_args.split('_')
    entity_filter = filter_args[0]
    entity_id = None
    if len(filter_args) > 1:
        entity_id = filter_args[1]

    if not entity_id:
        if entity_filter == 'role':
            for role in roles:
                members_list[role.name] = [m for m in all_members if role in m.roles and m.is_verified]
        elif entity_filter == 'status' and has_permission:
            members_list['Active'] = [m for m in all_members if m.is_active and m.is_verified]
            members_list['Inactive'] = [m for m in all_members if not m.is_active and m.is_verified]
        elif entity_filter == 'team':
            for team in teams:
                members_list[team.name] = [m for m in all_members if team in m.teams and m.is_verified]
        elif entity_filter == 'school':
            for school in schools:
                members_list[school.name] = [m for m in all_members if m.department.school.name == school.name and m.is_verified]
        elif entity_filter == 'department':
            for department in departments:
                members_list[department.name] = [m for m in all_members if m.department.name == department.name and m.is_verified]
        elif entity_filter == 'pending' and has_permission:
            members_list['Pending'] = [m for m in all_members if not m.is_verified]
        elif entity_filter == 'active' and has_permission:
            members_list['Active'] = [m for m in all_members if m.is_active and m.is_verified]
        elif entity_filter == 'inactive' and has_permission:
            members_list['Inactive'] = [m for m in all_members if not m.is_active and m.is_verified]
        else:
            members_list = {'Current': Member.query.filter(Member.is_verified == 1, Member.is_active == 1).all()}
    elif entity_id and entity_id.isnumeric():
        entity_id = int(entity_id)
        if entity_filter == 'role':
            role = [r for r in roles if r.id == entity_id][0]
            members_list[role.name] = [m for m in all_members if role in m.roles and m.is_verified]
        elif entity_filter == 'team':
            team = [t for t in teams if t.id == entity_id][0]
            members_list[team.name] = [m for m in team.members if m.is_verified]
        elif entity_filter == 'school':
            school = [s for s in schools if s.id == entity_id][0]
            members_list[school.name] = [m for m in all_members if school == m.department.school and m.is_verified]
        elif entity_filter == 'department':
            department = [d for d in departments if d.id == entity_id][0]
            members_list[department.name] = [m for m in all_members if department == m.department and m.is_verified]
        else:
            members_list = {'Current': Member.query.filter(Member.is_verified == 1, Member.is_active == 1).all()}

    # Sort by creation date
    for key in members_list:
        members_list[key].sort(key=lambda e: e.create_date, reverse=True)

    return members_list


def filter_treasuries(filter_args, treasuries):
    entities = []

    if filter_args is None:
        entities = [['Total Amount', 0, []]]
        for treasury in treasuries:
            entities[0][1] += treasury.amount
            entities[0][2] = Transaction.query.all()
            entities[0][2].sort(key=lambda e: e.create_date, reverse=True)

        return entities

    filter_args = filter_args.split('_')
    treasury_filter = filter_args[0]
    entity_id = None
    if len(filter_args) > 1:
        entity_id = filter_args[1]

    if not entity_id:
        if treasury_filter == 'treasury':
            for treasury in treasuries:
                entities.append([treasury.name, treasury.amount, treasury.transactions])
        elif treasury_filter == 'type':
            transactions = {}
            all_transactions = []
            for treasury in treasuries:
                all_transactions.extend(treasury.transactions)
            for transaction in all_transactions:
                if transaction.type not in transactions:
                    transactions[transaction.type] = [transaction]
                else:
                    transactions[transaction.type].append(transaction)
            for key in transactions:
                type_total_amount = 0
                for transaction in transactions[key]:
                    type_total_amount += transaction.amount
                entities.append([key, type_total_amount, transactions[key]])
    elif entity_id and entity_id.isnumeric():
        entity_id = int(entity_id)
        if treasury_filter == 'treasury':
            treasury = [t for t in treasuries if t.id == entity_id][0]
            entities.append([treasury.name, treasury.amount, treasury.transactions])

    for entity in entities:
        entity[2].sort(key=lambda e: e.create_date, reverse=True)
    return entities


def filter_entities(filter_args, teams, entities_type):
    entities = {}

    if filter_args is None:
        entities['All'] = []
        if entities_type == 'activities':
            # Select all entities that are not specifically related to a team and the related ones.
            entities['All'].extend(db.session.query(Activity).filter(~exists().where(and_(Activity.id == TeamActivities.activity_id))).all())
            for team in teams:
                entities['All'].extend(team.activities)
        elif entities_type == 'announcements':
            # Select all entities that are not specifically related to a team and the related ones.
            entities['All'].extend(db.session.query(Announcement).filter(~exists().where(and_(Announcement.id == TeamAnnouncements.announcement_id))).all())
            for team in teams:
                entities['All'].extend(team.announcements)
        elif entities_type == 'files':
            # Select all entities that are not specifically related to a team and the related ones.
            entities['All'].extend(db.session.query(File).filter(~exists().where(and_(File.id == TeamFiles.file_id))).all())
            for team in teams:
                entities['All'].extend(team.files)

        entities['All'].sort(key=lambda e: e.create_date, reverse=True)
        return entities

    filter_args = filter_args.split('_')
    entity_filter = filter_args[0]
    entity_id = None
    if len(filter_args) > 1:
        entity_id = filter_args[1]

    if not entity_id:
        entities['Common'] = []
        if entities_type == 'activities':
            # Select all entities that are not specifically related to a team and the related ones.
            entities['Common'].extend(db.session.query(Activity).filter(~exists().where(and_(Activity.id == TeamActivities.activity_id))).all())
            if entity_filter == 'team':
                for team in teams:
                    entities[team.name] = team.activities
        elif entities_type == 'announcements':
            # Select all entities that are not specifically related to a team and the related ones.
            entities['Common'].extend(db.session.query(Announcement).filter(~exists().where(and_(Announcement.id == TeamAnnouncements.announcement_id))).all())
            if entity_filter == 'team':
                for team in teams:
                    entities[team.name] = team.announcements
        if entities_type == 'files':
            # Select all entities that are not specifically related to a team and the related ones.
            entities['Common'].extend(db.session.query(File).filter(~exists().where(and_(File.id == TeamFiles.file_id))).all())
            if entity_filter == 'team':
                for team in teams:
                    entities[team.name] = team.files
    elif entity_id.isnumeric():
        filtered_list = list(filter(lambda t: t.id == int(entity_id), teams))
        team = filtered_list[0] if len(filtered_list) else None
        if team:
            if entities_type == 'activities':
                entities[team.name] = team.activities
            elif entities_type == 'announcements':
                entities[team.name] = team.announcements
            elif entities_type == 'files':
                entities[team.name] = team.files

    # Sort by creation date
    for key in entities:
        entities[key].sort(key=lambda e: e.create_date, reverse=True)

    return entities


def get_related_entities(filter_args, member, permissions, entities_type):
    member_roles_set = set([r.name for r in member.roles])
    has_permission = True if len(member_roles_set.intersection(permissions)) else False
    entities = []
    teams = []
    schools = []
    departments = []
    roles = []

    if not has_permission:
        if entities_type == 'members':
            teams = member.teams
            all_members = []
            for team in teams:
                all_members.extend(team.members)
            # Remove duplicates by casting the list into a dictionary and then back to a list
            all_members = list(dict.fromkeys(all_members))
            for member in all_members:
                roles.extend(member.roles)
                departments.append(member.department)
                schools.append(member.department.school)

            roles = list(dict.fromkeys(roles))
            departments = list(dict.fromkeys(departments))
            schools = list(dict.fromkeys(schools))

            entities = filter_members(filter_args, all_members, teams, roles, departments, schools, has_permission)
        elif entities_type == 'treasuries':
            teams = [t.treasury for t in member.teams if t.treasury.transactions]
            if not filter_args:
                filter_args = 'treasury'
            entities = filter_treasuries(filter_args, teams)
        else:
            teams = member.teams
            entities = filter_entities(filter_args, teams, entities_type)
        return entities, teams, departments, schools, roles
    else:
        if entities_type == 'members':
            # Get all teams with related members
            teams = db.session.query(Team).filter(exists().where(and_(Team.id == MemberTeams.team_id))).all()
            all_members = []
            for team in teams:
                all_members.extend(team.members)
            # Remove duplicates by casting the list into a dictionary and then back to a list
            all_members = list(dict.fromkeys(all_members))

            # Get departments, schools and roles with related members
            roles = db.session.query(Role).filter(exists().where(and_(Role.id == MemberRoles.role_id))).all()
            departments = db.session.query(Department).filter(exists().where(and_(Member.department_id == Department.id))).all()
            schools = [d.school for d in departments]
            entities = filter_members(filter_args, all_members, teams, roles, departments, schools, has_permission)
        else:
            if entities_type == 'activities':
                teams = db.session.query(Team).filter(exists().where(and_(Team.id == TeamActivities.team_id))).all()
                entities = filter_entities(filter_args, teams, entities_type)
            elif entities_type == 'announcements':
                teams = db.session.query(Team).filter(exists().where(and_(Team.id == TeamAnnouncements.team_id))).all()
                entities = filter_entities(filter_args, teams, entities_type)
            elif entities_type == 'files':
                teams = db.session.query(Team).filter(exists().where(and_(Team.id == TeamFiles.team_id))).all()
                entities = filter_entities(filter_args, teams, entities_type)
            elif entities_type == 'treasuries':
                teams = Treasury.query.filter(Treasury.transactions).all() # Actually get the team treasuries that have transactions
                entities = filter_treasuries(filter_args, teams)

    return entities, teams, departments, schools, roles


def has_access(entity, member_id, member_roles, required_roles):
    # If member has not access to all the entities, check the team
    if not [i for i in member_roles if i in required_roles]:
        # If announcement is specific for one or more teams, check the member's teams
        if entity.teams:
            member = Member.query.get_or_404(int(member_id))
            if not [i for i in member.teams if i in entity.teams]:
                return False
    return True
