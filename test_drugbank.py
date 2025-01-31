import pytest
import pandas as pd
import matplotlib.pyplot as plt
from unittest.mock import MagicMock, patch
from bs4 import BeautifulSoup
from pandas.testing import assert_frame_equal
from drugbank import create_df_info, extract_drugs, draw_group_pie_chart, create_df_products, draw_hist_interactions, analyze_gene

#testing extracting drugs
@pytest.mark.parametrize("path, expected_result", [
    ("skaramoosh.xml", None),
])
def test_extract_drugs_file_not_found(path, expected_result):
    with patch("os.path.exists", return_value=False):
        result = extract_drugs(path, 0)
        assert result == expected_result

#testing drawing pie chart
@pytest.mark.parametrize("approved, withdrawn, experimental, vet_approved", [
    (10, 5, 3, 2),  
    (0, 0, 0, 0),   
    (50, 25, 10, 5),
    (1, 1, 1, 1),
])
def test_draw_group_pie_chart(approved, withdrawn, experimental, vet_approved):
    with patch("matplotlib.pyplot.pie", return_value=(["color1", "color2", "color3", "color4"], None, None)) as mock_pie, \
        patch("matplotlib.pyplot.legend") as mock_legend, \
        patch("matplotlib.pyplot.show"):

        draw_group_pie_chart(approved, withdrawn, experimental, vet_approved)

        mock_pie.assert_called_once_with([approved, withdrawn, experimental, vet_approved], labels=None, autopct='%1.1f%%')
        expected_legend_labels = [
            f'approved: {approved}',
            f'withdrawn: {withdrawn}',
            f'experimental/investigational: {experimental}',
            f'vet approved: {vet_approved}'
        ]
        mock_legend.assert_called_once()

#testing creating df info
@pytest.fixture
def sample_df_info():
    """Fixture to provide a mock drug list as a BeautifulSoup object."""
    xml_data = """
    <drugs>
        <drug type="small-molecule">
            <drugbank-id primary="true">DB0001</drugbank-id>
            <name>Medikinet</name>
            <description>Used to treat ADHD.</description>
            <state>Solid</state>
            <indication>Improves attention in ADHD patients.</indication>
            <mechanism-of-action>Stimulates dopamine and norepinephrine release.</mechanism-of-action>
            <food-interactions>
                <food-interaction>Avoid high-fat meals.</food-interaction>
            </food-interactions>
        </drug>
        <drug type="biotech">
            <drugbank-id primary="true">DB0002</drugbank-id>
            <name>Clonazepam</name>
            <description>A benzodiazepine for seizures and anxiety.</description>
            <state>Solid</state>
            <indication>Treats seizures and panic disorders.</indication>
            <mechanism-of-action>Enhances GABAergic transmission.</mechanism-of-action>
            <food-interactions></food-interactions>
        </drug>
    </drugs>
    """
    soup = BeautifulSoup(xml_data, "xml")
    return soup.find_all("drug")

def test_create_df_info(sample_df_info):
    df_result, _, _ = create_df_info(sample_df_info)

    expected_data = {
        "Drugbank ID": ["DB0001", "DB0002"],
        "Name": ["Medikinet", "Clonazepam"],
        "Type": ["small-molecule", "biotech"],
        "Description": ["Used to treat ADHD.", "A benzodiazepine for seizures and anxiety."],
        "State": ["Solid", "Solid"],
        "Indication": ["Improves attention in ADHD patients.", "Treats seizures and panic disorders."],
        "Mechanism": ["Stimulates dopamine and norepinephrine release.", "Enhances GABAergic transmission."],
        "Food interactions": [["Avoid high-fat meals."], None],
    }

    expected_df = pd.DataFrame(expected_data)

    assert_frame_equal(df_result, expected_df, check_dtype=False)

#testing creating df products
@pytest.fixture
def sample_df_products():
    xml_data = """
    <drugs>
        <drug type="small-molecule">
            <drugbank-id primary="true">DB0001</drugbank-id>
            <name>Medikinet</name>
            <products>
                <product>
                    <name>Medikinet 10mg</name>
                    <labeller>Pharma Inc.</labeller>
                    <ndc-product-code>12345-6789</ndc-product-code>
                    <dosage-form>Tablet</dosage-form>
                    <route>Oral</route>
                    <strength>10mg</strength>
                    <country>US</country>
                    <source>FDA</source>
                </product>
            </products>
        </drug>
        <drug type="biotech">
            <drugbank-id primary="true">DB0002</drugbank-id>
            <name>Clonazepam</name>
            <products>
                <product>
                    <name>Clonazepam 2mg</name>
                    <labeller>HealthCorp</labeller>
                    <dosage-form>Tablet</dosage-form>
                    <route>Oral</route>
                    <strength>2mg</strength>
                    <country>Germany</country>
                    <source>EMA</source>
                </product>
            </products>
        </drug>
    </drugs>
    """
    soup = BeautifulSoup(xml_data, "xml")
    drug_list = soup.find_all("drug")
    drugbank_id_list = [drug.find("drugbank-id", attrs={"primary": "true"}).text.strip() for drug in drug_list]

    return drug_list, drugbank_id_list

def test_create_df_products(sample_df_products):
    
    drug_list, drugbank_id_list = sample_df_products
    df_result = create_df_products(drug_list, drugbank_id_list)

    expected_data = {
        "Drugbank ID": ["DB0001", "DB0002"],
        "Name": ["Medikinet 10mg", "Clonazepam 2mg"],
        "Labeller": ["Pharma Inc.", "HealthCorp"],
        "National Drug Code": ["12345-6789", "No information"], 
        "Dosage form": ["Tablet", "Tablet"],
        "Route": ["Oral", "Oral"],
        "Strength": ["10mg", "2mg"],
        "Country": ["US", "Germany"],
    }

    expected_df = pd.DataFrame(expected_data)

    assert_frame_equal(df_result, expected_df, check_dtype=False)

#checking analyzing a gene
@pytest.fixture
def sample_analyze_drug():
    xml_data = """
    <drug type="small-molecule">
        <drugbank-id primary="true">DB0001</drugbank-id>
        <name>Thiocodin</name>
    </drug>
    """
    soup = BeautifulSoup(xml_data, "xml")
    return soup.find("drug")

def test_analyze_gene_no_polypeptide(sample_analyze_drug):
    result = analyze_gene(sample_analyze_drug)
    assert result is None


