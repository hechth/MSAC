"""
check : Calculate the combined input+ adduct mass.
author: @m-blumer
"""
# Imports
import pandas as pd
import numpy as np

# Functions
def calculate_total_mz(adduct_tuple, mass):
    """Calculate adduct mz using multiplier, charge, and mass
    Parameters
    ----------
    adduct_tuple : tuple of floats
        input mass multiplier, adduct charge, and adduct mz 
    mass : int or float
        Total mass of input molecule
    Returns
    -------
    float
        Returns the total mz for the adduct/molecule pair.
    """
    input_mz_multiplier = adduct_tuple[0]
    adduct_charge = adduct_tuple[1]
    adduct_mz = adduct_tuple[2]
    #  calculating as adduct mz + ((input multiplier*input mass)/charge)
    total_mz = adduct_mz + input_mz_multiplier*mass/np.absolute(adduct_charge)
    return total_mz


def calculate_all_mz(df, mass_file, mass_col):
    """Calculate adduct mz using multiplier, charge, and mass
    Parameters
    ----------
    df : DataFrame
        Contains an entry representing each adduct of interest, 
        including adduct name, charge, m/z, and input mass multipler
    mass_file : str
        File containing masses of the input molecules.
    mass_col : str
        Name of mass column in mass_file.
    Returns
    -------
    DataFrame
        Returns a table of caluclated masses across all adducts for each input molecule.
    """
    input_masses = pd.read_csv(mass_file)

    #  create a lookup table for the adduct information:
    #  name, input mass mulitpler, charge, m/z
    d = {adduct: [mult, charge, mass] for adduct, (mult, (charge, mass))
         in zip(df['adduct'], zip(df['input_mass_multiplier'],
                zip(df['charge'], df['m/z'])))}

    masses_to_calc = input_masses[mass_col]
    original_cols = input_masses.columns
    all_masses = []
    for adduct in d.keys():
        #  put pos or neg on adduct name
        #  to designate electrospray ionization state
        if int(d[adduct][1]) > 0:
            adduct_name = adduct + '_ESIpos'
        else:
            adduct_name = adduct + '_ESIneg'
        input_masses[adduct_name] = [calculate_total_mz(d[adduct], mass)
                                     for mass in masses_to_calc]
    
    input_masses = pd.melt(input_masses, id_vars=original_cols, var_name='adduct', value_name='adduct mass')

    return input_masses
