from marshmallow import Schema, EXCLUDE, fields, validate, missing


class CreateLeadSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    name = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    first_name = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    phone = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    email = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    product_id = fields.Integer(required=True)


class GetLeadSchema(CreateLeadSchema):
    id = fields.Int(required=True)
    is_active = fields.Boolean(required=True, load_default=False)
    is_archived = fields.Boolean(required=True, load_default=True)


class GetLeadsSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    leads = fields.List(fields.Nested(GetLeadSchema), required=True)


class GetLeadsParameters(Schema):
    class Meta:
        unknown = EXCLUDE

    limit = fields.Int(load_default=10, validate=validate.Range(min=10, max=50))
    offset = fields.Int(load_default=0, validate=validate.Range(min=0, max=50))
    sort_field = fields.Str()
    sort_order = fields.Str(
        load_default="asc", validate=validate.OneOf(["asc", "desc"])
    )
