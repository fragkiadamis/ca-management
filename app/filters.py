from sqlalchemy import select, exists, and_

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
            entities['All'].extend(db.session.query(File).filter(~exists().where(and_(File.id == TeamFiles.activity_id))).all())
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
    else:
        team = [t for t in teams if t.id == int(entity_id)][0]
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


def filter_entities():
    """asd"""


def get_related_entities(filter_args, member, permissions, entities_type):
    member_roles_set = set([r.name for r in member.roles])
    has_permission = True if len(member_roles_set.intersection(permissions)) else False

    if not has_permission:
        teams = member.teams
        entities = filter_by_team(filter_args, teams, entities_type)
    else:
        teams = Team.query.all()
        entities = filter_by_team(filter_args, teams, entities_type)

    return entities, teams
