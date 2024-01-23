import json
from tests.utils import fixtures_path

from hestia_earth.models.cycle.product.properties import MODEL_KEY, run

class_path = f"hestia_earth.models.cycle.product.{MODEL_KEY}"
fixtures_folder = f"{fixtures_path}/cycle/product/{MODEL_KEY}"


def test_run_with_dryMatter():
    with open(f"{fixtures_folder}/with-dryMatter/cycle.jsonld", encoding='utf-8') as f:
        cycle = json.load(f)

    with open(f"{fixtures_folder}/with-dryMatter/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    result = run(cycle)
    print(json.dumps(result, indent=2))
    assert result == expected
