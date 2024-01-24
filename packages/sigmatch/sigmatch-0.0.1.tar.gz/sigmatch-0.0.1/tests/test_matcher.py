import pytest

from sigmatch import SignatureMatcher, SignatureMismatchError


def test_random_functions():
    def function_1():
        pass
    def function_2(arg):
        pass
    def function_3(**kwargs):
        pass
    def function_4(*args, **kwargs):
        pass
    def function_5(a, b):
        pass
    def function_6(a, b, c):
        pass
    def function_7(a, b, c=False):
        pass
    def function_8(a, b, c=False, *d):
        pass
    def function_9(a, b, c=False, *d, **e):
        pass
    def function_10(a, b, c=False, c2=False, *d, **e):
        pass
    def function_11(a, b, b2, c=False, c2=False, *d, **e):
        pass
    def function_12(c=False, c2=False):
        pass

    assert SignatureMatcher().match(function_1) == True
    assert SignatureMatcher('.').match(function_2) == True
    assert SignatureMatcher('**').match(function_3) == True
    assert SignatureMatcher('*', '**').match(function_4) == True
    assert SignatureMatcher('.', '.').match(function_5) == True
    assert SignatureMatcher('.', '.', '.').match(function_6) == True
    assert SignatureMatcher('.', '.', 'c').match(function_7) == True
    assert SignatureMatcher('.', '.', 'c', '*').match(function_8) == True
    assert SignatureMatcher('.', '.', 'c', '*', '**').match(function_9) == True
    assert SignatureMatcher('.', '.', 'c', 'c2', '*', '**').match(function_10) == True
    assert SignatureMatcher('.', '.', '.', 'c', 'c2', '*', '**').match(function_11) == True
    assert SignatureMatcher('c', 'c2').match(function_12) == True

    assert SignatureMatcher('.').match(lambda x: None) == True
    assert SignatureMatcher('.', '.').match(lambda x, y: None) == True
    assert SignatureMatcher('.', '*').match(lambda x, *y: None) == True
    assert SignatureMatcher('.', '**').match(lambda x, **y: None) == True


def test_random_async_functions():
    async def function_1():
        pass
    async def function_2(arg):
        pass
    async def function_3(**kwargs):
        pass
    async def function_4(*args, **kwargs):
        pass
    async def function_5(a, b):
        pass
    async def function_6(a, b, c):
        pass
    async def function_7(a, b, c=False):
        pass
    async def function_8(a, b, c=False, *d):
        pass
    async def function_9(a, b, c=False, *d, **e):
        pass
    async def function_10(a, b, c=False, c2=False, *d, **e):
        pass
    async def function_11(a, b, b2, c=False, c2=False, *d, **e):
        pass
    async def function_12(c=False, c2=False):
        pass

    assert SignatureMatcher().match(function_1) == True
    assert SignatureMatcher('.').match(function_2) == True
    assert SignatureMatcher('**').match(function_3) == True
    assert SignatureMatcher('*', '**').match(function_4) == True
    assert SignatureMatcher('.', '.').match(function_5) == True
    assert SignatureMatcher('.', '.', '.').match(function_6) == True
    assert SignatureMatcher('.', '.', 'c').match(function_7) == True
    assert SignatureMatcher('.', '.', 'c', '*').match(function_8) == True
    assert SignatureMatcher('.', '.', 'c', '*', '**').match(function_9) == True
    assert SignatureMatcher('.', '.', 'c', 'c2', '*', '**').match(function_10) == True
    assert SignatureMatcher('.', '.', '.', 'c', 'c2', '*', '**').match(function_11) == True
    assert SignatureMatcher('c', 'c2').match(function_12) == True


def test_random_wrong_functions():
    def function_1():
        pass
    def function_2(arg):
        pass
    def function_3(**kwargs):
        pass
    def function_4(*args, **kwargs):
        pass
    def function_5(a, b):
        pass
    def function_6(a, b, c):
        pass
    def function_7(a, b, c=False):
        pass
    def function_8(a, b, c=False, *d):
        pass
    def function_9(a, b, c=False, *d, **e):
        pass
    def function_10(a, b, c=False, c2=False, *d, **e):
        pass
    def function_11(a, b, b2, c=False, c2=False, *d, **e):
        pass
    def function_12(c=False, c2=False):
        pass

    assert SignatureMatcher('.').match(function_1) == False
    assert SignatureMatcher('c').match(function_2) == False
    assert SignatureMatcher('.', '**').match(function_3) == False
    assert SignatureMatcher('.', '**').match(function_4) == False
    assert SignatureMatcher('.', 'c').match(function_5) == False
    assert SignatureMatcher('.', '.').match(function_6) == False
    assert SignatureMatcher('.', '.').match(function_7) == False
    assert SignatureMatcher('.', '.', 'c').match(function_8) == False
    assert SignatureMatcher('.', 'c', '*', '**').match(function_9) == False
    assert SignatureMatcher('.', '.', 'c2', '*', '**').match(function_10) == False
    assert SignatureMatcher('.', '.', 'c2', '*', '**').match(function_11) == False
    assert SignatureMatcher('c').match(function_12) == False


