import random


def generate_random_color():
    """Generates a random color, excluding black and white."""
    while True:
        # Generate a random hexadecimal color
        color = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        # Exclude black (#000000) and white (#FFFFFF)
        if color.lower() not in ['#000000', '#ffffff']:
            return color
