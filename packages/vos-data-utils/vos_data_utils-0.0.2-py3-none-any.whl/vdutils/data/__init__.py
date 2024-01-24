import os
import pickle


def get_data_from_pnu(file_name):
    data_dir_path = os.path.abspath(__file__).replace("__init__.py", '')
    data_file_path = f"{data_dir_path}/pnu/{file_name}"
    with open(data_file_path, "rb") as f:
        return pickle.load(f)

def get_files_from_pnu():
    data_dir_path = os.path.abspath(__file__).replace("__init__.py", '')
    return os.listdir(f"{data_dir_path}/pnu")
