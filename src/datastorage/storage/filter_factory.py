from django_filters import rest_framework as filters


def ModelFilter(storage, model):
    FilterMeta = type(
        "Meta",
        (),
        {
            "model": model,
            "fields": storage.get_index_names()
        }
    )
    FilterClass = type(
        "{}Filter".format(storage.name.lower().capitalize()),
        (filters.FilterSet,),
        {
            "Meta": FilterMeta
        }
    )
    return FilterClass