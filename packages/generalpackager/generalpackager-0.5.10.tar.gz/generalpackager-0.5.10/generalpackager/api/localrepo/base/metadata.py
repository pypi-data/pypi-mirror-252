from generalfile import ConfigFile
from generallibrary import Ver
from generalpackager.api.shared.target import _TARGETS_LITERAL, _DEFAULT_TARGET


class _Metadata(ConfigFile):
    enabled = True
    private = False
    name = None
    target: _TARGETS_LITERAL = _DEFAULT_TARGET
    version = Ver("0.0.1")
    description = "Missing description."
    topics = []
    manifest = []
    contribute = False

    def _assert_correct_class_for_target(self):
        assert type(self).__name__.lower().endswith(self.target), f"{self} tried to write but its class name '{type(self).__name__}' doesn't end with its target '{self.target}'."

    def write_hook_pre(self, dict_):
        if self.target:
            self._assert_correct_class_for_target()