def test_random_wrong_async_functions():
    async def function_1():
        pass
    async def function_2(arg):
        pass
    async def function_3(**kwargs):
        pass
    async def function_4(*args, **kwargs):
        pass
    async def function_5(a, b):
        pass
    async def function_6(a, b, c):
        pass
    async def function_7(a, b, c=False):
        pass
    async def function_8(a, b, c=False, *d):
        pass
    async def function_9(a, b, c=False, *d, **e):
        pass
    async def function_10(a, b, c=False, c2=False, *d, **e):
        pass
    async def function_11(a, b, b2, c=False, c2=False, *d, **e):
        pass
    async def function_12(c=False, c2=False):
        pass

    assert SignatureMatcher('.').match(function_1) == False
    assert SignatureMatcher('c').match(function_2) == False
    assert SignatureMatcher('.', '**').match(function_3) == False
    assert SignatureMatcher('.', '**').match(function_4) == False
    assert SignatureMatcher('.', 'c').match(function_5) == False
    assert SignatureMatcher('.', '.').match(function_6) == False
    assert SignatureMatcher('.', '.').match(function_7) == False
    assert SignatureMatcher('.', '.', 'c').match(function_8) == False
    assert SignatureMatcher('.', 'c', '*', '**').match(function_9) == False
    assert SignatureMatcher('.', '.', 'c2', '*', '**').match(function_10) == False
    assert SignatureMatcher('.', '.', 'c2', '*', '**').match(function_11) == False
    assert SignatureMatcher('c').match(function_12) == False

    assert SignatureMatcher().match(lambda x: None) == False
    assert SignatureMatcher('.').match(lambda x, y: None) == False
    assert SignatureMatcher('*').match(lambda x, *y: None) == False
    assert SignatureMatcher('**').match(lambda x, **y: None) == False


def test_random_wrong_generator_functions():
    """
    Проверяем, что слепки сигнатур функций с неподходящими функциями не матчатся.
    """
    def function_1():
        yield None
    def function_2(arg):
        yield None
    def function_3(**kwargs):
        yield None
    def function_4(*args, **kwargs):
        yield None
    def function_5(a, b):
        yield None
    def function_6(a, b, c):
        yield None
    def function_7(a, b, c=False):
        yield None
    def function_8(a, b, c=False, *d):
        yield None
    def function_9(a, b, c=False, *d, **e):
        yield None
    def function_10(a, b, c=False, c2=False, *d, **e):
        yield None
    def function_11(a, b, b2, c=False, c2=False, *d, **e):
        yield None
    def function_12(c=False, c2=False):
        yield None

    assert SignatureMatcher('.').match(function_1) == False
    assert SignatureMatcher('c').match(function_2) == False
    assert SignatureMatcher('.', '**').match(function_3) == False
    assert SignatureMatcher('.', '**').match(function_4) == False
    assert SignatureMatcher('.', 'c').match(function_5) == False
    assert SignatureMatcher('.', '.').match(function_6) == False
    assert SignatureMatcher('.', '.').match(function_7) == False
    assert SignatureMatcher('.', '.', 'c').match(function_8) == False
    assert SignatureMatcher('.', 'c', '*', '**').match(function_9) == False
    assert SignatureMatcher('.', '.', 'c2', '*', '**').match(function_10) == False
    assert SignatureMatcher('.', '.', 'c2', '*', '**').match(function_11) == False
    assert SignatureMatcher('c').match(function_12) == False


def test_random_generator_functions():
    """
    Проверяем, что слепки сигнатур функций отрабатывают корректно.
    """
    def function_1():
        yield None
    def function_2(arg):
        yield None
    def function_3(**kwargs):
        yield None
    def function_4(*args, **kwargs):
        yield None
    def function_5(a, b):
        yield None
    def function_6(a, b, c):
        yield None
    def function_7(a, b, c=False):
        yield None
    def function_8(a, b, c=False, *d):
        yield None
    def function_9(a, b, c=False, *d, **e):
        yield None
    def function_10(a, b, c=False, c2=False, *d, **e):
        yield None
    def function_11(a, b, b2, c=False, c2=False, *d, **e):
        yield None
    def function_12(c=False, c2=False):
        yield None

    assert SignatureMatcher().match(function_1) == True
    assert SignatureMatcher('.').match(function_2) == True
    assert SignatureMatcher('**').match(function_3) == True
    assert SignatureMatcher('*', '**').match(function_4) == True
    assert SignatureMatcher('.', '.').match(function_5) == True
    assert SignatureMatcher('.', '.', '.').match(function_6) == True
    assert SignatureMatcher('.', '.', 'c').match(function_7) == True
    assert SignatureMatcher('.', '.', 'c', '*').match(function_8) == True
    assert SignatureMatcher('.', '.', 'c', '*', '**').match(function_9) == True
    assert SignatureMatcher('.', '.', 'c', 'c2', '*', '**').match(function_10) == True
    assert SignatureMatcher('.', '.', '.', 'c', 'c2', '*', '**').match(function_11) == True
    assert SignatureMatcher('c', 'c2').match(function_12) == True


def test_raise_exception_if_not_callable():
    with pytest.raises(ValueError, match='It is impossible to determine the signature of an object that is not being callable.'):
        SignatureMatcher().match('kek', raise_exception=True)


@pytest.mark.parametrize(
    'options',
    [
        {},
        {'raise_exception': False},
    ],
)
def test_not_raise_exception_if_not_callable(options):
    assert SignatureMatcher().match('kek', **options) == False


def test_raise_exception_if_dismatch():
    with pytest.raises(SignatureMismatchError):
        SignatureMatcher().match(lambda x: None, raise_exception=True)


@pytest.mark.parametrize(
    'options',
    [
        {},
        {'raise_exception': False},
    ],
)
def test_not_raise_exception_if_dismatch_and_flag_is_false(options):
    assert SignatureMatcher().match(lambda x: None, **options) == False


def test_it_works_with_class_based_callables():
    class LocalCallable:
        def __call__(self):
            pass

    assert SignatureMatcher().match(LocalCallable)
    assert not SignatureMatcher('.').match(LocalCallable)
