import re
import ast


class Guardor(object):
    _hidden_keywords = r'TOKEN|PASS|Authorization'
    _cleansed_title = r'********************'
    _sensive_regex = re.compile(_hidden_keywords, re.IGNORECASE)

    @staticmethod
    def _str2obj(raw_data):
        try:
            if isinstance(raw_data, basestring):
                obj = ast.literal_eval(raw_data)
            else:
                obj = raw_data
        except Exception:
            # maybe we should log sth.
            return raw_data

        if isinstance(obj, list):
            return map(Guardor._str2obj, obj)
        elif isinstance(obj, tuple):
            return tuple(map(Guardor._str2obj, obj))
        elif isinstance(obj, dict):
            return {k: Guardor._str2obj(v) for k, v in obj.items()}
        else:
            return obj

    @staticmethod
    def mask_sensive(raw_data):
        def _sensive2cleansed(key, value):
            try:
                if Guardor._sensive_regex.search(key):
                    cleansed = Guardor._cleansed_title
                else:
                    cleansed = value
            except TypeError:
                # If the key isn't regex-able, just return as-is.
                cleansed = value
            return cleansed

        if isinstance(raw_data, list):
            return map(Guardor.mask_sensive, raw_data)
        elif isinstance(raw_data, tuple):
            return tuple(map(Guardor.mask_sensive, raw_data))
        elif isinstance(raw_data, dict):
            return {k: Guardor.mask_sensive(_sensive2cleansed(k, v)) for k, v in raw_data.items()}
        else:
            return raw_data

    @staticmethod
    def cleanse_content(raw_data):
        data = Guardor._str2obj(raw_data)
        return Guardor.mask_sensive(data)
