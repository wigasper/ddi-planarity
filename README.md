# ddi-planarity

These are scripts used to analyze *S. cerevisiae* protein complexes in the context of their respective domain-domain interaction graphs.

## File Descriptions
### analysis
* **analysis/binding_affinity_analysis.py** - wrangles binding affinity data into a suitable data frame format for further analysis
* **analysis/check_repeated_entities.py** - uses the PDBe API to determine the number of polypeptides, and the count and frequency of repeated unique polypeptide entities in each complex 
* **analysis/checking_bimodal_groups.py** - seperates out the groups centered around each mode in the bimodal distribution of proportion of repeated entities for the planar complex group
* **analysis/disorder_analysis.py** - wrangles complex disorder data for exploratory analysis
* **analysis/essentiality_pcts.py** - puts together percent essentiality (the relative frequency of essential genes in each complex) data for further analysis
* **analysis/hydrophobicity_analysis.py** - computes the mean hydrophobicity for each complex in the planar and nonplanar groups and organizes data into a suitable data frame format for further analysis
* **analysis/panther.py** - wrangles data from PANTHER into a suitable format for visualization with ggplot2
* **analysis/planar_eda.md** - statistical analyses and visualizations for complex structural (and other) data factored by complex planarity
* **analysis/repeat_numbers.py** - organizes data related to the number of repeated unique polypeptide units in each complex for further statistical analysis
* **analysis/secondary_structure_analysis.py** - organizes secondary structure data into suitable format for further anslysis

### data-aggregation
* **data-aggregation/combine_size_data.py** - generates data about the domain-domain interaction graphs of each complex and aggregates this data in combination with structural data
* **data-aggregation/get_and_parse_pdb.py** - gets structural data for each complex from PDB and calls PRODIGY to compute binding affinity data for each complex
* **data-aggregation/get_complex_components.py** - gets Uniprot IDs and gene symbols for the protein entities comprising each complex (represented by a PDB ID)
* **data-aggregation/get_complex_disorder.py** - retrieves disorder content for proteins in complexes from MobiDB
* **data-aggregation/get_id_map.py** - attempts to get gene symbols for proteins comprising complexes
* **data-aggregation/get_secondary_struct_data.py** - retrieves and aggregates secondary structure data for complexes
* **data-aggregation/get_secondary_struct_residue_counts.py** - retrieves secondary structure data for each complex and counts the numbers of residues involved in secondary structure features for each complex
* **data-aggregation/parse_3did_dmi.py** - parses the 3did DMI file in order to get all interacting residues in complexes
* **data-aggregation/residue_counts_by_planarity.py** - separates the complex size data (size in number of residues) by planarity for further analysis
* **data-aggregation/uniprot_to_gene.py** - attempts to get a gene symbol from a Uniprot ID
