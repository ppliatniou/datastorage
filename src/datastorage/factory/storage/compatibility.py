from utils.exceptions import DetailedValidationError

__all__ = (
    'is_compatible'
)


def is_compatible(left, right):
    """
    :param left: previous schema definition
    :param right: current schema definition
    :return: bool
    """
    if left == right:
        return True
    
    if left["key"] != right["key"]:
        raise DetailedValidationError(
            detail="Key definitions aren't equivalent: confilct with {}".format(left["key"])
        )
    left_fields = dict((f["name"], f) for f in left["fields"])
    right_fields = dict((f["name"], f) for f in right["fields"])
    
    for name, item in left_fields.items():
        if name in right_fields and left_fields[name] == right_fields[name]:
            del right_fields[name]
        elif name in right_fields and left_fields[name] != right_fields[name]:
            raise DetailedValidationError(
                detail="Field name '{}' conflict with {}".format(name, left_fields[name])
            )
        else:
            raise DetailedValidationError(
                detail="Field name '{}' should be defined in field definition".format(name)
            )
    
    for new_field in right_fields.values():
        if "default" not in new_field:
            raise DetailedValidationError(
                detail="Field name '{}' should be defined with default value".format(new_field["name"])
            )
    
    return True
