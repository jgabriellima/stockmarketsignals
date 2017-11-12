from marshmallow import Schema, fields

class SignalsSchema(Schema):
    call = fields.Str(required=True)
    put = fields.Str(required=True)
    neutral = fields.Str(required=True)
