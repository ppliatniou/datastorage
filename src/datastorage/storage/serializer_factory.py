from rest_framework.serializers import ModelSerializer


__all__ = (
    'Serializer',
)

BUILT_IN_FIELDS = ["created_at", "updated_at"]


def Serializer(storage, model):
    write_fields = [storage.get_key_field_name()]
    write_fields.extend(storage.get_field_names())
    fields = []
    fields.extend(write_fields)
    fields.append("version")
    fields.extend(BUILT_IN_FIELDS)
    SerializerMeta = type(
        "Meta",
        (),
        {
            "model": model,
            "read_only_fields": BUILT_IN_FIELDS,
            "fields": fields
        }
    )
    SerializerClass = type(
        "{}Serializer".format(storage.name.lower().capitalize()),
        (ModelSerializer,),
        {
            "Meta": SerializerMeta
        }
    )
    return SerializerClass
