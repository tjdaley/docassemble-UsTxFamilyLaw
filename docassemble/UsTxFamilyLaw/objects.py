"""
classes.py - Classes introduced by UsTxFamilyLaw
"""
__author__ = "Thomas J. Daley, J.D."
# Ignore imoprt error on the next line.  It's a false positive.
from docassemble.base.util import DAList, DAObject, IndividualName, Name, Person  # type: ignore

__all__ = [
    'Asset',
    'MotorVehicle',
    'Automobile',
    'Boat',
    'Airplane',
    'BankAccount',
    'OtherAsset',
    'RetirementAccount',
    'Liability',
    'UnsecuredDebt',
    'Attorney',
    'AttorneyList'
]

class Attorney(Person):
    """Represents a natural person who is an attorney."""
    NameClass = Name
    AddressClass = Address
    LatitudeLongitudeClass = LatitudeLongitude

    def init(self, *pargs, **kwargs):
        if not hasattr(self, 'name') and 'name' not in kwargs:
            self.initializeAttribute('name', self.NameClass)
        if 'address' not in kwargs:
            self.initializeAttribute('address', self.AddressClass)
        if 'bar_no' not in kwargs:
            self.bar_no = ''
        if 'firm_name' not in kwargs:
            self.firm_name = ''
        if 'phone_number' not in kwargs:
            self.phone_number = ''
        if 'fax_number' not in kwargs:
            self.fax_number = ''
        if 'location' not in kwargs:
            self.initializeAttribute('location', self.LatitudeLongitudeClass)
        if 'name' in kwargs and isinstance(kwargs['name'], str):
            if not hasattr(self, 'name'):
                self.initializeAttribute('name', self.NameClass)
            self.name.text = kwargs['name']
            del kwargs['name']
        super().init(*pargs, **kwargs)

class AttorneyList(DAList):
    """Represents a list of attorneys."""
    AttorneyClass = Attorney

    def init(self, *pargs, **kwargs):
        self.object_type = self.AttorneyClass
        super().init(*pargs, **kwargs)

class Asset(DAObject):
    """An asset"""
    def init(self, *pargs, **kwargs):
        super().init(*pargs, **kwargs)

    def as_short_name(self):
        return self.short_name or '**BLANK**'
    
    def __str__(self):
        return self.as_short_name()

class Liability(DAObject):
    """A liability"""
    def init(self, *pargs, **kwargs):
        super().init(*pargs, **kwargs)

    def as_short_name(self):
        return self.short_name or '**BLANK**'
    
    def __str__(self):
        return self.as_short_name()

class UnsecuredDebt(Liability):
    """An unsecured debt"""
    def init(self, *pargs, **kwargs):
        super().init(*pargs, **kwargs)
    
    def as_short_name(self):
        return self.creditor_name or '**BLANK**'

class OtherAsset(Asset):
    """An asset of an unspecified type"""
    def init(self, *pargs, **kwargs):
        super().init(*pargs, **kwargs)

    def as_short_name(self):
        return self.description or '**BLANK**'

class BankAccount(Asset):
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

class RetirementAccount(Asset):
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

class MotorVehicle(Asset):
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
