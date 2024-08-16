from marshmallow import (
    Schema,
    fields,
    validate,
)


class FigureResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    file_id = fields.Integer(required=True)
    source_type = fields.String(required=True)
    source_id = fields.Integer(required=True)
    figure_label = fields.String(allow_none=True)
    figure_caption = fields.String(allow_none=True)
    figure_description = fields.String(allow_none=True)
    figure_link = fields.String(allow_none=True)
    llm_processed = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime()
