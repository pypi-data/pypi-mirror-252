from hestia_earth.schema import EmissionMethodTier, EmissionStatsDefinition, TermTermType
from hestia_earth.utils.lookup import column_name, download_lookup, get_table_value, extract_grouped_data
from hestia_earth.utils.model import find_primary_product, filter_list_term_type, find_term_match
from hestia_earth.utils.tools import list_sum, safe_parse_float

from hestia_earth.models.log import debugMissingLookup, logRequirements, logShouldRun
from hestia_earth.models.utils.input import get_feed
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.property import get_node_property_value_converted
from hestia_earth.models.utils.liveAnimal import get_default_digestibility
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "completeness.animalFeed": "True",
        "inputs": [{
            "@type": "Input",
            "term.termType": ["crop", "animalProduct", "feedFoodAdditive", "forage", "liveAquaticSpecies"],
            "term.units": "kg",
            "value": "> 0",
            "isAnimalFeed": "True",
            "optional": {
                "properties": [{
                    "@type": "Property",
                    "value": "",
                    "term.@id": ["neutralDetergentFibreContent", "energyContentHigherHeatingValue"]
                }]
            }
        }]
    }
}
LOOKUPS = {
    "liveAnimal": [
        "digestibility",
        "percentageYmMethaneConversionFactorEntericFermentationIPCC2019",
        "percentageYmMethaneConversionFactorEntericFermentationIPCC2019-sd"
    ],
    "crop-property": ["neutralDetergentFibreContent", "energyContentHigherHeatingValue"]
}
RETURNS = {
    "Emission": [{
        "value": "",
        "sd": "",
        "methodTier": "tier 2",
        "statsDefinition": "modelled"
    }]
}
TERM_ID = 'ch4ToAirEntericFermentation'
TIER = EmissionMethodTier.TIER_2.value
LOOKUP_TABLE = 'liveAnimal.csv'


def _emission(value: float, sd: float):
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    if sd or sd == 0:
        emission['sd'] = [sd]
        emission['statsDefinition'] = EmissionStatsDefinition.MODELLED.value
    emission['methodTier'] = TIER
    return emission


def _run(feed: float, enteric_factor: float, enteric_sd: float):
    value = feed * enteric_factor / 55.65
    return [_emission(value, enteric_sd)]


DE_NDF_MAPPING = {
    'high_DE_low_NDF': lambda DE, NDF: DE >= 70 and NDF < 35,
    'high_DE_high_NDF': lambda DE, NDF: DE >= 70 and NDF >= 35,
    'medium_DE_high_NDF': lambda DE, NDF: DE >= 63 and DE < 70 and NDF > 37,
    'low_DE_high_NDF': lambda DE, NDF: DE < 62 and NDF >= 38
}

DE_MAPPING = {
    'high_medium_DE': lambda DE, _: DE > 63,
    'medium_DE': lambda DE, _: DE > 62 and DE < 72,
    'low_DE': lambda DE, _: DE <= 62,
    'high_DE': lambda DE, _: DE >= 72,
    'high_DE_ionophore': lambda DE, ionophore: DE > 75 and ionophore
}


def _get_grouped_data_key(keys: list, DE: float, NDF: float, ionophore: bool):
    # test conditions one by one and return the key associated for the first one that passes
    return next(
        (key for key in keys if key in DE_NDF_MAPPING and DE_NDF_MAPPING[key](DE, NDF)),
        None
    ) or next(
        (key for key in keys if key in DE_MAPPING and DE_MAPPING[key](DE, ionophore)),
        None
    )


def _extract_groupped_data(value: str, DE: float, NDF: float, ionophore: bool):
    value_keys = [val.split(':')[0] for val in value.split(';')]
    value_key = _get_grouped_data_key(value_keys, DE, NDF, ionophore)
    return safe_parse_float(extract_grouped_data(value, value_key))


