from formencode import Schema, validators, foreach


class Certificate(Schema):
    id = validators.Int()
    name = validators.String(min=3, max=30)
    username = validators.String(min=3, max=30)
    description = validators.String()
    groups = foreach.ForEach(validators.Int(), required=False, default=[])
    expiration = validators.Int()
    expirated_at = validators.DateValidator()
    created_at = validators.DateValidator()
    updated_at = validators.DateValidator()


