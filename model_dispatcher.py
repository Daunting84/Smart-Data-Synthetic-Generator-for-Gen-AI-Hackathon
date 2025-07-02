def decide_model(schema):
    """
    Decide whether to use a tabular model (ctgan) or a text generator
    based on the schema profile.
    """
    has_numeric = False
    has_text = False

    for props in schema.values():
        col_type = props.get("type", "")
        if col_type in ["integer", "float"]:
            has_numeric = True
        elif col_type == "text":
            has_text = True

    if has_numeric:
        return "ctgan"
    elif has_text and not has_numeric:
        return "textgen"
    else:
        return "unknown"