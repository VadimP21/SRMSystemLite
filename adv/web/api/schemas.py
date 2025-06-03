from marshmallow import Schema, EXCLUDE, fields, validate, missing


class CreateAdvSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    name = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    chanel = fields.Str(
        required=True,
        validate=validate.OneOf(["Google", "VK", "TG", "YouTube", "Yandex"]),
    )
    cost = fields.Decimal(
        places=2, as_string=True, required=True, validate=validate.Range(min=1.00)
    )
    product_id = fields.Integer(required=True)


class GetAdvSchema(CreateAdvSchema):
    id = fields.Int(required=True)
    created_at = fields.DateTime()


class GetAdsSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    ads = fields.List(fields.Nested(GetAdvSchema), required=True)


class GetAdsParameters(Schema):
    class Meta:
        unknown = EXCLUDE

    limit = fields.Int(load_default=10, validate=validate.Range(min=10, max=50))
    offset = fields.Int(load_default=0, validate=validate.Range(min=0, max=50))
    sort_field = fields.Str()
    sort_order = fields.Str(
        load_default="asc", validate=validate.OneOf(["asc", "desc"])
    )
    since = fields.DateTime(format="iso")
