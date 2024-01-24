from pytest import fixture

from omniblack.model import Model


@fixture
def model():
    model = Model(__name__)
    print(model)
    return model


meta_names = {
    'struct',
    'field',
    'ui_string',
}


def test_load_from_package(model):
    assert not (set(model.structs) & meta_names)
    model.structs.load_model_package('omniblack.model.meta_model')
    assert len(set(model.structs) & meta_names) == len(meta_names)
