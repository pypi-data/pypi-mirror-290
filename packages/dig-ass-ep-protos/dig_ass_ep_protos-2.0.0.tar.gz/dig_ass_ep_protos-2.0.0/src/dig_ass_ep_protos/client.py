from dig_ass_ep_protos.DigitalAssistantEntryPoint_pb2_grpc import (
    DigitalAssistantEntryPointStub,
)
from dig_ass_ep_protos.DigitalAssistantEntryPoint_pb2 import (
    DigitalAssistantEntryPointRequest,
    DigitalAssistantEntryPointResponse,
    OuterContextItem,
)

from agi_med_protos.abstract_client import AbstractClient


class EntryPointClient(AbstractClient):
    def __init__(self, address) -> None:
        super().__init__(address)
        self._stub = DigitalAssistantEntryPointStub(self._channel)

    def __call__(self, text: str, outer_context: dict, image=None, pdf=None):
        request = DigitalAssistantEntryPointRequest(
            Text=text,
            OuterContext=OuterContextItem(
                Sex=outer_context['Sex'],
                Age=outer_context['Age'],
                UserId=outer_context['UserId'],
                SessionId=outer_context['SessionId'],
                ClientId=outer_context['ClientId'],
            ),
            Image=image,
            PDF=pdf,
        )
        response: DigitalAssistantEntryPointResponse = self._stub.GetTextResponse(request)
        return response.Text
