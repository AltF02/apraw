

class FullnameMixin:

    _kind = None

    @property
    def fullname(self):
        return "{}_{}".format(self._kind, self.id)