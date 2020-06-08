from django.core.exceptions import ValidationError
from django.test import TestCase

from nupe.core.models import City, Location, State
from nupe.core.models.Location import CITY_MAX_LENGTH, STATE_MAX_LENGTH
from resources.const.datas.Location import CITY_NAME, STATE_NAME


class CityTestCase(TestCase):
    def test_create_valid(self):
        city = City.objects.create(name=CITY_NAME)

        self.assertNotEqual(city.id, None)  # o objeto criado deve conter um id
        self.assertEqual(city.name, CITY_NAME)  # o objeto criado deve conter o nome fornecido
        self.assertEqual(City.objects.all().count(), 1)  # o objeto deve ser criado no banco de dados
        self.assertEqual(city.full_clean(), None)  # o objeto não deve conter erros de validação

    def test_create_invalid_max_length(self):
        # passar do limite de caracteres deve emitir erro de validação
        with self.assertRaises(ValidationError):
            City(name=CITY_NAME * CITY_MAX_LENGTH).clean_fields()

    def test_create_invalid_null(self):
        # deve emitir erro de que o campo não pode ser nulo
        with self.assertRaises(ValidationError):
            City(name=None).clean_fields()

    def test_create_invalid_blank(self):
        # deve emitir erro de que o campo é obrigatório
        with self.assertRaises(ValidationError):
            City().clean_fields()

        # deve emitir erro de que o campo não pode ser em branco
        with self.assertRaises(ValidationError):
            City(name="").clean_fields()

        # deve emitir erro de que o campo não pode ser em branco porque espaços são ignorados
        with self.assertRaises(ValidationError):
            City(name=" ").clean_fields()

    def test_create_invalid_unique_name(self):
        # deve emitir erro porque só pode conter um único objeto com o mesmo nome
        with self.assertRaises(ValidationError):
            City.objects.create(name=CITY_NAME)
            City(name=CITY_NAME).validate_unique()

    def test_no_delete(self):
        city = City.objects.create(name=CITY_NAME)
        state = State.objects.create(name=STATE_NAME)

        # a relação entre os objetos deve ser criada
        state.cities.add(city)
        self.assertEqual(state.cities.all().count(), 1)

        city.delete()
        # o objeto não deve ser mascarado e nem excluído do banco de dados
        self.assertEqual(City.objects.all().count(), 1)

        # a relação deve permanecer
        self.assertEqual(state.cities.all().count(), 1)


class StateTestCase(TestCase):
    def test_create_valid(self):
        state = State.objects.create(name=STATE_NAME)

        self.assertNotEqual(state.id, None)
        self.assertEqual(state.name, STATE_NAME)
        self.assertEqual(State.objects.all().count(), 1)
        self.assertEqual(state.full_clean(), None)

    def test_create_invalid_max_length(self):
        with self.assertRaises(ValidationError):
            State(name=STATE_NAME * STATE_MAX_LENGTH).clean_fields()

    def test_create_invalid_null(self):
        with self.assertRaises(ValidationError):
            State(name=None).clean_fields()

    def test_create_invalid_blank(self):
        with self.assertRaises(ValidationError):
            State().clean_fields()

        with self.assertRaises(ValidationError):
            State(name="").clean_fields()

        with self.assertRaises(ValidationError):
            State(name=" ").clean_fields()

    def test_create_invalid_unique_name(self):
        with self.assertRaises(ValidationError):
            State.objects.create(name=STATE_NAME)
            State(name=STATE_NAME).validate_unique()

    def test_no_delete(self):
        state = State.objects.create(name=STATE_NAME)
        city = City.objects.create(name=CITY_NAME)

        city.states.add(state)
        self.assertEqual(city.states.all().count(), 1)

        state.delete()
        self.assertEqual(State.objects.all().count(), 1)
        self.assertEqual(city.states.all().count(), 1)


class LocationTestCase(TestCase):
    def setUp(self):
        # cria no banco de dados de test antes de executar os tests
        City.objects.create(name=CITY_NAME)
        State.objects.create(name=STATE_NAME)

    def test_create_valid(self):
        city = City.objects.get(name=CITY_NAME)
        state = State.objects.get(name=STATE_NAME)

        location = Location.objects.create(city=city, state=state)

        self.assertNotEqual(location.id, None)
        self.assertEqual(location.city, city)
        self.assertEqual(location.state, state)
        self.assertEqual(Location.objects.all().count(), 1)
        self.assertEqual(location.full_clean(), None)

    def test_create_invalid_null(self):
        with self.assertRaises(ValidationError):
            Location(city=None).clean_fields()

        with self.assertRaises(ValidationError):
            Location(state=None).clean_fields()

    def test_create_invalid_city_and_state_instance(self):
        # deve emitir um erro porque deve ser fornecido uma instancia de objeto do respectivo field

        with self.assertRaises(ValueError):
            Location.objects.create(city="")

        with self.assertRaises(ValueError):
            Location.objects.create(state="")

        with self.assertRaises(ValueError):
            Location.objects.create(city=1)

        with self.assertRaises(ValueError):
            Location.objects.create(state=1)

    def test_create_invalid_city_and_state_unique_together(self):
        city = City.objects.get(name=CITY_NAME)
        state = State.objects.get(name=STATE_NAME)

        # deve emitir um erro porque só pode exitir um objeto com a mesma cidade e estado
        with self.assertRaises(ValidationError):
            Location.objects.create(city=city, state=state)
            Location(city=city, state=state).validate_unique()

    def test_no_delete(self):
        state = State.objects.get(name=STATE_NAME)
        city = City.objects.get(name=CITY_NAME)

        location = Location.objects.create(city=city, state=state)

        location.delete()
        self.assertEqual(Location.objects.all().count(), 1)
