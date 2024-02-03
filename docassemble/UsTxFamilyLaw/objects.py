"""
classes.py - Classes introduced by UsTxFamilyLaw
"""
# Ignore imoprt error on the next line.  It's a false positive.
from docassemble.base.util import DAObject  # type: ignore

__all__ = [
    'MotorVehicle',
    'Automobile',
    'Boat',
    'Airplane',
    'BankAccount',
    'RetirementAccount'
]

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

class MotorVehicle(DAObject):
    """A motor vehicle"""
    def init(self, *pargs, **kwargs):
        super().init(*pargs, **kwargs)

    def as_short_name(self):
        name_parts = [self.year or '', self.manufacturer or '', self.model or '']
        return ' '.join(name_parts)
    
    def __str__(self):
        return self.as_short_name()
    
class Automobile(MotorVehicle):
    """An automobile"""
    def init(self, *pargs, **kwargs):
        if 'type' not in kwargs:
            kwargs['type'] = 'automobile'
        super().init(*pargs, **kwargs)

class Boat(MotorVehicle):
    """A boat"""
    def init(self, *pargs, **kwargs):
        if 'type' not in kwargs:
            kwargs['type'] = 'boat'
        super().init(*pargs, **kwargs)

class Airplane(MotorVehicle):
    """An airplane"""
    def init(self, *pargs, **kwargs):
        if 'type' not in kwargs:
            kwargs['type'] = 'airplane'
        super().init(*pargs, **kwargs)
