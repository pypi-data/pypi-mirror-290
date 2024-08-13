"""The local AI toolbar to hook up with the server-side reflex agent."""

import os

import httpx
import reflex as rx
from anthropic.types import ToolUseBlock
from flexai.message import Message, ToolUseMessage
from reflex_ai.selection import ClickSelectionState
from reflex_ai.local_agent import (
    get_agent,
    InternRequest,
    InternResponse,
    ToolRequestResponse,
)


def make_request(
    endpoint: str,
    data: dict,
    url: str = os.getenv("FLEXGEN_BACKEND_URL", "http://localhost:8000"),
    timeout: int = 60,
) -> dict:
    """Make a request to the backend.

    Args:
        endpoint: The endpoint to send the request to.
        data: The data to send.
        url: The URL of the backend.
        timeout: The timeout for the request.

    Returns:
        The JSON response from the backend.
    """
    resp = httpx.post(
        f"{url}/api/{endpoint}",
        data=data,
        timeout=timeout,
    )
    print(resp)
    print(resp.json())
    resp.raise_for_status()
    return resp.json()


class ToolbarState(rx.State):
    """The toolbar state."""

    processing: bool = False
    selected_id: str = ""
    code: str = ""
    prompt: str = ""

    async def process(self, prompt: dict[str, str]):
        """Process the user's prompt.

        Args:
            prompt: The prompt from the user from the form input.
        """
        # Set the processing flag to True.
        self.processing = True
        yield

        # Get the selected code.
        selection_state = await self.get_state(ClickSelectionState)
        selected_code = "\n".join(selection_state._selected_code)

        # Create the intern request.
        request = InternRequest(
            prompt=prompt["prompt"],
            selected_code=selected_code,
            selected_module=selection_state.selected_module,
            selected_function=selection_state.selected_function,
        )
        response = make_request("intern", request.model_dump_json())
        resp_obj = InternResponse(**response)
        messages = [Message(role=m.role, content=m.content) for m in resp_obj.messages]

        # Process the messages with the local agent.
        local_intern = get_agent()
        unconverted_messages = []

        # Run in a loop until we're done with the request.
        while True:
            # Get any tool use messages from the intern and process them.
            tool_response_messages = []
            for message in messages:
                try:
                    tool_use_message = local_intern.llm.to_tool_use_message(
                        ToolUseBlock.parse_raw(message.content),
                    )
                except ValueError:
                    unconverted_messages.append(message)
                    continue
                # Invoke the tool and get the response.
                tool_response_messages.append(
                    await local_intern.invoke_tool(tool_use_message)
                )

            # Base case: no more messages to process.
            if not tool_response_messages:
                break

            # Send the tool response to the intern.
            tool_response_request = ToolRequestResponse(
                request_id=resp_obj.request_id,
                messages=tool_response_messages,
            )
            response = make_request(
                "intern/tool_response", tool_response_request.model_dump_json()
            )
            messages = [Message(**m) for m in response]

        self.processing = False


def toolbar() -> rx.Component:
    return rx.hstack(
        rx.cond(
            ToolbarState.processing,
            rx.spinner(size="3", color="white"),
        ),
        rx.form(
            rx.input(name="prompt", disabled=ToolbarState.processing),
            on_submit=ToolbarState.process,
            reset_on_submit=True,
        ),
    )


def playground(page) -> rx.Component:
    return rx.vstack(
        page(),
        rx.box(
            toolbar(),
            width="100%",
            bottom="0",
        ),
        rx.code_block(ClickSelectionState.code),
        min_height="100vh",
    )
