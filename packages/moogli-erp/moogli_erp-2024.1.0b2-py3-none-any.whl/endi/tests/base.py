class Dummy:
    def __init__(self, **kwargs):
        for key, value in list(kwargs.items()):
            setattr(self, key, value)


def printstatus(obj):
    """
    print an object's status regarding the sqla's session
    """
    from sqlalchemy.orm import object_session
    from sqlalchemy.orm.util import has_identity

    if object_session(obj) is None and not has_identity(obj):
        print("Sqlalchemy status : transient")
    elif object_session(obj) is not None and not has_identity(obj):
        print("Sqlalchemy status : pending")
    elif object_session(obj) is None and has_identity(obj):
        print("Sqlalchemy status : detached")
    elif object_session(obj) is not None and has_identity(obj):
        print("Sqlalchemy status : persistent")
    else:
        print("Unknown Status")
