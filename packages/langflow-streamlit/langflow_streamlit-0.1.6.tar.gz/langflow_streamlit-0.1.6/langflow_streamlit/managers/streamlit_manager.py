import os
import threading
import subprocess
from langflow_streamlit.utils.process_utils import check_if_port_is_used_by_program, kill_process_on_port
from langflow_streamlit.utils import settings

class StreamlitManager:
    port = settings.STREAMLIT_PORT
    path = settings.FOLDER_PATH

    @classmethod
    def __load_streamlit(cls):
        if not os.path.exists(f"{cls.path}streamlit.py"):
            with open(f"{cls.path}streamlit.py", "w") as file:
                file.write("import streamlit as st")
        else:
            with open(f"{cls.path}streamlit.py", "r+") as file:
                content = file.read()
                if len(content) < 10:
                    file.seek(0)
                    file.write("import streamlit as st\nfrom time import sleep\nwhile True:\n    sleep(2)")
                    file.truncate()

    @classmethod
    def run_streamlit(cls, args):
        command = f"streamlit run {cls.path}streamlit.py --browser.serverPort {cls.port} --server.port {cls.port} --server.headless true {args}"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            raise Exception(f"Streamlit startup failed. Error: {stderr.decode()}")

    @classmethod
    def start(cls, args="--server.headless false"):
        if check_if_port_is_used_by_program(cls.port, ["streamlit"]):
            kill_process_on_port(cls.port)
        cls.__load_streamlit()
        streamlit_thread = threading.Thread(target=cls.run_streamlit, args=(args,))
        streamlit_thread.start()

    @classmethod
    def restart(cls):
        kill_process_on_port(cls.port)
        cls.start("--server.headless true")
