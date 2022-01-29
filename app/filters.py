from sqlalchemy import exists, and_

from app import db
from app.models import Team, Member, Announcement, Activity, TeamActivities, File, TeamFiles, TeamAnnouncements


def filter_simple_view(member_id):
    entities = {}
    member = Member.query.get_or_404(member_id)
    for team in member.teams:
        entities[team.name] = team.members

    return entities


def filter_by_team(filter_args, teams, entities_type):
    entities = {}

    if filter_args is None:
        entities['All'] = []
        # Select all entities that are not specifically related to a team and the related ones.
        if entities_type == 'activities':
            entities['All'].extend(db.session.query(Activity).filter(~exists().where(and_(Activity.id == TeamActivities.activity_id))).all())
            for team in teams:
                entities['All'].extend(team.activities)
        elif entities_type == 'announcements':
            entities['All'].extend(db.session.query(Announcement).filter(~exists().where(and_(Announcement.id == TeamAnnouncements.announcement_id))).all())
            for team in teams:
                entities['All'].extend(team.announcements)
        elif entities_type == 'files':
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
    teams = []

    if not has_permission:
        teams = member.teams
        entities = filter_by_team(filter_args, teams, entities_type)
    else:
        # teams = Team.query.all()
        if entities_type == 'activities':
            teams = db.session.query(Team).filter(exists().where(and_(Team.id == TeamActivities.team_id))).all()
        if entities_type == 'announcements':
            teams = db.session.query(Team).filter(exists().where(and_(Team.id == TeamAnnouncements.team_id))).all()
        if entities_type == 'files':
            teams = db.session.query(Team).filter(exists().where(and_(Team.id == TeamFiles.team_id))).all()
        entities = filter_by_team(filter_args, teams, entities_type)

    return entities, teams


def has_access(entity, member_id, member_roles, required_roles):
    # If member has not access to all the entities, check the team
    if not [i for i in member_roles if i in required_roles]:
        # If announcement is specific for one or more teams, check the member's teams
        if entity.teams:
            member = Member.query.get_or_404(int(member_id))
            if not [i for i in member.teams if i in entity.teams]:
                return False
    return True
