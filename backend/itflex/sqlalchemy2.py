from datetime import date, datetime

from sqlalchemy import inspect
from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class SQLBase(object):
    def to_dict(self):
        data = {}
        for c in inspect(self).mapper.column_attrs:
            value = getattr(self, c.key)
            if isinstance(value, (datetime, date)):
                value = value.isoformat()

            data[c.key] = value

        return data

