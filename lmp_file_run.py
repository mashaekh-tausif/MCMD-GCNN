import os
import subprocess
import yaml
# Specify the directory you want to run the command in
with open("config.yml", "r") as file:
    config = yaml.safe_load(file)

base_directory=config['directories']['lmp_file_directory']


for temperature in range(350,1150+1,100):

    print(f'T={temperature}K')


    directory = base_directory+f'\\T={temperature}K'

    print(directory)

    os.chdir(directory)

    command = f"mpiexec -np 12 lmp -in lmp_T={temperature}.txt"  # For Windows


    subprocess.run(command, shell=True, capture_output=True, text=True)

