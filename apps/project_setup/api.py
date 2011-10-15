from project_setup import setup_menu_entry

setup_items = []


def register_setup(link):
    setup_items.append(link)
    setup_menu_entry['link'].setdefault('permissions', [])
    setup_menu_entry['link']['permissions'].extend(link.get('permissions', []))
