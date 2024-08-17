import logging
from typing import Any

import pydantic

from ycf.exceptions import MultiBaseException
from ycf.types import AliceSkillRequest, Context, HttpRequest, HttpResponse, MessagesQueueRequest

logger = logging.getLogger('ycf')


class YcfServer(object):
    def __init__(self) -> None:
        pass

    async def __call__(self, event: dict[str, Any], context: object) -> Any:
        if isinstance(context, dict):
            context_obj = Context.model_validate(context)

        else:
            context_obj = Context.model_validate(context.__dict__)

        validation_exs: list[BaseException] = []

        try:
            obj = HttpRequest.model_validate(event)
            logger.info('Handled data for http_request_handler. Executing')
            response = await self.http_request_handler(context_obj, obj)

            if isinstance(response, HttpResponse):
                return response

            if isinstance(response, str):
                return HttpResponse(200, body=response)

            if isinstance(response, dict):
                return HttpResponse(200, data=response)

            raise RuntimeError(f'Undefined response type: {type(response),__name__} - {response}')

        except pydantic.ValidationError as ex:
            validation_exs.append(ex)

        try:
            obj = AliceSkillRequest.model_validate(event)
            logger.info('Handled data for alice_skill_handler. Executing')
            return await self.alice_skill_handler(context_obj, obj)

        except pydantic.ValidationError as ex:
            validation_exs.append(ex)

        try:
            obj = MessagesQueueRequest.model_validate(event)
            logger.info('Handled data for queue_messages_handler. Executing')
            return await self.queue_messages_handler(context_obj, obj)

        except pydantic.ValidationError as ex:
            validation_exs.append(ex)

        raise MultiBaseException('We were unable to parse event data', validation_exs)

    async def http_request_handler(
        self,
        context: Context,
        request: HttpRequest,
    ) -> str | dict[str, Any] | None:
        logger.error(f'An unexpected HttpRequest was received: {request}')

    async def alice_skill_handler(
        self,
        context: Context,
        request: AliceSkillRequest,
    ) -> str | dict[str, Any] | None:
        logger.error(f'An unexpected AliceSkillRequest was received: {request}')

    async def queue_messages_handler(
        self,
        context: Context,
        request: MessagesQueueRequest,
    ) -> str | dict[str, Any] | None:
        logger.error(f'An unexpected MessagesQueueRequest was received: {request}')
