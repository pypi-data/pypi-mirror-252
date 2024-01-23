REQUIREMENTS = {
    "Cycle": {
        "inputs": [{
            "@type": "Input",
            "term.units": "kg",
            "term.termType": ["crop", "animalProduct", "feedFoodAdditive"],
            "value": "> 0",
            "isAnimalFeed": "True",
            "properties": [{"@type": "Property", "value": "", "term.@id": "energyContentHigherHeatingValue"}]
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
    "crop-property": "energyContentHigherHeatingValue"
}
TERM_ID = 'feedConversionRatioCarbon'


def run(cycle: dict, feed: float): return feed * 0.021
