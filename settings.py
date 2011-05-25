import sys

COMPULSORY_SETTINGS = ['NAME','MODULES']

class ValidationError(Exception):
    pass


class Settings(object):
    def __init__(self):
        self.settings_module = sys.argv[1]
        self.modules = []
        self.load_settings()
        self.import_modules()
        self.update_compulsory()
        self.validate_settings()

    def load_settings(self):
        try:
            self.settings = __import__(self.settings_module)
        except ImportError:
            raise ValidationError("Cannot import settings file %s" % self.settings_module)

    def import_modules(self):
        for module in self.settings.MODULES:
            try:
                self.modules.append(__import__(module))
            except ImportError:
                raise ValidationError("Cannot import module %s" % module)

    def update_compulsory(self):
        for module in self.modules:
            COMPULSORY_SETTINGS.append(getattr(module, 'COMPULSORY_SETTINGS', []))

    def validate_settings(self):
        for setting in COMPULSORY_SETTINGS:
            if not hasattr(self.settings, setting):
                raise ValidationError("%s must be specified in settings module" % setting)
        for setting in dir(self.settings):
            value = getattr(self.settings, setting)
            Validator.validate(setting, value)
            for module in self.modules:
                if hasattr(module, 'Validator'):
                    module.Validator.validate(setting, value)

    def get_settings_and_modules(self):
        return self.settings, self.modules


def get_setting(name, default=None):
    if default:
        return getattr(settings, name, default)
    else:
        return getattr(settings, name)

class Validator(object):
    @staticmethod
    def validate(name, value):
        getattr(Validator, 'validate_' + name, lambda x: None)(value)

    @staticmethod
    def validate_MODULES(value):
        if not (isinstance(value, list) or isinstance(value, tuple)):
            raise ValidationError('MODULES must be tuple or list (got %s)' % type(value))

settings, modules = Settings().get_settings_and_modules()