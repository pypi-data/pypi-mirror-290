from __future__ import annotations
import typing as _t
import pydantic as _pydantic
import tinytable as _tt

from pydantable import errors


def validate_table(
    table: _tt.Table,
    model: _t.Type[_pydantic.BaseModel]
) -> _tt.Table:
    out_table: _tt.Table = table.copy()
    validation_errors: list[dict] = []
    errored = False
    for i, row in table.iterrows():
        try:
            validated_row: _pydantic.BaseModel = model.model_validate(dict(row))
            if not errored:
                out_table[i] = dict(validated_row)
        except _pydantic.ValidationError as e:
            validation_errors.extend(e.errors())
            errored = True
    if validation_errors:
        grouped_errors: list[dict] = errors.group_errors(validation_errors)
        raise errors.ValidationErrors(grouped_errors)
    return out_table
    

class BaseTableModel(_pydantic.BaseModel):
    # TODO: Add __init__ for reading dict
    # TODO: Add read_dict class method
    
    @classmethod
    def read_csv(cls, path: str) -> _tt.Table:
        tbl: _tt.Table = _tt.read_csv(path)
        return validate_table(tbl, cls)