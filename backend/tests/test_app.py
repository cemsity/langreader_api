import pytest  
import flask


class TestApp:

    def test_app(self, app):
        print(type(app))
        assert type(app) is flask.app.Flask

    def test_ext(self, app):
        for i in app.extensions.keys():
            print(i)

        assert True is False