from __future__ import annotations

from enum import StrEnum, IntEnum
from typing import Optional

from pydantic import BaseModel, computed_field, Field


class AnalyticsReportType(StrEnum):
    """
    Enum for the type of analytics report to generate.

    Attributes
    ----------
    EFFORT : Effort report.
    PIPELINE : Pipeline report.
    """
    EFFORT = "Effort"
    PIPELINE = "Pipeline"


class FindLeadsQueryStatus(IntEnum):
    """
    Enum for the status of a lead.

    Attributes
    ----------
    OPEN : Open status.
    CANCELLED : Cancelled status.
    LOST : Lost status.
    WON : Won status.
    """
    OPEN = 0
    CANCELLED = 12
    LOST = 11
    WON = 10


class FindLeadsQueryFilter(IntEnum):
    """
    Enum for the filter to apply to the leads query.

    ...
    Attributes
    ----------
    MY_LEADS : My leads filter.
    MY_TEAM_LEADS : My team leads filter.
    ALL_LEADS : All leads filter.
    """
    MY_LEADS = 0
    MY_TEAM_LEADS = 1
    ALL_LEADS = 2


class ActivityStatus(IntEnum):
    """
    Enum for the status of an activity.

    ...
    Attributes
    ----------
    SCHEDULED : Scheduled status.
    LOGGED : Logged status.
    CANCELLED : Cancelled status.
    OVERDUE: Overdue status.
    """
    SCHEDULED = 0
    LOGGED = 1
    CANCELLED = 2
    OVERDUE = -1


class User(BaseModel):
    """
    Represents a user in the Nutshell API.

    ...
    Attributes
    ----------
    stub : bool
        Whether the user info is a stub.
    id : int
        The id of the User object.
    entity_type : str
        The entity type (Users).
    rev : str
        The revision of the User object.
    name : str
        The name of the user.
    first_name : str
        The first name of the user.
    last_name : str
        The last name of the user.
    is_enabled : bool
        Whether the user is enabled.
    is_administrator : bool
        Whether the user is an administrator.
    emails : list[str]
        The emails associated with the user.
    modified_time : str
        The time of last modification of the user.
    created_time : str
        The time the user was created.
    """
    stub: bool = None
    id: int
    entity_type: str = Field(..., alias="entityType", pattern=r"Users")
    rev: str
    name: str
    first_name: str = Field(None, alias="firstName")
    last_name: str = Field(None, alias="lastName")
    is_enabled: bool = Field(..., alias="isEnabled")
    is_administrator: bool = Field(..., alias="isAdministrator")
    emails: list[str]
    modified_time: str = Field(..., alias="modifiedTime")
    created_time: str = Field(..., alias="createdTime")


class Team(BaseModel):
    """
    Represents a team object from the Nutshell API.

    ...
    Attributes
    ----------
    stub : bool
        Whether the team info is a stub.
    id : int
        The id of the Team object.
    name : str
        The name of the team.
    rev : str
        The revision of the Team object.
    entity_type : str
        The entity type (Teams).
    modified_time : str
        The time of last modification of the team.
    created_time : str
        The time the team was created.
    """
    stub: bool
    id: int
    name: str
    rev: str
    entity_type: str = Field(..., alias="entityType", pattern=r"Teams")
    modified_time: str = Field(..., alias="modifiedTime")
    created_time: str = Field(..., alias="createdTime")


class ActivityType(BaseModel):
    """
    Represents an activity type object from the Nutshell API.

    ...
    Attributes
    ----------
    stub : bool
        Whether the activity type info is a stub.
    id : int
        The id of the ActivityType object.
    rev : str
        The revision of the ActivityType object.
    entity_type : str
        The entity type (Activity_Types).
    name : str
        The name of the activity type.
    """
    stub: bool
    id: int
    rev: str
    entity_type: str = Field(..., alias="entityType", pattern=r"Activity_Types")
    name: str
    deleted_time: Optional[str] = Field(None, alias="deletedTime")


class TimeSeriesData(BaseModel):
    """
    Represents the time series data for an analytics report response.

    ...
    Attributes
    ----------
    total_effort : list[list[int]]
        The total effort data.
    successful_effort : list[list[int]]
        Only the successful effort data.
    """
    total_effort: list[list[int]]
    successful_effort: list[list[int]]


class SummaryData(BaseModel):
    """
    Represents the summary data for an analytics report response.

    ...
    Attributes
    ----------
    sum : float
        The sum value.
    avg : float
        The average value.
    min : float
        The minimum value.
    max : float
        The maximum value.
    sum_delta : float
        The sum delta value.
    avg_delta : float
        The average delta value.
    min_delta : float
        The minimum delta value.
    max_delta : float
        The maximum delta value.
    """
    sum: float
    avg: float
    min: float
    max: float
    sum_delta: float
    avg_delta: float
    min_delta: float
    max_delta: float


