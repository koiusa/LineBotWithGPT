"""
Constant types in Python.
"""

import sys


class _const:
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const (%s)" % name)
        self.__dict__[name] = value


sys.modules[__name__] = _const()

# OpenAIモデル名（環境や用途に応じて変更可能）
OPENAI_MODEL = "gpt-4.1-turbo"