def _get_liveAnimal_lookup_value(lookup, term_id: str, lookup_col: str, DE: float, NDF: float, ionophore: bool):
    value = get_table_value(lookup, 'termid', term_id, column_name(lookup_col)) if term_id else None
    debugMissingLookup(LOOKUP_TABLE, 'termid', term_id, lookup_col, value, model=MODEL, term=TERM_ID)
    return value if value is None or ':' not in value else _extract_groupped_data(value, DE, NDF, ionophore)


def _get_crop_property_average(cycle: dict, inputs: list, property_id: str):
    values = [get_node_property_value_converted(MODEL, input, property_id) for input in inputs]
    property_value = list_sum(values)
    ratio_inputs_with_props = len(values) / len(inputs) if len(inputs) and len(values) else 0
    total_value = list_sum([list_sum(i.get('value', [])) for i in inputs])

    logRequirements(cycle, model=MODEL, term=TERM_ID, property_id=property_id,
                    nb_inputs=len(inputs),
                    nb_inputs_with_prop=len(values),
                    ratio_inputs_with_props=ratio_inputs_with_props,
                    min_ratio=0.8)

    return (property_value / total_value) if total_value > 0 and ratio_inputs_with_props > 0.8 else 0


def _get_DE_type(lookup, term_id: str):
    return get_table_value(lookup, 'termid', term_id, column_name(LOOKUPS['liveAnimal'][0]))


def _is_ionophore(cycle: dict, total_feed: float):
    inputs = cycle.get('inputs', [])
    has_input = find_term_match(inputs, 'ionophores', None) is not None
    maize_input = find_term_match(inputs, 'maizeSteamFlaked', {'value': 0})
    maize_feed = get_feed(MODEL, [maize_input])
    return has_input and maize_feed / total_feed >= 0.9


def _should_run(cycle: dict):
    is_animalFeed_complete = cycle.get('completeness', {}).get('animalFeed', False) is True

    primary_product = find_primary_product(cycle) or {}
    term_id = primary_product.get('term', {}).get('@id')

    lookup = download_lookup(LOOKUP_TABLE)
    DE_type = _get_DE_type(lookup, term_id) if term_id else None

    total_feed = get_feed(MODEL, cycle.get('inputs', []), termTypes=[
        TermTermType.CROP.value,
        TermTermType.ANIMALPRODUCT.value,
        TermTermType.FEEDFOODADDITIVE.value,
        TermTermType.FORAGE.value,
        TermTermType.LIVEAQUATICSPECIES.value
    ])
    ionophore = _is_ionophore(cycle, total_feed) if total_feed > 0 else False

    inputs = filter_list_term_type(cycle.get('inputs', []), TermTermType.CROP)
    # only keep inputs that have a positive value
    inputs = list(filter(lambda i: list_sum(i.get('value', [])) > 0, inputs))
    DE = (
        _get_crop_property_average(cycle, inputs, DE_type) if DE_type and isinstance(DE_type, str) else None
    ) or get_default_digestibility(cycle) or 0
    NDF = _get_crop_property_average(cycle, inputs, 'neutralDetergentFibreContent')

    enteric_factor = safe_parse_float(_get_liveAnimal_lookup_value(
        lookup, term_id, LOOKUPS['liveAnimal'][1], DE, NDF, ionophore
    )) / 100
    enteric_sd = safe_parse_float(_get_liveAnimal_lookup_value(
        lookup, term_id, LOOKUPS['liveAnimal'][2], DE, NDF, ionophore
    ), None)

    logRequirements(cycle, model=MODEL, term=TERM_ID,
                    term_type_animalFeed_complete=is_animalFeed_complete,
                    DE_type=DE_type,
                    digestibility=DE,
                    ndf=NDF,
                    ionophore=ionophore,
                    total_feed=total_feed,
                    enteric_factor=enteric_factor,
                    enteric_sd=enteric_sd)

    should_run = all([is_animalFeed_complete, total_feed, enteric_factor, DE, NDF])
    logShouldRun(cycle, MODEL, TERM_ID, should_run, methodTier=TIER)
    return should_run, total_feed, enteric_factor, enteric_sd


def run(cycle: dict):
    should_run, feed, enteric_factor, enteric_sd = _should_run(cycle)
    return _run(feed, enteric_factor, enteric_sd) if should_run else []
