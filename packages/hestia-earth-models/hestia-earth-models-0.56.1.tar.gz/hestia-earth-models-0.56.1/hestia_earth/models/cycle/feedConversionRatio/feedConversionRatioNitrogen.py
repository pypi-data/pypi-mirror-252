from hestia_earth.schema import TermTermType
from hestia_earth.utils.tools import list_sum
from hestia_earth.utils.model import filter_list_term_type

from hestia_earth.models.utils.property import get_node_property_value_converted

from .. import MODEL

REQUIREMENTS = {
    "Cycle": {
        "inputs": [{
            "@type": "Input",
            "term.units": "kg",
            "term.termType": ["crop", "animalProduct", "feedFoodAdditive"],
            "value": "> 0",
            "isAnimalFeed": "True",
            "properties": [
                {"@type": "Property", "value": "", "term.@id": "energyContentHigherHeatingValue"},
                {"@type": "Property", "value": "", "term.@id": "crudeProteinContent"}
            ]
        }],
        "products": [{
            "@type": "Product",
            "term.termType": "animalProduct",
            "optional": {
                "properties": [{
                    "@type": "Property",
                    "value": "",
                    "term.@id": [
                        "processingConversionLiveweightToColdCarcassWeight",
                        "processingConversionLiveweightToColdDressedCarcassWeight",
                        "processingConversionColdCarcassWeightToReadyToCookWeight",
                        "processingConversionColdDressedCarcassWeightToReadyToCookWeight"
                    ]
                }]
            }
        }]
    }
}
RETURNS = {
    "Practice": [{
        "value": ""
    }]
}
LOOKUPS = {
    "crop-property": "crudeProteinContent"
}
TERM_ID = 'feedConversionRatioNitrogen'


def run(cycle: dict, feed: float):
    inputs = filter_list_term_type(cycle.get('inputs', []), TermTermType.CROP)
    return list_sum([get_node_property_value_converted(MODEL, input, 'crudeProteinContent') / 625 for input in inputs])
