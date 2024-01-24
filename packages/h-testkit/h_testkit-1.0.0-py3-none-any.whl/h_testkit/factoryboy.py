import tests  # pylint:disable=import-error


def set_factoryboy_sqlalchemy_session(db_session):
    from factory.alchemy import SQLAlchemyModelFactory

    sqlalchemy_factory_classes = [
        class_
        for class_ in tests.factories.__dict__.values()
        if isinstance(class_, type) and issubclass(class_, SQLAlchemyModelFactory)
    ]

    for class_ in sqlalchemy_factory_classes:
        class_._meta.sqlalchemy_session = db_session  # pylint:disable=protected-access
