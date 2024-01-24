import random

# Sentence templates

main_sentences = [
    "The image was classified as {0}.",
    "The image was identified as {0}.",
    "The image's location was classified as {0}.",
    "The image's location was determined to be {0}.",
    "The image's location has been determined to be {0}.",
    "The image's geographical origin has been classified as {0}.",
    "The location of the image was classified as {0}.",
    "The location of the image was determined to be {0}.",
    "The identified location for this image is {0}.",
    "The model identified the image as {0}.",
    "The model classified the image as {0}.",
    "The model classified the location of the image as {0}.",
    "The model determined that the image was captured in {0}.",
    "The model determined that the image was most likely captured in {0}.",
    "Our model classified the image as {0}.",
    "Our system classified the image as {0}.",
    "Our system determined that the image was most likely captured in {0}."
]

main_sentences_with_probability = [
    "The image was classified as {0} with {1}% certainty.",
    "The image was identified as {0} with a confidence of {1}%.",
    "The image's location was classified as {0} with a probability of {1}%.",
    "The image's location was determined to be {0} with {1}% certainty.",
    "The image's geographical origin has been classified as {0} with {1}% certainty.",
    "The location of the image was classified as {0} with a probability of {1}%.",
    "The location of the image was determined to be {0} with {1}% certainty.",
    "The identified location for this image is {0} with a {1}% confidence level.",
    "The model classified the image as {0} with {1}% certainty.",
    "The model classified the location of the image as {0} with {1}% confidence.",
    "The model determined that the image was most likely captured in {0} with {1}% confidence.",
]

# old sentences
part_sentences = [
    "The location was identified because of the {0} in the image.",
    "The location was identified due to the {0} in the image.",
    "{0} was/were detected in the image.",
    "The classification was influenced by {0} in the image.",
    "The {0} in the image influenced the classification.",
    "The {0} in the image influenced the classification decision.",
    "The model's decision was influenced by {0} in the image.",
    "{0} was/were relevant for the identification of the location.",
]

part_first_sentences = [
    "The classification was influenced by the presence of the {0} in the image.",
    "The model's decision was influenced by the presence of the {0} in the image.",
    "The classification decision was influenced by the {0} in the image.",
    "The model's decision was shaped by the presence of the {0} in the image."
]

part_subsequent_sentences = [
    "The {0} in the image also influenced the classification.",
    "The {0} in the image also influenced the classification decision.",
    "Also, the {0} in the image contributed to the classification decision.",
    "The {0} also played a significant role in the model's decision.",
    "The {0} detected in the image contributed to the classification outcome as well.",
    "The {0} in the image played a crucial role in influencing the classification.",
    "The {0} further influenced the classification decision.",
    "In addition, the {0} in the image influenced the model's decision.",
    "Furthermore, the {0} in the image played a significant role in the classification outcome.",
]

part_first_sentences_with_relevancy = [
    "The classification was influenced by the presence of the {0} in the image with a relevance of {1}%.",
    "The model's decision was influenced by the presence of the {0} in the image with {1}% relevance.",
    "The classification decision was influenced by the {0} in the image with {1}% relevance.",
    "The model's decision was influenced by the {0} in the image with a relevance of {1}%.",
    "The location of the image was identified due to the {0} with {1}% relevance.",
    "The image's location was identified due to the {0} with a relevance of {1}%.",
]

part_subsequent_sentences_with_relevancy = [
    "The {0} in the image also influenced the classification with a relevance of {1}%.",
    "The {0} in the image also influenced the classification decision with {1}% relevance.",
    "The {0} in the image contributed to the classification decision with {1}% relevance.",
    "The {0} also played a significant role in the model's decision with a relevance of {1}%.",
    "The {0} detected in the image contributed to the classification outcome with {1}% relevance.",
    "The {0} further influenced the classification decision with {1}% relevance.",
    "In addition, the {0} in the image influenced the model's decision with {1}% relevance.",
    "Furthermore, the {0} in the image played a significant role in the classification outcome with a relevance of {1}%.",
    "The {0} in the image had {1}% relevance for the classification.",
    "The {0} in the image was {1}% relevant for the classification decision.",
    "With {1}% relevance, the classification was further influenced by the {0} in the image.",
    "With a relevance of {1}%, the model's decision was also influenced by the {0} in the image.",
]


def generate_sentence_construction_medium(single_object):
    """
    Method for medium explanation with sentence construction for GeoGuesser
    Gets random main sentence from list with fixed part sentences.s
    """

    explanation = generate_main_label_explanation(single_object)

    # part labels sentence
    if 'parts' not in single_object:
        return explanation[:-1]

    # Start of the second sentence
    part_explanation = " The location was mainly identified that way, because of the "

    # sentence part for each part label
    for part in single_object.get('parts'):

        part_label = part.get('part_label')
        part_explanation += str(part_label)

        if 'relevance' in part:
            relevance = part.get('relevance')
            part_explanation += " with " + str(relevance) + "% relevance"
        part_explanation += ", "

    # fix format of last part explanation and return explanation
    explanation += format_explanation(part_explanation, single_object)

    return explanation


def generate_main_label_explanation(single_object):
    """
    Method to construct main label sentence
    """

    if len(single_object) < 1:
        return ""
    location = single_object.get('label').capitalize()

    if 'probability' in single_object:
        probability = single_object.get('probability')
        return random.choice(main_sentences_with_probability).format(location, probability)
    else:
        return random.choice(main_sentences).format(location)


def generate_part_label_explanation(part, is_first_part):
    """
    Method to construct part label sentence
    """
    part_label = part.get('part_label').replace('_', ' ')

    if 'relevance' in part:
        relevance = part.get('relevance')
        if is_first_part:
            return random.choice(part_first_sentences_with_relevancy).format(part_label, relevance)
        else:
            return random.choice(part_subsequent_sentences_with_relevancy).format(part_label, relevance)

    if is_first_part:
        return random.choice(part_first_sentences).format(part_label)
    else:
        return random.choice(part_subsequent_sentences).format(part_label)


def format_explanation(explanation, single_object):
    """
    Method fix format issues with last part explanation sentence.
    Add dot at the end and replace last comma with 'and'.
    """
    if explanation.endswith(" "):
        explanation = explanation[:-2] + "."

    if 'parts' in single_object:
        last_comma_index = explanation.rfind(",")
        explanation = explanation[:last_comma_index] + " and" + explanation[last_comma_index + 1:]

    return explanation


def float_to_percentage(a):
    """
    Method parse float string to percentage string
    """
    try:
        return str(round(float(a) * 100))
    except ValueError:
        return "0.0"
