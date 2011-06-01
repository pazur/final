import glob
import sys

COMPULSORY_SETTINGS = ['MODULES', 'INPUT_FORMAT', 'INPUT_FILE', 'PIPELINE', 'SUMMARY', 'SUMMARY_FILE', 'SUMMARY_TYPE']

class ValidationError(Exception):
    pass


class Settings(object):
    def __init__(self):
        self.settings_module = sys.argv[1]
        self.modules = {}
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
                self.modules[module] = (__import__(module))
            except ImportError:
                raise ValidationError("Cannot import module %s" % module)

    def update_compulsory(self):
        for module in self.modules:
            compulsory = getattr(module, 'COMPULSORY_SETTINGS', [])
            COMPULSORY_SETTINGS.extend(compulsory)

    def validate_settings(self):
        for setting in COMPULSORY_SETTINGS:
            if not hasattr(self.settings, str(setting)):
                raise ValidationError("%s must be specified in settings module" % setting)
        for setting in dir(self.settings):
            value = getattr(self.settings, setting)
            SettingsValidator.validate(setting, value)
            for module in self.modules:
                if hasattr(module, 'SettingsValidator'):
                    module.SettingsValidator.validate(setting, value)

    def get_settings_and_modules(self):
        return self.settings, self.modules


class SettingsValidator(object):
    @staticmethod
    def validate(name, value):
        getattr(SettingsValidator, 'validate_' + name, lambda x: None)(value)

    @staticmethod
    def validate_MODULES(value):
        if not (isinstance(value, list) or isinstance(value, tuple)):
            raise ValidationError('MODULES must be tuple or list (got %s)' % type(value))

    @staticmethod
    def validate_INPUT_FORMAT(value):
        if not isinstance(value, basestring):
            raise ValidationError('INPUT_FORMAT must be string')

    @staticmethod
    def validate_INPUT_FILE(value):
        if not isinstance(value, basestring):
            raise ValidationError('INPUT_FILE must be string')
        found = glob.glob(value)
        if (not found) or (found != [value]):
            raise ValidationError('INPUT_FILE %s not found' % value)

    @staticmethod
    def validate_PIPELINE(value):
        if not (isinstance(value, list) or isinstance(value, tuple)):
            raise ValidationError('PIPELINE must be tuple or list (got %s)' % type(value))
        for step in value:
            if not (isinstance(step, tuple) or isinstance(step, list)):
                raise ValidationError('PIPELINE item must be a tuple or list')
            if len(step) != 3:
                raise ValidationError('PIPELINE item must have length 2')


def get_setting(name, *args):
    if args:
        return getattr(settings, name, args[0])
    else:
        return getattr(settings, name)

settings, modules = Settings().get_settings_and_modules()