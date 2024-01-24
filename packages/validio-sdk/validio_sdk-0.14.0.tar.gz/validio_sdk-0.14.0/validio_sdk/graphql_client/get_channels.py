from datetime import datetime
from typing import Annotated, Any, List, Literal, Optional, Union

from pydantic import Field

from .base_model import BaseModel


class GetChannels(BaseModel):
    channels: List[
        Annotated[
            Union[
                "GetChannelsChannelsChannel",
                "GetChannelsChannelsSlackChannel",
                "GetChannelsChannelsWebhookChannel",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class GetChannelsChannelsChannel(BaseModel):
    typename__: Literal["Channel"] = Field(alias="__typename")
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    notification_rules: List["GetChannelsChannelsChannelNotificationRules"] = Field(
        alias="notificationRules"
    )


class GetChannelsChannelsChannelNotificationRules(BaseModel):
    id: Any
    name: str


class GetChannelsChannelsSlackChannel(BaseModel):
    typename__: Literal["SlackChannel"] = Field(alias="__typename")
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    notification_rules: List[
        "GetChannelsChannelsSlackChannelNotificationRules"
    ] = Field(alias="notificationRules")
    config: "GetChannelsChannelsSlackChannelConfig"


class GetChannelsChannelsSlackChannelNotificationRules(BaseModel):
    id: Any
    name: str


class GetChannelsChannelsSlackChannelConfig(BaseModel):
    webhook_url: str = Field(alias="webhookUrl")
    timezone: Optional[str]
    application_link_url: str = Field(alias="applicationLinkUrl")


class GetChannelsChannelsWebhookChannel(BaseModel):
    typename__: Literal["WebhookChannel"] = Field(alias="__typename")
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    notification_rules: List[
        "GetChannelsChannelsWebhookChannelNotificationRules"
    ] = Field(alias="notificationRules")
    config: "GetChannelsChannelsWebhookChannelConfig"


class GetChannelsChannelsWebhookChannelNotificationRules(BaseModel):
    id: Any
    name: str


class GetChannelsChannelsWebhookChannelConfig(BaseModel):
    webhook_url: str = Field(alias="webhookUrl")
    application_link_url: str = Field(alias="applicationLinkUrl")
    auth_header: Optional[str] = Field(alias="authHeader")


GetChannels.model_rebuild()
GetChannelsChannelsChannel.model_rebuild()
GetChannelsChannelsChannelNotificationRules.model_rebuild()
GetChannelsChannelsSlackChannel.model_rebuild()
GetChannelsChannelsSlackChannelNotificationRules.model_rebuild()
GetChannelsChannelsSlackChannelConfig.model_rebuild()
GetChannelsChannelsWebhookChannel.model_rebuild()
GetChannelsChannelsWebhookChannelNotificationRules.model_rebuild()
GetChannelsChannelsWebhookChannelConfig.model_rebuild()
