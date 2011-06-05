import os.path
import sys

import settings_validator

COMPULSORY_SETTINGS = [
    'MODULES',
    'INPUT_FORMAT',
    'INPUT_FILE',
    'PIPELINE',
    'SUMMARY',
    'SUMMARY_FILE',
    'SUMMARY_TYPE',
]

SUMMARY_TYPES = ['HUMAN_READABLE']

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
            raise settings_validator.ValidationError("Cannot import settings file %s" % self.settings_module)

    def import_modules(self):
        for module in self.settings.MODULES:
            try:
                self.modules[module] = (__import__(module))
            except ImportError:
                raise settings_validator.ValidationError("Cannot import module %s" % module)

    def update_compulsory(self):
        for module in self.modules:
            compulsory = getattr(module, 'COMPULSORY_SETTINGS', [])
            COMPULSORY_SETTINGS.extend(compulsory)

    def validate_settings(self):
        for setting in COMPULSORY_SETTINGS:
            if not hasattr(self.settings, str(setting)):
                raise settings_validator.ValidationError("%s must be specified in settings module" % setting)
        for setting in dir(self.settings):
            value = getattr(self.settings, setting)
            SettingsValidator(self.modules).validate(setting, value)
            for module in self.modules:
                if hasattr(module, 'SettingsValidator'):
                    module.SettingsValidator(self.modules).validate(setting, value)

    def get_settings_and_modules(self):
        return self.settings, self.modules


class SettingsValidator(settings_validator.SettingsValidator):
    def validate_MODULES(self, value):
        self.validate_list_or_tuple(value, 'MODULES')

    def validate_INPUT_FORMAT(self, value):
        self.validate_string(value, 'INPUT_FORMAT')

    def validate_INPUT_FILE(self, value):
        self.validate_file(value, 'INPUT_FILE')

    def validate_PIPELINE(self, value):
        self.validate_list_or_tuple(value, 'PIPELINE')
        for number, step in enumerate(value):
            self.validate_list_or_tuple(step, 'PIPELINE item')
            if len(step) != 3:
                raise settings_validator.ValidationError('PIPELINE item must have length 3')
            module, args, extra = step
            if module not in self.modules:
                raise settings_validator.ValidationError('PIPELINE: module %s not in MODULES' % module)
            for arg in extra:
                if arg not in self.modules[module].ARGUMENTS:
                    raise settings_validator.ValidationError('PIPELINE: module %s has no argument %s' % (module, arg))
            for (num, source) in args:
                if num >= number:
                    raise settings_validator.ValidationError('PIPELINE: source number greater than actual number (%d)' % number)
                if source not in self.modules[value[num][0]].RESULTS:
                    raise settings_validator.ValidationError('PIPELINE: source not in module output (%d)' % number)
                if args[(num, source)] not in self.modules[module].ARGUMENTS:
                    raise settings_validator.ValidationError('PIPELINE: module %s has no argument %s' % (module, args[(num, source)]))

    def validate_SUMMARY_FILE(self, value):
        self.validate_string(value, 'SUMMARY_FILE')

    def validate_SUMMARY_TYPE(self, value):
        if value not in SUMMARY_TYPES:
            raise settings_validator.ValidationError('SUMMARY_TYPE must be in ' + str(SUMMARY_TYPES))

    def validate_SUMMARY(self, value):
        self.validate_list_or_tuple(value, 'SUMMARY')
        for v in value:
            self.validate_list_or_tuple(v, 'SUMMARY ITEM')
            if len(v) != 2:
                raise settings_validator.ValidationError('SUMMARY ITEM length must be 2')

def get_setting(name, *args):
    if args:
        return getattr(settings, name, args[0])
    else:
        return getattr(settings, name)

def get_file(name, *args):
    if args:
        path = getattr(settings, name, args[0])
    else:
        path = getattr(settings, name)
    prefix = ''
    if hasattr(settings, 'PREFIX'):
        prefix = getattr(settings, 'PREFIX')
    if (not isinstance(path, basestring)) or os.path.isabs(path):
        return path
    else:
        return os.path.join(prefix, path)

def set_setting(name, value):
    setattr(settings, name, value)

settings, modules = Settings().get_settings_and_modules()