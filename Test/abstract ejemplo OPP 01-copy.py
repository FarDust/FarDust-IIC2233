from abc import abstractproperty,ABCMeta

class Base(metaclass= ABCMeta):
    
    @abstractproperty
    def value(self):
        return 'Nunca deberíamos llegar aquí'


class Implementation(Base):
    
    @property
    def value(self):
        return 'propiedad concreta'

try:
    b = Base()
    print('Base.value: {}'.format(b.value))
    
except Exception as err:
    print('ERROR: {}'.format(str(err)))

i = Implementation()

print('Implementation.value: {}'.format(i.value))