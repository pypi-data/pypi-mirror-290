SYSTEM_MESSAGE = """"""

from tools import list_files, write_to_file, read_from_file, run_command, view_image
from agent import Agent

agent = Agent(
    model_name="gpt-4o-2024-08-06",
    temperature=0.7,
    system_message=SYSTEM_MESSAGE,
    tools=[list_files, write_to_file, read_from_file, run_command, view_image],
)
