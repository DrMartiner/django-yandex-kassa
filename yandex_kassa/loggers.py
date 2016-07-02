# -*- coding: utf-8 -*-

import json
import logging


class ErrorsFilter(logging.Filter):
    def filter(self, record):
        errors = getattr(record, 'errors', None)
        if errors:
            if isinstance(errors, dict):
                try:
                    record.errors = json.dumps(errors,
                                               encoding='utf8',
                                               ensure_ascii=False)
                except:
                    pass
            else:
                record.errors = errors
        else:
            record.errors = ''

        return True
