from project_tools import tools_menu_entry

tool_items = []


def register_tool(link):
    tool_items.append(link)
    tools_menu_entry['link'].setdefault('permissions', [])
    tools_menu_entry['link']['permissions'].extend(link.get('permissions', []))
