Graph Neural Network Framework for Predicting the Potential Energy Landscape in Hybrid Monte Carlo Molecular Dynamics Simulations
============================================================================================

![Project Image](https://github.com/mashaekh-tausif/MCMD-GCNN/blob/ec687ac0f4413dc04b5e9f3a986294e7877cbe5e/Flowchart.png)

This project leverages graph neural networks (GNNs) to predict the potential energy landscape of a medium-entropy alloy through hybrid Monte-Carlo molecular dynamics (MC/MD) simulations.

--------------------------------------------------------------------------------------------
Instructions:
--------------------------------------------------------------------------------------------

1. Clone the Repository:
   ----------------------
   Use the following commands to clone the repository and navigate to the project directory:
   ```bash
   git clone https://github.com/yourusername/repo_name.git
   cd repo_name

1. Install Dependencies:
   ----------------------
   Install the necessary libraries as listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt

2. Edit config.yml:
   ------------------
   Update `config.yml` to specify the directories for LAMMPS (`lmp`) files and graph data storage.

3. Generate LAMMPS Files:
   -----------------------
   Run `lmp_file_maker.py` to create LAMMPS input files in the directory specified in `config.yaml`:
   ```bash
   python lmp_file_maker.py

4. Run Hybrid MC/MD Simulations:
   ------------------------------
   Run `lmp_file_run.py` to perform hybrid MC/MD simulations in LAMMPS for various annealing temperatures. 
   The default run command can be modified within this script if needed:
   ```bash
   python lmp_file_run.py

5. Generate Graph Data:
   ---------------------
   Convert dump files generated from simulations into graph data by running `make_graph.py`:
   ```bash
   python make_graph.py

6. Conduct Case Studies:
   ----------------------
   Execute the Jupyter notebooks for each of the three case studies by running:
   
   - case_study_1.ipynb: Training and predictions of single annealing temperature data
   - case_study_2.ipynb: Training a single model on combined annealing temperatures data
   - case_study_3.ipynb: Model trained on some annealing temperatures data, tested on unseen annealing temperatures data

   Open each notebook in Jupyter Notebook or Jupyter Lab to run the cells as needed.
   You can adjust annealing temperature parameters within each notebook.

--------------------------------------------------------------------------------------------