class AnalyticsReport(BaseModel):
    """
    Represents an analytics report response from the Nutshell API.

    ...
    Attributes
    ----------
    series_data : TimeSeriesData
        The time series data.
    summary_data : dict[str, SummaryData]
        The summary data.
    period_description : str
        The human-readable period description.
    delta_period_description : str
        The human-readable delta period description.
    """
    series_data: TimeSeriesData = Field(..., alias="seriesData")
    summary_data: dict[str, SummaryData] = Field(..., alias="summaryData")
    period_description: str = Field(..., alias="periodDescription")
    delta_period_description: str = Field(..., alias="deltaPeriodDescription")


class Stageset(BaseModel):
    """
    Represents a stageset object from the Nutshell API.

    ...
    Attributes
    ----------
    id : int
        The id of the Stageset object.
    entity_type : str
        The entity type (Stagesets).
    name : str
        The name of the stageset.
    default : int
        The default value.
    position : int
        The position value.
    """
    id: int
    entity_type: str = Field(..., alias="entityType", pattern=r"Stagesets")
    name: str
    default: Optional[int] = None
    position: Optional[int] = None


class Milestone(BaseModel):
    """
    Represents a milestone object from the Nutshell API.

    ...
    Attributes
    ----------
    id : int
        The id of the Milestone object.
    entity_type : str
        The entity type (Milestones).
    rev : str
        The revision of the Milestone object.
    name : str
        The name of the milestone.
    position : int
        The position value.
    stageset_id : int
        The stageset id.
    """
    id: int
    entity_type: str = Field(..., alias="entityType", pattern=r"Milestones")
    rev: str
    name: str
    position: Optional[int] = None
    stageset_id: Optional[int] = Field(None, alias="stagesetId")


class Lead(BaseModel):
    """
    Represents a lead object from the Nutshell API.

    ...
    Attributes
    ----------
    stub : bool
        Whether the lead info is a stub.
    id : int
        The id of the Lead object.
    entity_type : str
        The entity type (Leads).
    rev : str
        The revision of the Lead object.
    name : str
        The name of the lead.

    """
    stub: Optional[bool] = None
    id: int
    entity_type: str = Field(..., alias="entityType", pattern=r"Leads")
    rev: str
    name: str
    html_url: Optional[str] = Field(None, alias="htmlUrl")
    tags: Optional[list[str]] = None
    description: str
    created_time: Optional[str] = Field(None, alias="createdTime")
    creator: Optional[User] = None
    milestone: Optional[Milestone] = None
    stageset: Optional[Stageset] = None
    status: int
    confidence: Optional[int] = None
    assignee: Optional[User | Team] = None
    due_time: Optional[str] = Field(None, alias="dueTime")
    value: Optional[dict[str, float | str]] = 0
    normalized_value: Optional[dict[str, float | str]] = Field(None, alias="normalizedValue")
    products: Optional[list[dict]] = None
    primary_account: Optional[dict] = Field(None, alias="primaryAccount")


class Activity(BaseModel):
    """
    Represents an activity object from the Nutshell API.

    ...
    Attributes
    ----------
    id : int
        The id of the Activity object.
    entity_type : str
        The entity type (Activities).
    rev : str
        The revision of the Activity object.
    name : str
        The name of the activity.
    description : str
        The description of the activity.
    activity_type : ActivityType
        The activity type.
    lead : Lead
        The lead associated with the activity.
    leads : list[Lead]
        The leads associated with the activity.
    start_time : str
        The start time of the activity.
    end_time : str
        The end time of the activity.
    is_all_day : bool
        Whether the activity is all day.
    is_flagged : bool
        Whether the activity is flagged.
    status : int
        The status of the activity.
    log_description : str
        The log description of the activity.
    log_note : dict
        The log note of the activity.
    logged_by : dict[str, str | int]
        The user who logged the activity.
    participants : list
        The participants of the activity.
    follow_up : dict
        The follow up of the activity.
    follow_up_to : dict
        The follow up to of the activity.
    deleted_time : str
        The time the activity was deleted.
    modified_time : str
        The time the activity was last modified.
    created_time : str
        The time the activity was created.

    """
    id: int
    stub: Optional[bool] = None
    entity_type: str = Field(..., alias="entityType", pattern=r"Activities")
    rev: str
    name: str
    description: Optional[str] = None
    activity_type: ActivityType = Field(None, alias="activityType")
    lead: Optional[Lead] = None
    leads: Optional[list[Lead]] = None
    start_time: str = Field(..., alias="startTime")
    end_time: str = Field(..., alias="endTime")
    is_all_day: bool = Field(..., alias="isAllDay")
    is_flagged: bool = Field(..., alias="isFlagged")
    status: int
    log_description: Optional[str] = Field(None, alias="logDescription")
    log_note: Optional[dict] = Field(None, alias="logNote")
    logged_by: Optional[dict[str, str | int | list]] = Field(None, alias="loggedBy")
    participants: Optional[list] = None
    follow_up: Optional[Activity] = Field(None, alias="followUp")
    follow_up_to: Optional[Activity] = Field(None, alias="followUpTo")
    deleted_time: Optional[str] = Field(None, alias="deletedTime")
    modified_time: str = Field(..., alias="modifiedTime")
    created_time: str = Field(..., alias="createdTime")


