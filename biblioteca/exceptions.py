# -*- coding: utf-8 -*-

class EmprestarError(Exception):
    pass

class MaxEmprestimoError(EmprestarError):
    pass

class NoItensError(EmprestarError):
    pass

class AlreadyEmprestimoError(EmprestarError):
    pass

class ReservaError(Exception):
    pass