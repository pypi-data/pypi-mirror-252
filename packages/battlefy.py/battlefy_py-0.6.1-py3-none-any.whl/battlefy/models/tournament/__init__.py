from typing import List, Optional
from datetime import datetime
from dateutil import parser
from .stage import Stage
from .team import Team


class Contact:
    type: str
    details: str

    def __init__(self, data: dict) -> None:
        self.type = data.get("type", "")
        self.details = data.get("details", "")


class TournamentCustomField:
    name: str
    public: bool
    id: str

    def __init__(self, data: dict) -> None:
        self.name = data.get("name")
        self.public = data.get("public")
        self.id = data.get("_id")


class EmailsSent:
    one_day: bool
    now: bool
    pending_team_notification: bool

    def __init__(self, data: dict) -> None:
        self.one_day = data.get("oneDay")
        self.now = data.get("now")
        self.pending_team_notification = data.get("pendingTeamNotification")

class Rules:
    complete: str
    critical: str

    def __init__(self, data: dict) -> None:
        self.complete = data.get("complete", "")
        self.critical = data.get("critical", "")


class Tournament:
    id: str
    start_time: Optional[datetime]
    rules: Rules
    players_per_team: int
    custom_fields: List[TournamentCustomField]
    user_can_report: bool
    name: str
    about: str
    banner_url: str
    contact: Contact
    contact_details: str
    prizes: str
    schedule: str
    check_in_required: bool
    check_in_starts: int
    type: str
    has_max_players: bool
    has_registration_cap: bool
    team_cap: int
    max_players: int
    country_flags_on_brackets: bool
    has_points: bool
    is_published: bool
    service_fee_percent: int
    game_name: str
    is_featured: bool
    is_public: bool
    is_suspended: bool
    is_roster_locked: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    check_in_start_time: Optional[datetime]
    slug: str
    cloned_from_tournament_id: str
    registration_enabled: bool
    emails_sent: EmailsSent
    organization_id: str
    game_id: str
    stage_ids: List[str]
    last_completed_match_at: Optional[datetime]
    template_id: str

    teams: List[Team]
    stages: List[Stage]

    def __init__(self, data: dict):
        self.id = data.get("_id")
        if "startTime" in data:
            self.start_time = parser.isoparse(data.get("startTime"))
        self.rules = Rules(data.get("rules", {}))
        self.players_per_team = data.get("playersPerTeam")
        self.custom_fields = [TournamentCustomField(x) for x in data.get("customFields")]
        self.user_can_report = data.get("userCanReport")
        self.name = data.get("name")
        self.about = data.get("about")
        self.banner_url = data.get("bannerUrl")
        self.contact = Contact(data.get("contact", {}))
        self.contact_details = data.get("contactDetails")
        self.prizes = data.get("prizes")
        self.schedule = data.get("schedule")
        self.check_in_required = data.get("checkInRequired")
        self.check_in_starts = data.get("checkInStarts")
        self.type = data.get("type")
        self.has_max_players = data.get("hasMaxPlayers")
        self.has_registration_cap = data.get("hasRegistrationCap")
        self.team_cap = data.get("teamCap")
        self.max_players = data.get("maxPlayers")
        self.country_flags_on_brackets = data.get("countryFlagsOnBrackets")
        self.has_points = data.get("hasPoints")
        self.is_published = data.get("isPublished")
        self.service_fee_percent = data.get("serviceFeePercent")
        self.game_name = data.get("gameName")
        self.is_featured = data.get("isFeatured")
        self.is_public = data.get("isPublic")
        self.is_suspended = data.get("isSuspended")
        self.is_roster_locked = data.get("isRosterLocked")
        if "createdAt" in data:
            self.created_at = parser.isoparse(data.get("createdAt"))
        if "updatedAt" in data:
            self.updated_at = parser.isoparse(data.get("updatedAt"))
        if "checkInStartTime" in data:
            self.check_in_start_time = parser.isoparse(data.get("checkInStartTime"))
        self.slug = data.get("slug")
        self.cloned_from_tournament_id = data.get("clonedFromTournamentID")
        self.registration_enabled = data.get("registrationEnabled")
        self.emails_sent = EmailsSent(data.get("emailsSent", {}))
        self.organization_id = data.get("organizationID")
        self.game_id = data.get("gameID")
        self.stage_ids = data.get("stageIDs")
        if "lastCompletedMatchAt" in data:
            self.last_completed_match_at = parser.isoparse(data.get("lastCompletedMatchAt"))
        self.template_id = data.get("templateID")
        stages_data = data.get("stages", [])
        self.stages = []
        for stage_data in stages_data:
            self.stages.append(Stage(stage_data))
        self.teams = []

    def add_stage(self, stage: Stage):
        self.stages.append(stage)

    def add_teams(self, data: List[dict]):
        for team_data in data:
            self.teams.append(Team(team_data))

    def get_team_from_team_id(self, team_id: str) -> Team:
        for team in self.teams:
            if team.id == team_id:
                return team
        return None

    def get_team_from_persistent_team_id(self, persistent_team_id: str) -> Team:
        for team in self.teams:
            if team.persistent_team_id == persistent_team_id:
                return team
        return None

    def get_player_from_persistent_player_id(self, persistent_player_id: str):
        for team in self.teams:
            for player in team.players:
                if player.persistent_player_id == persistent_player_id:
                    return player
        return None




