import codecs
import subprocess
import pathlib
import os
import sys
import tempfile
import time
import traceback

from model.Configuration import Configuration
from src.Cso import Cso
from src.HTMLOutput import HtmlOutput
from src.SimulatedAnnealing import SimulatedAnnealing


def main(file_name, alg_name="cso"):
    start_time = int(round(time.time() * 1000))

    configuration = Configuration()
    target_file = str(pathlib.Path().absolute()) + file_name
    configuration.parseFile(target_file)

    if alg_name == "sa":
        alg = SimulatedAnnealing(configuration)
    else:
        alg = Cso(configuration)

    print("\n\nMaking a Class Schedule Using", alg, ".\n")
    alg.run()
    html_result = HtmlOutput.getResult(alg.result)

    temp_file_path = tempfile.gettempdir() + file_name.replace(".json", ".htm")
    writer = codecs.open(temp_file_path, "w", "utf-8")
    writer.write(html_result)
    writer.close()

    seconds = (int(round(time.time() * 1000)) - start_time) / 1000.0
    print("\nCompleted in {} secs.\n".format(seconds))

    opener = "open" if sys.platform == "darwin" else "xdg-open"
    subprocess.call([opener, temp_file_path])


if __name__ == "__main__":
    # file_name = "/GaSchedule.json"
    file_name = "/Input.json"
    alg_name = "cso"
    if len(sys.argv) > 1:
        if sys.argv[1] in ["cso", "sa"]:
            alg_name = sys.argv[1]
        else:
            file_name = sys.argv[1]
    
    if len(sys.argv) > 2:
        alg_name = sys.argv[2]


    try:
        main(file_name, alg_name)
    except:
        traceback.print_exc()
