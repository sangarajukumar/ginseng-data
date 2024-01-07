import streamlit as st
import pandas as pd
from rdkit import Chem
from mordred import Calculator, descriptors
import base64

# Function to calculate descriptors using Mordred
def calculate_descriptors(smiles_list, mol_ids):
    # Initialize RDKit and Mordred calculator
    calc = Calculator(descriptors, ignore_3D=False)
    mols = [Chem.MolFromSmiles(smi) for smi in smiles_list]
    
    # Calculate descriptors and return as pandas dataframe
    df = calc.pandas(mols).fillna(0)
    df.insert(0, 'Compound_Name', mol_ids)
    return df

# Function to download data as CSV
def filedownload(df):
    csv = df.to_csv(index=False, header=True)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="molecular_descriptors.csv">Download CSV File</a>'
    return href

# Page title
st.markdown("""
# Molecular Descriptor Calculator using Mordred

This app calculates molecular descriptors for computational drug discovery projects, such as QSAR/QSPR models.

**Credits**
- Descriptor calculated using [Mordred-Descriptor](https://github.com/mordred-descriptor/mordred) software.
- Moriwaki, H., Tian, YS., Kawashita, N. et al. Mordred: a molecular descriptor calculator. J Cheminform 10, 4 (2018). https://doi.org/10.1186/s13321-018-0258-y       
""")

# Sidebar
with st.sidebar.header('1. Upload your CSV data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
    st.sidebar.markdown("""
[Example CSV input file](https://raw.githubusercontent.com/sangarajukumar/ginseng-data/main/Ginseng_dataset.csv)
""")

with st.sidebar.header('2. Enter column names for Molecule ID and SMILES'):
    name_mol = st.sidebar.text_input('Column name for Compounds', 'Compound_Name')
    name_smiles = st.sidebar.text_input('Column name for SMILES', 'canonical_smiles')

# Main app
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader('Initial data from CSV file')
    st.dataframe(df)

    st.subheader('Formatted as Mordred input file')
    formatted_df = df[[name_mol, name_smiles]]
    st.dataframe(formatted_df)
    
    if st.button("Calculate Descriptors"):
        with st.spinner("Calculating descriptors using Mordred..."):
            descriptors_df = calculate_descriptors(df[name_smiles].tolist(), df[name_mol].tolist())
            st.subheader('Calculated Molecular Descriptors')
            st.dataframe(descriptors_df)
            st.markdown(filedownload(descriptors_df), unsafe_allow_html=True)
            st.info('Number of descriptors: ' + str(descriptors_df.shape[1]-1))  # Subtract 1 for Compound_Name column
else:
    st.info('Awaiting for CSV file to be uploaded.')

# Example dataset button
if st.button('Use Example Dataset'):
    example_url = 'https://raw.githubusercontent.com/sangarajukumar/ginseng-data/main/Ginseng_dataset.csv'
    example_df = pd.read_csv(example_url)
    st.subheader('Initial data from Example CSV file')
    st.dataframe(example_df)
    
    st.subheader('Formatted as Mordred input file')
    formatted_example_df = example_df[[name_mol, name_smiles]]
    st.dataframe(formatted_example_df)
    
    with st.spinner("Calculating descriptors using Mordred..."):
        example_descriptors = calculate_descriptors(example_df[name_smiles].tolist(), example_df[name_mol].tolist())
        st.subheader('Calculated Molecular Descriptors')
        st.dataframe(example_descriptors)
        st.markdown(filedownload(example_descriptors), unsafe_allow_html=True)
        st.info('Number of descriptors: ' + str(example_descriptors.shape[1]-1))  # Subtract 1 for Compound_Name column