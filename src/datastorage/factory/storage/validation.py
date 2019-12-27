from utils.exceptions import DetailedValidationError

__all__ = ('is_valid',)


def is_valid(definition):
    # TODO: check for reserved names: storage_meta, version and etc
    for f in definition["fields"]:
        if f["name"] == definition["key"]["name"]:
            raise DetailedValidationError(
                detail="Field name '{}' conflicts with key".format(f["name"])
            )
    return True