import streamlit as st
import json
import time
import os
import pathlib
import tempfile
import codecs
import subprocess
import sys

from model.Configuration import Configuration
from src.Cso import Cso
from src.SimulatedAnnealing import SimulatedAnnealing
from src.HTMLOutput import HtmlOutput

def main():
    st.set_page_config(layout="wide")
    st.title("Genetic Class Scheduler")

    # Sidebar for inputs
    st.sidebar.header("Configuration")

    # --- 1. File Upload ---
    st.sidebar.subheader("Input Data")
    uploaded_file = st.sidebar.file_uploader("Upload Input.json", type=['json'])
    
    if uploaded_file is not None:
        # To read file as string:
        string_data = uploaded_file.getvalue().decode("utf-8")
        input_data = json.loads(string_data)
    else:
        with open("Input.json", 'r') as f:
            input_data = json.load(f)
    
    st.sidebar.text_area("JSON Input", json.dumps(input_data, indent=2), height=250)


    # --- 2. Algorithm Selection ---
    st.sidebar.subheader("Algorithm Selection")
    alg_name = st.sidebar.selectbox("Choose Algorithm", ["Cuckoo Search (CSO)", "Simulated Annealing (SA)"])

    # --- 3. Hyperparameter Tuning ---
    st.sidebar.subheader("Hyperparameters")
    
    params = {}
    if alg_name == "Cuckoo Search (CSO)":
        params['numberOfCrossoverPoints'] = st.sidebar.slider("Number of Crossover Points", 1, 10, 2)
        params['mutationSize'] = st.sidebar.slider("Mutation Size", 1, 10, 2)
        params['crossoverProbability'] = st.sidebar.slider("Crossover Probability", 0, 100, 80)
        params['mutationProbability'] = st.sidebar.slider("Mutation Probability", 0, 100, 3)
        params['maxIterations'] = st.sidebar.number_input("Max Iterations", 1, 50000, 5000)
    elif alg_name == "Simulated Annealing (SA)":
        params['temperature'] = st.sidebar.number_input("Initial Temperature", 1, 10000, 1000)
        params['cooling_rate'] = st.sidebar.slider("Cooling Rate", 0.001, 0.1, 0.003, step=0.001, format="%.3f")
        params['max_iterations'] = st.sidebar.number_input("Max Iterations", 1, 50000, 5000)

    # --- 4. Run Button ---
    if st.sidebar.button("Generate Schedule"):
        
        # Write the current json to a temporary file to be used by the configuration parser
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json', encoding='utf-8') as tmp:
            json.dump(input_data, tmp)
            temp_file_name = tmp.name

        run_scheduler(temp_file_name, alg_name, params)
        os.remove(temp_file_name)


def run_scheduler(json_path, alg_name, params):
    st.header("Results")
    
    with st.spinner("Generating schedule... Please wait."):
        start_time = int(round(time.time() * 1000))

        # We need to get the relative path for the configuration parser
        file_name = "/" + os.path.basename(json_path)
        absolute_path = str(pathlib.Path(json_path).parent.absolute())
        
        configuration = Configuration()
        configuration.parseFile(absolute_path + file_name)

        if alg_name == "Cuckoo Search (CSO)":
            alg = Cso(configuration, **params)
        elif alg_name == "Simulated Annealing (SA)":
            alg = SimulatedAnnealing(configuration, **params)

        alg.run()
        
        html_result = HtmlOutput.getResult(alg.result)

        seconds = (int(round(time.time() * 1000)) - start_time) / 1000.0
        
        st.subheader("Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Final Fitness", f"{alg.result.fitness:.6f}")
        col2.metric("Execution Time", f"{seconds:.2f}s")
        if alg_name == "Cuckoo Search (CSO)":
            col3.metric("Generations", f"{len(alg._best_history)}")

        st.subheader("Generated Timetable")
        st.components.v1.html(html_result, height=1000, scrolling=True)

if __name__ == "__main__":
    main() 