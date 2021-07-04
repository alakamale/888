class Events:
    def __init__(self, name, slug, active, event_type, sport_Name, status,
                 scheduled_Start, actual_Start):
        self.name = name
        self.slug = slug
        self.active = active
        self.event_type = event_type
        self.sport_Name = sport_Name
        self.status = status
        self.scheduled_Start = scheduled_Start
        self.actual_Start = actual_Start
