"""
classes.py - Classes introduced by UsTxFamilyLaw
"""
# Ignore imoprt error on the next line.  It's a false positive.
from docassemble.base.util import DAObject  # type: ignore

__all__ = ['BankAccount', 'RetirementAccount']

class BankAccount(DAObject):
    """A bank account"""
    def init(self, *pargs, **kwargs):
        super().init(*pargs, **kwargs)

    def as_short_name(self):
        if isinstance(self.short_name, str):
            return self.short_name
        elif isinstance(self.account_number, str) and isinstance(self.institution_name, str):
            return f'{self.institution_name} {self.account_number[-4:]}'
        return f'**BLANK**'
    
    def __str__(self):
        return self.as_short_name()

class RetirementAccount(DAObject):
    """A retirement account"""
    def init(self, *pargs, **kwargs):
        super().init(*pargs, **kwargs)

    def as_short_name(self):
        if isinstance(self.short_name, str):
            return self.short_name
        elif isinstance(self.account_number, str) and isinstance(self.institution_name, str):
            return f'{self.institution_name} {self.account_number[-4:]}'
        return f'**BLANK**'
    
    def __str__(self):
        return self.as_short_name()
