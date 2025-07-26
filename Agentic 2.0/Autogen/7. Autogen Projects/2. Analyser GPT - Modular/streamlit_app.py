import streamlit as st
import asyncio
import os

from teams.analyzer_gpt import getDataAnalyzerTeam
from models.openai_model_client import get_model_client
from config.docker_util import getDockerCommandLineExecutor,start_docker_container,stop_docker_container
from autogen_agentchat.messages import TextMessage



st.title('Analyser GPT- Digital Data Analyzer') 

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])


task = st.chat_input("Enter your task here...")


async def run_analyser_gpt(docker,openai_model_client,task):
    try:
        await start_docker_container(docker)
        team = getDataAnalyzerTeam(docker,openai_model_client)

        async for message in team.run_stream(task=task):
            st.markdown(f"**{message}")

        return None
    except Exception as e:
        st.error(f"Error: {e}")
        return e
    finally:   
        await stop_docker_container(docker)


if task:
   if uploaded_file is not None: 
        
        if not os.path.exists('temp'):
            os.makedirs('temp', exist_ok=True)
   
        with open('temp/data.csv','wb') as f:
            f.write(uploaded_file.getbuffer())

        openai_model_client= get_model_client()
        docker = getDockerCommandLineExecutor()

        error = asyncio.run(run_analyser_gpt(docker,openai_model_client,task))

        if error:
            st.error('An error occured:',{error})
        
   
   else:
       st.warning('Please upload the file and provide the task')

else:
    st.warning('Please provide the task')