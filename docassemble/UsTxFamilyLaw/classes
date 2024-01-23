"""
classes.py - Classes introduced by UsTxFamilyLaw
"""
from datetime import date
from docassemble.base.util import DAObject

__all__ = ['BankAccount']

class BankAccount(DAObject):
    """A bank account"""
    def init(self, *pargs, **kwargs):
        super().init(*pargs, **kwargs)

    def short_name(self):
        if self.short_name:
            return self.short_name
        return f'{self.institution_name} {self.account_number[-4:]}'
