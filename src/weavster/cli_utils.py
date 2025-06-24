from pathlib import Path

import typer

TEMPLATE_PROJECT_YML = """\
project_name: %s
compiler_url: http://localhost:8080/craft
version: 0.1.0
"""

TEMPLATE_TRANSFORMER = """\
name: normalize_lab_data
description: Normalize incoming lab data to standard schema
inputs:
  - hl7_message
steps:
  - use_macro: normalize_name
  - lookup: lab_code_mappings
    key: hl7_message.obx.3
output: normalized_lab
"""

TEMPLATE_MACRO = """\
name: normalize_name
description: Standardizes patient names
params:
  - input_field
steps:
  - operation: trim_whitespace
  - operation: title_case
"""

TEMPLATE_CONNECTOR = """\
name: emr_connection
type: hl7_listener
port: 2575
protocol: MLLP
"""

TEMPLATE_ROUTE = """\
name: lab_results_route
source: emr_connection
filters:
  - filter_by_patient_type
transformers:
  - normalize_lab_data
destination: fhir_api
"""


def create_file(path: Path, content: str) -> None:
    """
    Create a file at the specified path with the given content.
    If the parent directory does not exist, it will be created.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    typer.echo(f"Created: {path}")
