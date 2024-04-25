def model_to_dict(model):
    return {c.key: getattr(model, c.key) for c in model.__mapper__.column_attrs}
