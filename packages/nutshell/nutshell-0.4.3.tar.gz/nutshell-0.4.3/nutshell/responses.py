from nutshell.entities import User, Team, ActivityType, AnalyticsReport, Stageset, Milestone, Lead, Activity

from pydantic import BaseModel


class _APIResponse(BaseModel):
    """Base class for all API responses."""
    result: list[BaseModel] | BaseModel | bool


class FindUsersResult(_APIResponse):
    result: list[User]


class GetUserResult(_APIResponse):
    result: User


class FindTeamsResult(_APIResponse):
    result: list[Team]


class FindActivityTypesResult(_APIResponse):
    result: list[ActivityType]


class GetAnalyticsReportResult(_APIResponse):
    result: AnalyticsReport


class FindStagesetsResult(_APIResponse):
    result: list[Stageset]


class FindMilestonesResult(_APIResponse):
    result: list[Milestone]


class FindLeadsResult(_APIResponse):
    result: list[Lead]


class FindActivitiesResult(_APIResponse):
    result: list[Activity]


class NewActivityResult(_APIResponse):
    result: Activity


class GetActivityResult(_APIResponse):
    result: Activity


class EditActivityResult(_APIResponse):
    result: Activity


class DeleteActivityResult(_APIResponse):
    result: bool
