from datetime import datetime

from autonomous import log
from autonomous.db.autodb import Database


class ORM:
    _database = Database()

    def __init__(self, name, attributes):
        self.table = self._database.get_table(table=name, schema=attributes)
        self.name = name

    def _replace_pk_with_id(self, data):
        if isinstance(data, dict):
            for key in list(data.keys()):
                if key == "pk":
                    data["_id"] = data.pop("pk")
                else:
                    self._replace_pk_with_id(data[key])
                    # breakpoint()
        elif isinstance(data, list):
            for item in data:
                self._replace_pk_with_id(item)
        log(data)

    def _replace_id_with_pk(self, data):
        if isinstance(data, dict):
            for key in list(data.keys()):
                if key == "_id":
                    data["pk"] = data.pop("_id")
                else:
                    self._replace_pk_with_id(data[key])
                    # breakpoint()
        elif isinstance(data, list):
            for item in data:
                self._replace_pk_with_id(item)
        log(data)

    def save(self, data):
        self._replace_pk_with_id(data)
        if result := self.table.save(data):
            self._replace_id_with_pk(result)
        return result

    def get(self, pk):
        if result := self.table.get(pk):
            self._replace_id_with_pk(result)
        return result

    def all(self):
        if results := self.table.all():
            self._replace_id_with_pk(results)
        return results

    def search(self, **kwargs):
        self._replace_pk_with_id(kwargs)
        if results := self.table.search(**kwargs):
            self._replace_id_with_pk(results)

    def find(self, **kwargs):
        log(kwargs)
        self._replace_pk_with_id(kwargs)
        log(kwargs)
        if result := self.table.find(**kwargs):
            self._replace_id_with_pk(result)
        log(result)
        return result

    def random(self):
        if result := self.table.random():
            self._replace_id_with_pk(result)
        return result

    def delete(self, pk):
        return self.table.delete(_id=pk)

    def flush_table(self):
        return self.table.clear()


# class AutoEncoder:
#     @classmethod
#     def encode(cls, objs):
#         if isinstance(objs, dict):
#             obj_copy = {k: cls.encode(v) for k, v in objs.items()}
#         elif isinstance(objs, list):
#             obj_copy = [cls.encode(v) for v in objs]
#         else:
#             obj_copy = cls().default(objs)
#         return obj_copy

#     def default(self, o):
#         from autonomous.model.automodel import AutoModel

#         if issubclass(type(o), AutoModel):
#             name = "AutoModel"
#         else:
#             name = type(o).__name__

#         encoder_name = f"encode_{name}"

#         try:
#             encoder = getattr(self, encoder_name)
#         except AttributeError:
#             return o
#         else:
#             encoded = {"__extended_json_type__": name, "value": encoder(o)}

#         return encoded

#     def encode_datetime(self, o):
#         return o.isoformat()

#     def encode_AutoModel(self, o):
#         if o.pk:
#             return {
#                 "pk": o.pk,
#                 "_automodel": o.model_name(),
#             }
#         else:
#             log(
#                 o.__class__.__name__,
#                 "The above object was not been saved. You must save subobjects if you want them to persist.",
#             )
#             raise ValueError("Cannot encode unsaved AutoModel")


# class AutoDecoder:
#     @classmethod
#     def decode(cls, objs):
#         decoder = cls()
#         if isinstance(objs, dict):
#             if "__extended_json_type__" in objs:
#                 objs = decoder.default(objs)
#             else:
#                 for k, v in objs.items():
#                     objs[k] = cls.decode(v)
#         elif isinstance(objs, list):
#             for i, v in enumerate(objs):
#                 objs[i] = cls.decode(v)
#         return objs

#     def default(self, obj):
#         try:
#             name = obj["__extended_json_type__"]
#             decoder_name = f"decode_{name}"
#             decoder = getattr(self, decoder_name)
#         except (KeyError, AttributeError, TypeError):
#             return obj
#         else:
#             return decoder(obj)

#     def decode_datetime(self, o):
#         return datetime.fromisoformat(o["value"])

#     def decode_AutoModel(self, o):
#         obj = o["value"]
#         try:
#             from autonomous.model.automodel import DelayedModel

#             if not obj["pk"]:
#                 raise KeyError
#             return DelayedModel(obj["_automodel"], obj["pk"])
#         except KeyError:
#             log(
#                 "AutoModel",
#                 "The above object was not been saved. You must save subobjects if you want them to persist.",
#             )
#             raise ValueError("Cannot decode unsaved AutoModel")
