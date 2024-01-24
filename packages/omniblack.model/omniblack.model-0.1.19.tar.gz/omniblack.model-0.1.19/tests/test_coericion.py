from string import capwords

from pytest import fixture, raises

from omniblack.model import CoercionError, Model
from omniblack.model.types import TypeDef, native_adapter


def create_test_field(name, type):
    display = capwords(name.replace('_', ' '))
    return dict(
        name=name,
        display=dict(en=display),
        desc=dict(en=display),
        type=type,
    )


top_struct = {
    'name': 'top_level',
    'display': {'en': 'Top Level'},
    'fields': [
        create_test_field('field_1', 'integer'),
        create_test_field('test_type_field', 'test_type'),
    ],
}


def return_true(*args, **kwargs):
    return True


@fixture
def model():
    model = Model(__name__)
    model.structs(top_struct)
    test_type = TypeDef(
        name='test_type',
        implementation=int,
        adapters=dict(json=native_adapter),
        validator=return_true,
        attributes=tuple(),
    )
    model.types(**test_type.dict)

    return model


pre_rec = {
    'field_1': 1,
    'test_type_field': 1,
}

expected_post_rec = {
    'field_1': '1',
    'test_type_field': 1,
}


def test_to(model):
    # simple conversion works
    indiv = model.structs.top_level(pre_rec)
    post = model.coerce_to(indiv, 'json')
    assert post == expected_post_rec

    with raises(CoercionError):
        model.coerce_to(indiv, 'string')


def test_from(model):
    expected_post_indiv = model.structs.top_level(pre_rec)
    post_indiv = coerce_from(model, expected_post_rec, 'json', 'top_level')
    assert post_indiv == expected_post_indiv
