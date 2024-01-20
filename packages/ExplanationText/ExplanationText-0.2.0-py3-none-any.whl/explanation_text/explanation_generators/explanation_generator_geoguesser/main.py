from explanation_text.explanation_generators.explanation_generator_geoguesser.information_generator import \
    generate_part_information
from explanation_text.explanation_generators.explanation_generator_geoguesser.knowledge_base.wikipedia import \
    get_first_sentence_wikipedia
from explanation_text.explanation_generators.explanation_generator_geoguesser.overview import generate_overview_text
from explanation_text.explanation_generators.explanation_generator_geoguesser.sentence_construction import \
    generate_sentence_construction_medium, generate_main_label_explanation, generate_part_label_explanation
from explanation_text.explanation_generators.rephraser import rephrase

PRINT_COMPONENT_TEXTS = False
REPHRASE_DETAILED = True


def generate_gg_overview(location):
    overview_text = generate_overview_text(location)
    if PRINT_COMPONENT_TEXTS:
        print("")
        print("Individual parts of explanation text before rephrasing:")
        print("  Overview text: " + overview_text)
    return overview_text


def generate_gg_medium(single_object, api_token, fallback):
    # Generate first location description
    location_information = generate_main_label_explanation(single_object)

    # for each part generate additional sentence
    part_label_information = ""
    for part in single_object['parts']:
        part_label_information += generate_part_label_explanation(part) + " "

    medium_text = location_information + " " + part_label_information

    if PRINT_COMPONENT_TEXTS:
        print("  Sentence Construction Text: " + medium_text)
    if fallback:
        return medium_text
    rephrase_text = rephrase("strict", medium_text, api_token)
    return rephrase_text


def generate_gg_detailed(single_object, api_token, google_vision_api_key, fallback):

    # generate basic location information
    location_information = generate_main_label_explanation(single_object)
    location_information += get_first_sentence_wikipedia(single_object.get("label").capitalize())
    if not fallback:
        location_information = rephrase("strict", location_information, api_token)

    if PRINT_COMPONENT_TEXTS:
        print("  Detailed Location Information text: " + location_information)

    # for each part generate additional sentence
    part_label_information = ""
    knowledge_base_information = ""
    for part in single_object['parts']:
        part_label_information += generate_part_label_explanation(part) + " "
        if not fallback:
            knowledge_base_information += generate_part_information(google_vision_api_key != "",
                                                                    single_object.get('label'), part, api_token,
                                                                    google_vision_api_key) + " "

    if PRINT_COMPONENT_TEXTS:
        print("  Detailed Part Label Information text: " + part_label_information)
        print("  Detailed Knowledge Base Information text: " + knowledge_base_information)

    if not fallback:
        part_label_information = rephrase("strict", part_label_information, api_token)
    if knowledge_base_information != "":
        knowledge_base_information = rephrase("strict", knowledge_base_information, api_token)

    total_part_information = part_label_information + " " + knowledge_base_information

    if PRINT_COMPONENT_TEXTS:
        print("")

    return location_information + " " + total_part_information
