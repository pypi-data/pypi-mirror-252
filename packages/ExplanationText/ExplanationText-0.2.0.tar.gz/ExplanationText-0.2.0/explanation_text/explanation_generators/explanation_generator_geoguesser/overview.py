import random

# sentence templates

overview_sentences = ["The location of the image was classified as {0}.",
                      "The identified location for this image is {0}.",
                      "The image's location was classified as {0}.",
                      "The image's geographical origin has been classified as {0}.",
                      "The image's location was determined to be {0}.",
                      "The location of the image was determined to be {0}.",
                      "The image was classified as {0}.",
                      "Our system determined that the image was captured in {0}.",
                      "The model determined that the image was captured in {0}.",
                      "Our model classified the image as {0}.",
                      "Our system classified the image as {0}.",
                      "The image's location has been determined to be {0}.",
                      "The model identified the image as {0}.",
                      "The image was identified as {0}.",
                      "The image was classified as {0}."]

# Removed sentence "The view was classified as {0}."


def generate_overview_text(location):
    """
    Method to generate overview text for GeoGuesser
    """

    if len(location) != 1:
        return "There was a problem with the classification of the image."

    country_name = location[0].capitalize()

    return random.choice(overview_sentences).format(country_name)
