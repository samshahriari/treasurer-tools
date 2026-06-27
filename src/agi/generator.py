"""AGI XML generation logic matching the official Skatteverket e-filing format."""

from datetime import datetime
import xml.etree.ElementTree as ET
from .config import AGIConfig
from .models import Employee

NS_DEFAULT = "http://xmls.skatteverket.se/se/skatteverket/da/instans/schema/1.1"
NS_AGD = "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
NS_XSI = "http://www.w3.org/2001/XMLSchema-instance"


def generate_agi_xml(employees: list[Employee], config: AGIConfig) -> str:
    """
    Generate Skatteverket Arbetsgivardeklaration (AGI) XML in the official e-filing format.

    Args:
        employees: List of validated Employee models.
        config: Configuration containing sender and employer metadata.

    Returns:
        A string containing the serialized, pretty-printed XML document.
    """
    # Register namespaces to match exactly the official format
    ET.register_namespace("", NS_DEFAULT)
    ET.register_namespace("agd", NS_AGD)
    ET.register_namespace("xsi", NS_XSI)

    # 1. Root Element: <Skatteverket> with attributes and default namespace
    root = ET.Element(
        f"{{{NS_DEFAULT}}}Skatteverket",
        {
            "omrade": "Arbetsgivardeklaration",
            f"{{{NS_XSI}}}schemaLocation": (
                f"{NS_DEFAULT} "
                "http://xmls.skatteverket.se/se/skatteverket/da/arbetsgivardeklaration/arbetsgivardeklaration_1.1.xsd"
            ),
        },
    )

    # Helper function to create agd namespace elements
    def agd_el(tag, parent=None, **attrs) -> ET.Element:
        tag_name = f"{{{NS_AGD}}}{tag}"
        if parent is not None:
            return ET.SubElement(parent, tag_name, **attrs)
        return ET.Element(tag_name, **attrs)

    # Helper function to create agd namespace elements with text content
    def agd_el_text(tag, parent, text, **attrs) -> ET.Element:
        el = agd_el(tag, parent, **attrs)
        el.text = str(text)
        return el

    # 2. <agd:Avsandare> (Sender Information)
    avsandare = agd_el("Avsandare", root)
    agd_el_text("Programnamn", avsandare, config.org_namn)
    agd_el_text("Organisationsnummer", avsandare, config.org_number)

    tech_contact = agd_el("TekniskKontaktperson", avsandare)
    agd_el_text("Namn", tech_contact, config.contact_name)
    agd_el_text("Telefon", tech_contact, config.contact_phone)
    agd_el_text("Epostadress", tech_contact, config.contact_email)

    agd_el_text(
        "Skapad",
        avsandare,
        datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    )

    # 3. <agd:Blankettgemensamt> (Contact person for the employer)
    gemensamt = agd_el("Blankettgemensamt", root)
    arbetsgivare = agd_el("Arbetsgivare", gemensamt)
    agd_el_text("AgRegistreradId", arbetsgivare, config.org_number)

    contact = agd_el("Kontaktperson", arbetsgivare)
    agd_el_text("Namn", contact, config.contact_name)
    agd_el_text("Telefon", contact, config.contact_phone)
    agd_el_text("Epostadress", contact, config.contact_email)
    agd_el_text("Sakomrade", contact, config.contact_subject_area)

    # Calculate individual entries and sums
    period_year = int(config.reporting_period[:4])
    total_tax = sum(int(round(emp.skatt)) for emp in employees)
    total_employer_contrib = sum(
        emp.calculate_employer_contribution(period_year) for emp in employees
    )

    # 4. Huvuduppgift (HU) <agd:Blankett> Block
    blankett_hu = agd_el("Blankett", root)

    arende_hu = agd_el("Arendeinformation", blankett_hu)
    agd_el_text("Arendeagare", arende_hu, config.org_number)
    agd_el_text("Period", arende_hu, config.reporting_period)

    innehall_hu = agd_el("Blankettinnehall", blankett_hu)
    hu = agd_el("HU", innehall_hu)

    hugroup = agd_el("ArbetsgivareHUGROUP", hu)
    agd_el_text("AgRegistreradId", hugroup, config.org_number, faltkod="201")

    agd_el_text(
        "RedovisningsPeriod",
        hu,
        config.reporting_period,
        faltkod="006",
    )
    agd_el_text(
        "i",
        hu,
        str(total_employer_contrib),
        faltkod="487",
    )
    agd_el_text("SummaSkatteavdr", hu, str(total_tax), faltkod="497")

    # 5. Individuppgift (IU) <agd:Blankett> Blocks (one per employee)
    for idx, emp in enumerate(employees, start=1):
        emp_tax = int(round(emp.skatt))
        emp_salary = int(round(emp.total_lon))

        blankett_iu = agd_el("Blankett", root)

        arende_iu = agd_el("Arendeinformation", blankett_iu)
        agd_el_text("Arendeagare", arende_iu, config.org_number)
        agd_el_text("Period", arende_iu, config.reporting_period)

        innehall_iu = agd_el("Blankettinnehall", blankett_iu)
        iu = agd_el("IU", innehall_iu)

        iugroup = agd_el("ArbetsgivareIUGROUP", iu)
        agd_el_text("AgRegistreradId", iugroup, config.org_number, faltkod="201")

        mottagargroup = agd_el("BetalningsmottagareIUGROUP", iu)
        mottagarchoice = agd_el("BetalningsmottagareIDChoice", mottagargroup)
        agd_el_text(
            "BetalningsmottagarId",
            mottagarchoice,
            emp.personnummer,
            faltkod="215",
        )

        agd_el_text(
            "RedovisningsPeriod",
            iu,
            config.reporting_period,
            faltkod="006",
        )

        # Specifikationsnummer formatted as zero-padded 3-digit string (e.g. 001)
        spec_num = f"{idx:03d}"  # TODO: depend on verksamhets
        agd_el_text("Specifikationsnummer", iu, spec_num, faltkod="570")

        # Gross cash salary (FK011)
        agd_el_text(
            "KontantErsattningUlagAG",
            iu,
            str(emp_salary),
            faltkod="011",
        )

        # Withheld tax (FK001)
        agd_el_text("AvdrPrelSkatt", iu, str(emp_tax), faltkod="001")

    # Pretty-print the document with 2-space indentation
    ET.indent(root, space="  ")

    # Serialize to XML string with standalone="no" matching the example file
    xml_bytes = ET.tostring(
        root,
        encoding="UTF-8",
        xml_declaration=True,
    )
    xml_str = xml_bytes.decode("utf-8")

    # Replace the single quotes in the XML declaration to double quotes,
    # and append ' standalone="no"' to fully match the example's header.
    if xml_str.startswith("<?xml version='1.0' encoding='UTF-8'?>"):
        xml_str = xml_str.replace(
            "<?xml version='1.0' encoding='UTF-8'?>",
            '<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
            1,
        )

    return xml_str
