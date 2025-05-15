from eventer.api.user.views import user_router
from eventer.api.event.views import event_router
from eventer.api.team.views import team_router
from eventer.api.team_members.views import team_members_router
from eventer.api.city.views import city_router
from eventer.api.organization.views import organization_router
from eventer.api.event_members.views import event_members_router
from eventer.api.stage.views import stage_router
from eventer.api.event_day.views import eventdays_router
from eventer.api.event_teams.views import event_teams_router
from eventer.api.stage_team_transitions.views import stage_team_transitions_router
from eventer.api.stage_score.views import stage_score_router
from eventer.api.score_details.views import score_details_router
from eventer.api.certificate.views import certificate_router
from eventer.api.document.views import document_router
from eventer.api.leaderboard.views import leaderboard_router
from eventer.api.parameters.views import parameter_router

__all__ = (
    user_router,
    event_router,
    team_router,
    team_members_router,
    city_router,
    organization_router,
    event_members_router,
    stage_router,
    eventdays_router,
    event_teams_router,
    stage_team_transitions_router,
    stage_score_router,
    score_details_router,
    certificate_router,
    document_router,
    leaderboard_router,
    parameter_router 
)