import os
import yaml
import shutil

with open("config.yml", "r") as file:
    config = yaml.safe_load(file)

structure_file_name='structure.lmp'
potential_file_name='NiCoCr.lammps.eam'

# Specify the absolute path to the main directory
main_directory = config['directories']['lmp_file_directory']  # Linux/Mac

os.makedirs(main_directory, exist_ok=True)

# Loop to create folders for different temperature values and save files inside them
for temp in range(350, 1150+1, 100):
    # Define the sub-folder path for each temperature
    sub_folder = os.path.join(main_directory, f"T={temp}K")

    # Create the sub-folder if it doesn't already exist
    os.makedirs(sub_folder, exist_ok=True)

    # Define the LAMMPS input script as a multi-line string, using the temperature variable
    lammps_script = f"""
    units           metal
    atom_style      atomic
    dimension       3
    boundary        p p p
    variable        temperature equal {temp}

    read_data       structure.lmp

    pair_style      eam/alloy
    pair_coeff      * * NiCoCr.lammps.eam Co Cr Ni 

    timestep        0.001
    reset_timestep  0

    min_style       cg
    minimize        1.0e-6  1.0e-8   1000    100000

    velocity        all create ${{temperature}} 4598 dist gaussian

    #-----------Compute Different Properties---------

    compute         potential all pe

    thermo          10000
    thermo_style    custom step tpcpu temp c_potential
    run             0
    

    #--------------NPT Equilibration-------------

    fix             1 all npt temp ${{temperature}} ${{temperature}} 0.1 iso 0 0 1 drag 1.8

    run             75000
    unfix           1

    reset_timestep  0

    write_data      NPT_complete.txt
    variable        pot_energy equal "c_potential"

    write_dump all custom dump.mc.0 id type x y z vx vy vz
    print			"0 ${{pot_energy}}" append "Potential Energy vs step T_{temp}.txt" screen no


    #----------------Monte Carlo Simulation------------------------

    variable        i loop 60000

    label loop

    variable        modulus equal ${{i}}%200
    variable        tmp_1 equal ${{i}}*10*round(random(1,100,45962))
    variable        tmp_2 equal ${{i}}*20*round(random(1,100,566243))
    variable        tmp_3 equal ${{i}}*30*round(random(1,100,759452))

    variable        SEED_1 equal round(random(10,100000,${{tmp_1}}))
    variable        SEED_2 equal round(random(10,100000,${{tmp_2}}))
    variable        SEED_3 equal round(random(10,100000,${{tmp_3}}))

    variable        w1 equal round(random(0.5,3.5,${{SEED_1}}))
    variable        t1 equal ${{w1}}

    label           atom_2
    variable        w2 equal round(random(0.5,3.5,${{SEED_2}}))
    variable        t2 equal ${{w2}}

    if "${{t1}}==${{t2}}" then "jump SELF atom_2"
    fix             1 all atom/swap 1 10 ${{SEED_3}} ${{temperature}} types ${{t1}} ${{t2}}

    run             1
    unfix           1

    fix             2 all npt temp ${{temperature}} ${{temperature}} 0.1 iso 0 0 1 drag 1.8
    run             2
    unfix           2

   

    print           "${{i}} ${{pot_energy}}" append "Potential Energy vs step T_{temp}.txt" screen no

    if "${{modulus}}==0" then " write_dump all custom dump.mc.${{i}} id type x y z vx vy vz"

    print           "Step = ${{i}} t1=${{t1}} t2=${{t2}}"
    next            i
    jump            SELF loop
    write_data	final_T_${{temp}}K.txt
    """

    shutil.copy(structure_file_name,sub_folder)
    shutil.copy(potential_file_name,sub_folder)

    # Define the file path inside the sub-folder for each temperature
    file_path = os.path.join(sub_folder, f"lmp_T={temp}.txt")

    # Write the LAMMPS script to the file inside the sub-folder
    with open(file_path, 'w') as file:
        file.write(lammps_script)








    print(f"LAMMPS input script has been written to {file_path}")
