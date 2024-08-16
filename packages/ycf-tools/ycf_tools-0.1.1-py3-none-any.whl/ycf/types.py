from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class Context(BaseModel):
    class TokenContext(BaseModel):
        access_token: str
        expires_in: int
        token_type: str

    token: TokenContext
    aws_request_id: str
    deadline_ms: int
    function_name: str
    function_version: str
    invoked_function_arn: str
    log_group_name: str
    log_stream_name: str
    memory_limit_in_mb: int
    request_id: str


class HttpRequest(BaseModel):
    class Context(BaseModel):
        class Identity(BaseModel):
            source_ip: str = Field(alias='sourceIp')
            user_agent: str = Field(alias='userAgent')

        identity: Identity
        http_method: str = Field(alias='httpMethod')
        request_id: str = Field(alias='requestId')
        request_time: str = Field(alias='requestTime')
        request_time_epoch: int = Field(alias='requestTimeEpoch')

    request_context: Context = Field(alias='requestContext')
    http_method: str = Field(alias='httpMethod')
    headers: dict[str, str]
    path: str
    multi_value_headers: dict[str, list[str]] = Field(alias='multiValueHeaders')
    query_string_parameters: dict[str, str] = Field(default_factory=dict, alias='queryStringParameters')
    multi_value_query_string_parameters: dict[str, list[str]] = Field(
        default_factory=dict,
        alias='multiValueQueryStringParameters',
    )
    is_base64_encoded: bool = Field(alias='isBase64Encoded')
    body: str


class AliceSkillRequest(BaseModel):

    class MetaModel(BaseModel):
        class InterfacesModel(BaseModel):
            account_linking: dict[str, str] = {}
            payments: dict[str, str] = {}
            screen: dict[str, str] = {}

        interfaces: InterfacesModel
        client_id: str
        locale: str
        timezone: str

    class RequestModel(BaseModel):
        class MarkupModel(BaseModel):
            dangerous_context: bool

        class NluModel(BaseModel):
            entities: list[dict[str, str]]
            tokens: list[str]
            intents: dict[str, str]

        nlu: NluModel
        markup: MarkupModel
        original_utterance: str
        command: str
        type: str

    class SessionModel(BaseModel):
        class UserModel(BaseModel):
            user_id: str

        class ApplicationModel(BaseModel):
            application_id: str

        user: UserModel
        application: ApplicationModel
        message_id: int
        new: bool
        session_id: str
        skill_id: str
        user_id: str

    class StateModel(BaseModel):
        session: dict[str, str]
        user: dict[str, str]
        application: dict[str, str]

    meta: MetaModel
    request: RequestModel
    session: SessionModel
    state: StateModel
    version: str


class MessagesQueueRequest(BaseModel):
    class MessageEvent(BaseModel):
        class Details(BaseModel):
            class Message(BaseModel):
                class MessageAttribute(BaseModel):
                    class MessageAttributes(BaseModel):
                        data_type: str = Field(..., alias='dataType')
                        string_value: str = Field(..., alias='stringValue')

                    message_attribute_key: MessageAttributes = Field(..., alias='messageAttributeKey')

                message_id: UUID
                md5_of_body: str
                body: str
                attributes: dict[str, str]
                message_attributes: MessageAttribute
                md5_of_message_attributes: str

            message: Message
            queue_id: str

        class EventMetadata(BaseModel):
            event_id: UUID
            event_type: str
            created_at: datetime

        event_metadata: EventMetadata
        details: Details

    messages: list[MessageEvent]
