"""
Product Properties

This model handles the following case:
- when the `dryMatter` property is set, the model recalculates the other properties based on the data from feedipedia.
"""
from hestia_earth.utils.model import find_term_match

from hestia_earth.models.utils.feedipedia import rescale_properties_from_dryMatter
from .. import MODEL

REQUIREMENTS = {
    "Cycle": {
        "products": [{
            "@type": "Product",
            "or": {
                "properties": [{"@type": "Property", "@id": "dryMatter"}]
            }
        }]
    }
}
RETURNS = {
    "Product": [{
        "properties": [{
            "@type": "Property"
        }]
    }]
}
MODEL_KEY = 'properties'
DRY_MATTER_TERM_ID = 'dryMatter'


def _should_run_by_dryMatter(product: dict):
    return find_term_match(product.get('properties', []), 'dryMatter') is not None


def run(cycle: dict):
    # filter list of products to run
    products = [
        i for i in cycle.get('products', []) if any([
            _should_run_by_dryMatter(i)
        ])
    ]
    return rescale_properties_from_dryMatter(MODEL, cycle, products)
