from marshmallow import (
    Schema,
    fields,
    validate,
)


class TableFigureResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    file_id = fields.Integer(required=True)
    source_type = fields.String(required=True)
    source_id = fields.Integer(required=True)
    label = fields.String(allow_none=True)
    caption = fields.String(allow_none=True)
    description = fields.String(allow_none=True)
    content = fields.String(allow_none=True)
    link = fields.String(allow_none=True)
    llm_processed = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime()
