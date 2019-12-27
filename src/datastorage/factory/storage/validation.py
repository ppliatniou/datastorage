from utils.exceptions import DetailedValidationError

__all__ = ('is_valid',)


RESERVED_NAMES = ['storage_meta', 'version', 'created_at', 'updated_at', 'key', "pk"]


def is_valid(definition):
    if definition["key"]["name"] in RESERVED_NAMES:
        raise DetailedValidationError(
            detail="Field name '{}' is reserved".format(definition["key"]["name"])
        )
    for f in definition["fields"]:
        if f["name"] == definition["key"]["name"]:
            raise DetailedValidationError(
                detail="Field name '{}' conflicts with key".format(f["name"])
            )
        if f["name"] in RESERVED_NAMES:
            raise DetailedValidationError(
                detail="Field name '{}' is reserved".format(f["name"])
            )
    return True