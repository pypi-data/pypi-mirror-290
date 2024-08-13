import pandas as pd
from sarapy.utils import amg_ppk
import os
def getRawOperations(data_file, historical_data_file):
    """
    Args:
        data_file: Path to the file with the data.
        historical_data_file: Path to the file with the historical data.
    Returns the raw operations from the database.
    """
    #cargo examples\2024-05-30\UPM007N\data.json
    data = pd.read_json(os.path.join("examples","2024-05-30","UPM007N","data.json"))
    historical_data = pd.read_json(os.path.join("examples","2024-05-30","UPM007N","historical-data.json"))
    #convierto a lista de diccionarios
    data=data.to_dict(orient="records")
    historical_data=historical_data.to_dict(orient="records")
    hash_table = {}
    for datum in data:
        hash_table[datum["timestamp"]] = {"id_db_dw": datum["id"], "id_db_h": 0, "serialized_datum": ""}
    for historical_datum in historical_data:
        if historical_datum["timestamp"] in hash_table:
            hash_table[historical_datum["timestamp"]].update({"id_db_h": historical_datum["id"], "serialized_datum": historical_datum["datum"]})
    ppk_results = amg_ppk.main(hash_table, [])  # ToDo: PPK (Fernando)

    return ppk_results