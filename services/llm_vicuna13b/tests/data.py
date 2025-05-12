from pydantic.v1 import BaseModel
import regex
from services_api.llm_vicuna13b import Vicuna13BRequest, Vicuna13BResponse

reg = regex.compile(r"[^\s\w\punct\d_\-]")


class TestCase(BaseModel):
    name: str
    request: Vicuna13BRequest
    response: Vicuna13BResponse
    response_comparator: object = lambda checked_response, target_response: reg.sub(
        "", target_response.text
    ) in reg.sub("", checked_response.text)


hlp_prompt = """A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. 
USER: Imagine, you are an intelligent assistant that helps me divide household tasks into subgoals, which will be executed by the warehouse robot step-by-step. The warehouse robot can put boxes on different shelves in storage rack. To clarify the task, I will provide a list of objects that are used in it. If you get it, reply with the message "Waiting for next input." Understood? 
ASSISTANT: Understood. Waiting for next input.
</s>USER: Put a big black box from the table to the second shelf from the top. List of items to use in the task: 
ASSISTANT: 1. put a big black box from the table to the second shelf from the top
2. done.
</s>USER: Put all the boxes from the floor to the third shelf from the bottom. List of items to use in the task: box 1, box 2, box 3, box 4, box 5 
ASSISTANT: 1. put box 1 from floor to the third shelf from the bottom.
2. put box 2 from floor to the third shelf from the bottom.
3. put box 3 from floor to the third shelf from the bottom.
4. put box 4 from floor to the third shelf from the bottom.
5. put box 5 from floor to the third shelf from the bottom.
6. done.
</s>USER: Take cupboard box from the floor and put it on the top shelf, then take small plastic container from third shelf from top and place it on a fouth shelf from top. List of items to use in the task: 
ASSISTANT: 1. Take cupboard box from the floor.
2. put cupboard box on the top shelf
3. take small plastic container from third shelf from top and place it on a fouth shelf from top.
5. done.
</s>USER: Grab a container from bottom shelf and put in on the floor. List of items to use in the task:  
ASSISTANT: 1. grab a container from bottom shelf and put it on the floor.
2. done.
</s>USER: Take all the plastic containers from the storage rack and place them on the table. List of items to use in the task: plastic container 1, plastic container 2 
ASSISTANT: 1. take plastic container 1 from the storage rack and place it on the table.
2. take plastic container 2 from the storage rack and place it on the table.
3. done.
"""

test_cases = [
    TestCase(
        name="1.hlp: 1 action",
        request=Vicuna13BRequest(
            prompt=hlp_prompt
            + "</s>USER:"
            + "pick up box 73 from shelf 41"
            + "List of items to use in the task: box 73"
            + "\nASSISTANT:"
        ),
        response=Vicuna13BResponse(
            text="""1. pick up box 73 from shelf 41
2. done."""
        ),
    ),
    TestCase(
        name="2.hlp: 1 action",
        request=Vicuna13BRequest(
            prompt=hlp_prompt
            + "</s>USER:"
            + "put box 1 on shelf 15"
            + "List of items to use in the task: box 1"
            + "\nASSISTANT:"
        ),
        response=Vicuna13BResponse(
            text="""1. put box 1 on shelf 15
2. done."""
        ),
    ),
    TestCase(
        name="3.hlp: 2 actions",
        request=Vicuna13BRequest(
            prompt=hlp_prompt
            + "</s>USER:"
            + "take box 8 from shelf 2 and place it on shelf 9, then pick up box 1 from shelf 10"
            + "List of items to use in the task: box 8, box 1"
            + "\nASSISTANT:"
        ),
        response=Vicuna13BResponse(
            text="""1. take box 8 from shelf 2 and place it on shelf 9
2. pick up box 1 from shelf 10
3. done."""
        ),
    ),
    TestCase(
        name="4.hlp: 2 actions",
        request=Vicuna13BRequest(
            prompt=hlp_prompt
            + "</s>USER:"
            + "take box 80 from shelf 3 and place it on shelf 43, then take box 56 from shelf 100 and place it on shelf 99"
            + "List of items to use in the task: box 80, box 56"
            + "\nASSISTANT:"
        ),
        response=Vicuna13BResponse(
            text="""1. take box 80 from shelf 3 and place it on shelf 43
2. take box 56 from shelf 100 and place it on shelf 99
3. done."""
        ),
    ),
    TestCase(
        name="5.hlp: 2 actions",
        request=Vicuna13BRequest(
            prompt=hlp_prompt
            + "</s>USER:"
            + "take box 7 from shelf 13 and place it on shelf 14, then take box 100 from shelf 21 and place it on shelf 27, and then take box 17 from shelf 1 and place it on shelf 89"
            + "List of items to use in the task: box 7, box 100, box 17"
            + "\nASSISTANT:"
        ),
        response=Vicuna13BResponse(
            text="""1. take box 7 from shelf 13 and place it on shelf 14
2. take box 100 from shelf 21 and place it on shelf 27
3. take box 17 from shelf 1 and place it on shelf 89
4. done."""
        ),
    ),
]


test_cases = {test_case.name: test_case for test_case in test_cases}
