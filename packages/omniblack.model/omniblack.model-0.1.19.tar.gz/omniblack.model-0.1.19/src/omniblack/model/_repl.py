from .model import Model


def configure_repl():
    model = Model(
        'Test Model',
        struct_packages=['omniblack.model.test_model'],
    )

    return locals()
