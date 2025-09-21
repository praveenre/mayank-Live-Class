import logging
import os

# get current working directory
cwd = os.getcwd()
print(f"Current working directory: {cwd}")

# always create log file in current working directory
log_file = os.path.join(cwd, "agent.log")

logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    filemode="a"  # append mode
)

logger = logging.getLogger(__name__)

from google.adk.agents.llm_agent import Agent

logger.info("Logger initialized. Writing to %s", log_file)




root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
