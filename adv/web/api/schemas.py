from marshmallow import Schema, EXCLUDE, fields, validate


class CreateAdvSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    chanel = fields.Str(required=True, validate=validate.OneOf(["Google", "VK", "TG", "YouTube", "Yandex"]))
    cost = fields.Decimal(
        places=2,
        as_string=True,
        required=True,
        validate=validate.Range(min=1.00)
    )
    product_id = fields.Integer(required=True)

    class Meta:
        unknown = EXCLUDE

class GetAdvSchema(CreateAdvSchema):
    id = fields.Int(required=True)
    created_at = fields.DateTime()