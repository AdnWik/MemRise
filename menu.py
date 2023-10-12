"""Menu function"""


def show_menu(menu_options: list,
              submenu_name='',
              start_message='',
              end_message=''
              ) -> str:
    """"Create menu with numbered options and optionally submenu name,
        start and stop message

    Args:
        menu_options (list): options to show and numbered
        submenu_name (str, optional): submenu name.
        start_message (str, optional): message before numbered options.
        end_message (str, optional): message after numbered options.

    Returns:
        str: _description_
    """
    if submenu_name:
        result = submenu_name.upper().center(50, '-') + '\n'
    else:
        result = ''

    if start_message:
        result += start_message + '\n\n'

    if menu_options:
        for number, option in enumerate(menu_options, 1):
            result += f'{number} - {option}\n'

    if end_message:
        result += '\n' + end_message
    else:
        result += '\nOther - EXIT'

    return result
