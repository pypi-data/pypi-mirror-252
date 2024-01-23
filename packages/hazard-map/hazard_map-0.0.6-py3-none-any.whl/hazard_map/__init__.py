import sys

from .hazardmap import HazardMap
from .types_constants import Sheet

def main():
    try:
        workbook_filename = sys.argv[1]
    except IndexError:
        raise Exception('Please pass an xlsx file')

    hazard_map = HazardMap(workbook_filename)
    hazard_map.extract_sheet_mappings([
        Sheet('cause-hazard', True),
        Sheet('cause-control', False)
    ])

    hazard_map.write_to_file()
    hazard_map.save_graph()
