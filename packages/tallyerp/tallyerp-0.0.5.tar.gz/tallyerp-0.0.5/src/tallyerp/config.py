import os
import xml.etree.ElementTree as gfg


tallyMasterImportBody = {
    "HEADER": {
        "VERSION": 1,
        "TALLYREQUEST": "Import",
        "TYPE": "Data",
        "ID": "All Masters",
    },
    "BODY": {
        "DESC": {"STATICVARIABLES": {"IMPORTDUPS": "@@DUPCOMBINE"}},
        "DATA": {"TALLYMESSAGE": {}},
    },
}


TALLY_URL = os.environ.get("TALLY_API_URL", "http://localhost:9000")


class TallyRequestTemplate:
    masterImport = tallyMasterImportBody

