import os.path

class ValidationError(Exception):
    pass

class SettingsValidator(object):
    def __init__(self, modules=()):
        self.modules = modules

    def validate(self, name, value):
        getattr(self, 'validate_' + name, lambda x: None)(value)

    def validate_file(self, path, name=''):
        self.validate_string(path, name)
        if not os.path.exists(path):
            raise ValidationError('%s: path %s does not exist' % (name, path))

    def validate_string(self, value, name=''):
        if not isinstance(value, basestring):
            raise ValidationError('%s must be string' % name)

    def validate_list_or_tuple(self, value, name=''):
        if not (isinstance(value, list) or isinstance(value, tuple)):
            raise ValidationError('%s must be tuple or list (got %s)' % (name, type(value)))