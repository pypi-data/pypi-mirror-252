import json

from langchain.prompts import SystemMessagePromptTemplate

from llm_prompting_gen.models.prompt_engineering import PromptEngineeringMessages, PromptElements


def test_data_class_initialising():
    """Test if we can init a templates class based on some test json files"""
    for file_name in ["sentiment", "kindergartner"]:
        # Test loading json
        pe_messages = PromptEngineeringMessages.from_json(f"templates/{file_name}.json")
        # Test creating chat prompt template
        pe_messages.get_chat_prompt_template()


def test_few_shot_string_examples():
    """Test if examples can be provided without human ai interaction"""
    prompt_elements = PromptElements(examples=["positive", "negative", "neutral"])
    prompt_messages = PromptEngineeringMessages.from_pydantic(prompt_elements)
    example_msg = prompt_messages.messages["examples"][0]
    assert type(example_msg) == SystemMessagePromptTemplate
    assert "Example 1: positive" in example_msg.format().content
    assert "Example 2: negative" in example_msg.format().content
    assert "Example 3: neutral" in example_msg.format().content

def test_order_prompt_engineering_messages_by_json():
    """Test whether the order of the original local json file is retained"""
    # test file has a different order compared to PromptElements fields
    file_path = "tests/test_templates/order_test.json"
    prompt_messages = PromptEngineeringMessages.from_json(file_path)
    with open(file_path, "r") as fp:
        message_dict = json.load(fp)
    expected_pe_messages_order = list(message_dict.keys())

    # Test if original json order is retained, after instance creation
    assert expected_pe_messages_order == list(prompt_messages.messages.keys())


