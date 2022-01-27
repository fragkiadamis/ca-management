from app.models import Team


def filter_entities(filter_args, all_entities, teams):
    entities = {}

    if filter_args is None:
        entities['All'] = all_entities
        return entities

    filter_args = filter_args.split('_')
    entity_filter = filter_args[0]
    entity_id = None
    if len(filter_args) > 1:
        entity_id = filter_args[1]

    if not entity_id:
        if entity_filter == 'common':
            entities['Common'] = [e for e in all_entities if not len(e.teams)]
        elif entity_filter == 'team':
            # Find all the common activities
            entities['Common'] = [e for e in all_entities if not e.teams]
            # Check type of elements in list and get respective list from teams
            if all(str(n) == 'Activity' for n in all_entities):
                for team in teams:
                    entities[team.name] = team.activities
            elif all(str(n) == 'Announcement' for n in all_entities):
                for team in teams:
                    entities[team.name] = team.announcements
            elif all(str(n) == 'File' for n in all_entities):
                for team in teams:
                    entities[team.name] = team.files
    elif entity_filter == 'team':
        team = Team.query.get_or_404(entity_id)
        # Check type of elements in list and get respective list from teams
        if all(str(n) == 'Activity' for n in all_entities):
            entities[team.name] = team.activities
        elif all(str(n) == 'Announcement' for n in all_entities):
            entities[team.name] = team.announcements
        elif all(str(n) == 'File' for n in all_entities):
            entities[team.name] = team.files

    return entities
