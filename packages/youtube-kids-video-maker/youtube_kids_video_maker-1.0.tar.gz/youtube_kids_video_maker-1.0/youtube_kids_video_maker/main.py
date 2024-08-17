import random

def select_content(age_group, category, duration):
    """
    Selects appropriate content for a YouTube Kids video based on given parameters.
    
    :param age_group: str, age group of the target audience (e.g., "preschool", "school-age")
    :param category: str, category of content (e.g., "educational", "entertainment")
    :param duration: int, desired duration of the video in minutes
    :return: dict, selected content details
    """
    # This is a simplified example. In a real scenario, this might involve
    # database queries, API calls, or complex selection algorithms.
    
    content_database = {
        "preschool": {
            "educational": ["Counting with Animals", "Colors in Nature"],
            "entertainment": ["Nursery Rhymes", "Animated Stories"]
        },
        "school-age": {
            "educational": ["Science Experiments", "History Facts"],
            "entertainment": ["Kids' Quiz Show", "Craft Ideas"]
        }
    }
    
    try:
        available_content = content_database[age_group][category]
        selected_content = random.choice(available_content)
        
        return {
            "title": selected_content,
            "age_group": age_group,
            "category": category,
            "duration": duration
        }
    except KeyError:
        return {"error": "Invalid age group or category"}

# Example usage
content = select_content("preschool", "educational", 10)
print(content)
