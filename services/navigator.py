def click_button(button_text, elements):
    for button in elements.buttons:
        if button_text.lower() in button['text'].lower():
            return f"Simulated click on button: '{button['text']}'"
    return "Button not found."

def fill_input(field_name, value, elements):
    for input_field in elements.inputs:
        if input_field['name'] and field_name.lower() in input_field['name'].lower():
            return f"Filled '{field_name}' with '{value}'"
    return "Input field not found."