class CreateActivity(BaseModel):
    """
    Minimal class for creating an activity in the Nutshell API. serialization_alias used as this class should only be
    used to create a new activity.
    
    ...
    Attributes:
        name : str
            The name of the activity.
        description : str
            The description of the activity.
        activity_type_id : int
            The activity type id.
        leads : list[Lead]
            The leads associated with the activity.
        start_time : str
            The start time of the activity.
        end_time : str
            The end time of the activity.
        is_all_day : bool
            Whether the activity is all day.
        is_flagged : bool
            Whether the activity is flagged.
        status : int
            The status of the activity.
        participants : list
            The participants of the activity.
    """

    name: str = None
    description: str = None
    activity_type_id: int = Field(None, serialization_alias="activityTypeId")
    leads: Optional[list[Lead]] = None
    start_time: str = Field(..., serialization_alias="startTime")
    end_time: str = Field(..., serialization_alias="endTime")
    is_all_day: Optional[bool] = Field(None, serialization_alias="isAllDay")
    is_flagged: Optional[bool] = Field(None, serialization_alias="isFlagged")
    status: Optional[int] = None
    participants: Optional[list] = None


class FindLeadsQuery(BaseModel):
    """
    For building a valid query for the findLeads method.

    ...
    Attributes:
        status : FindLeadsQueryStatus
            The status of the leads.
        filter : FindLeadsQueryFilter
            The filter to apply to the leads query.
        milestone_id : int
            The milestone id.
        milestone_ids : list[int]
            The milestone ids.
        stageset_id : int
            The stageset id.
        stageset_ids : list[int]
            The stageset ids.
        due_time : str
            The due time of the leads.
        assignee : list[User | Team]
            The assignee of the leads.
        number : int
            The number of leads.

    Computed Attributes:
        query : dict
            A correctly formed query dictionsary for the findLeads method.
    """
    status: Optional[FindLeadsQueryStatus] = None
    filter: Optional[FindLeadsQueryFilter] = None
    milestone_id: Optional[int] = None
    milestone_ids: Optional[list[int]] = None
    stageset_id: Optional[int] = None
    stageset_ids: Optional[list[int]] = None
    due_time: Optional[str] = None
    assignee: Optional[list[User | Team]] = None
    number: Optional[int] = None

    @computed_field
    @property
    def query(self) -> dict:
        query_dict = {}

        if isinstance(self.status, FindLeadsQueryStatus):
            query_dict["status"] = self.status.value
        if isinstance(self.filter, FindLeadsQueryFilter):
            query_dict["filter"] = self.filter.value
        if self.milestone_id:
            query_dict["milestoneId"] = self.milestone_id
        if self.milestone_ids:
            query_dict["milestoneIds"] = self.milestone_ids
        if self.stageset_id:
            query_dict["stagesetId"] = self.stageset_id
        if self.stageset_ids:
            query_dict["stagesetIds"] = self.stageset_ids
        if self.due_time:
            query_dict["dueTime"] = self.due_time
        if self.assignee:
            query_dict["assignee"] = [
                {"entityType": entity.entity_type, "id": entity.id} for entity in self.assignee
            ]
        if self.number:
            query_dict["number"] = self.number

        return query_dict


class FindActivitiesQuery(BaseModel):
    """
    For building a valid query for the findActivities method.

    ...
    Attributes
    ----------
    lead_id:
        An optional lead ID that the activity is associated with
    contact_id:
        An optional array of contact IDs who are participants in the activity
    account_id:
        An optional array of account IDs who are participants in the activity
    user_id:
        An optional array of user IDs who are participants in the activity
    status:
        An optional ActivityStatus enum value
    activity_type_id:
        An optional array of activity type IDs
    is_flagged:
        An optional boolean for filtering by the "Important" flag
    start_time:
        An optional date or time to compare against the start time, prefixed by a comparison operator (either "<", ">", "=", ">=", or "<=").
    end_time:
        An optional date or time to compare against the end time, prefixed by a comparison operator (either "<", ">", "=", ">=", or "<=").
    """
    lead_id: Optional[int] = None
    contact_id: Optional[list[int]] = None
    account_id: Optional[list[int]] = None
    user_id: Optional[list[int]] = None
    status: Optional[ActivityStatus] = None
    activity_type_id: Optional[list[int]] = None
    is_flagged: Optional[bool] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None

    @computed_field
    @property
    def query(self) -> dict:
        query_dict = {}

        if self.lead_id:
            query_dict["leadId"] = self.lead_id
        if self.contact_id:
            query_dict["contactId"] = self.contact_id
        if self.account_id:
            query_dict["accountId"] = self.account_id
        if self.user_id:
            query_dict["userId"] = self.user_id
        if isinstance(self.status, ActivityStatus):
            query_dict["status"] = self.status.value
        if self.activity_type_id:
            query_dict["activityTypeId"] = self.activity_type_id
        if self.is_flagged:
            query_dict["isFlagged"] = self.is_flagged
        if self.start_time:
            query_dict["startTime"] = self.start_time
        if self.end_time:
            query_dict["endTime"] = self.end_time

        return query_dict
