from marshmallow import Schema, validate, fields


class ParsSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=[validate.Length(max=100)])
    usd_price = fields.String(required=True, validate=[validate.Length(max=50)])
    city = fields.String(required=True, validate=[validate.Length(max=50)])
    description = fields.String(required=True, validate=[validate.Length(max=500)])
    message = fields.String(dump_only=True)

