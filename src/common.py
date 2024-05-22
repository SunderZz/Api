def model_to_dict(model):
    return {c.key: getattr(model, c.key) for c in model.__mapper__.column_attrs}

url ="http://api.ipstack.com/check?access_key=e6b90ef1b887acd19f5921c37c45c00e"