from autogen_agentchat.agents import CodeExecutorAgent
import asyncio
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

async def main():

    docker = DockerCommandLineCodeExecutor(
        work_dir='/tmp',
        timeout=120
    )