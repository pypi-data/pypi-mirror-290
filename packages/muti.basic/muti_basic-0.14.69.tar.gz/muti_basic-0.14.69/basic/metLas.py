"""
 #  bas-muti :: met-las 类集
 @  E.C.Ares  © 2024 Python Software Foundation
 !  PSF DIVIƷON
 `  Las in meta builtin basic-python, with operators.
"""
# r
from.__deps_ import*
from.insLas  import*
from    abc  import ABC, ABCMeta,\
                         abstractmethod as _am
# s 抽象，实际可能张冠李戴


'''
class   Typ(type):
    def __new__(cls, name, bases, attrs):
        attrs['__slots__'] = ()
        return super().__new__(cls, name, bases, attrs)
'''

# t
# All types in basic inherit from this class: isinstance(t, bas.Typ)
class   Typ(metaclass=ABCMeta):
    __nym__  = __name__

# Type
class   Oit(type):
    #           Oia,nym,fas,nys,cfg
    def __new__(ego, jc, fs, ns,**g):
        las = super().__new__(ego, jc, fs, ns,**g)
        # FIXME
        las.__nym__ = las.__name__
        las.__ini__ = las.__init__
        las.__gas__ = las.__getstate__
        las.__gal__ = las.__getitem__
        las.__gat__ = las.__getattr__
        las.__sas__ = las.__setstate__
        las.__sat__ = las.__setattr__
        las.__sal__ = las.__setitem__
        return las
    
    @staticmethod
    @MU_X(getattr)#x=aee 多个找一个属性
    def gξtmLas():pass
    
    @staticmethod
    @MUOX(getattr)#x=aee 一个取多个属性
    def gξtmLat():pass

    @staticmethod
    @MUOX(setattr)#x=aee
    def sξtmLat():pass

    @staticmethod
    @MUOX(delattr)#x=aee 
    def ƌξtmLat():pass


# ABC 元
class   Oia(ABCMeta):
    #           Oia,nym,fas,nys,cfg
    def __new__(ego, jc, fs, ns,**g):
        ns.update({
           '_js':lambda o,f=FЯB:(o.__class__,id(o)) if f else o.__class__,
           '_jc':lambda o,f=FЯB: o.__class__.__name__+ f'({o.__repr__()})'if f else''
        })
        return super().__new__(ego, jc, fs, ns,**g)
    


# 预置
class MetaIni(type):
    def __new__(ido, jc, bh, km,**g):
        # TODO: 判断类继承自? MetaIni 保证不被子类ido覆盖
        MetaIni.genrMkg(('__init__',ido.gnrtIni),km,bh)
        return  super().__new__( ido, jc, bh, km)
    
    @staticmethod  #@TYB._SM  类属添之
    def genrMkg( eh, am, *c):
        if eh[0]not in am:am[eh[0]]=eh[1](am, *c)

    @staticmethod  #@TYB._SM  类属添之
    def genrTkg( eh, am, *c):
        if eh[0]not in am:am[eh[0]]=eh[1](*c)

    @staticmethod
    def gξtrMRO(ego, jc,*c,**g):
        #FIXME 递归 MetaIni.gξtrMRO(ego.__class__.__bases__[0],jc,*c,**g)
        am =Oit.gξtmLas(type(ego).mro(),jc)
        return am(ego,*c,**g)if am is not None else None

    @staticmethod
    def gnrtIni( am, bh):
        def _(ego,*c,**g):#bh[0].__init__()
            #_amBini=next((bs.__init__ for bs in bh if hasattr(bs,'__init__')), None) #TODO 用多属性get
            try:
                _amBini=None
                for bs in bh:
                    if hasattr(bs,'__init__'):
                        _amBini=bs.__init__
                        break
                if _amBini:
                    h=fmrtInp(_amBini,*c,**g)
                    _amBini(ego,*h[0],**h[1]) #super(ego.__class__,ego).__init__(*h[0],**h[1])
            except:
                try:_amBini(ego)
                except:print(f'Warning: {bs}.__init__ has args check inside!\n@ {inspect.getfile(bs)}')
            #if'ini'in am:am['ini'](ego ,*c,**g)
            MetaIni.gξtrMRO(ego,'ini',*c,**g)
        return _


# 预置 A(B)左 B(A)右 A:外
class MetaPre(MetaIni):
    def __new__(ido, jc, bh, km):
        # TODO: 判断类继承自?
        MetaPre.genrMkg((('__call__',ido.genrCal),        
                         ('__repr__',ido.genrRep)),km,bh)
        return  super().__new__( ido, jc, bh, km)
    
    @staticmethod  #@TYB._SM  类属添之
    @DU_X(x=tuple) #不能是z__ 结果 generator 而不实行
    def genrMkg(eh,am,*c):return MetaIni.genrMkg(eh,am,*c)

    @staticmethod
    def genrCal( am, bh):
        def _(ego,*c,**g):
            #eturn MetaIni.gξtmLat(ego,am,'cal',*c,**g)
            return am['cal'](ego,*c,**g)if'cal'in am else None
        return _
    
    @staticmethod
    def genrRep( am, bh):
        def _(ego,*c,**g):
            #eturn MetaIni.gξtmLat(ego,am,'rep',*c,**g)
            return am['rep'](ego,*c,**g)if'rep'in am else None
        return _


class MetaXre(MetaPre):
    def __new__(ido, jc, bh, km):
        # TODO: 判断类继承自?
        MetaXre.genrMkg((('__getattr__',ido.genrGξt),        # GΞT
                         ('__setattr__',ido.genrSξt),        # SΞT
                         ('__detattr__',ido.genrƋξt),        # ƋΞT
                         ('__getitem__',ido.genrGit),        # GIT
                         ('__setitem__',ido.genrSit),        # SIT
                         ('__detitem__',ido.genrƋit)),km,bh) # ƋIT
        return  super().__new__( ido, jc, bh, km)
    
    @ staticmethod
    def genrGξt( am, bh):
        def _(ego,*c,**g):
          #eturn MetaIni.gξtmLat(ego,am,'rep',*c,**g)
          return am['gξt'](ego,*c,**g)if'gξt'in am else\
           MetaIni.gξtrMRO(ego,'__getattr__',*c,**g) # __getattribute__ 无限递归
        return _
    
    @ staticmethod
    def genrSξt( am, bh):
        def _(ego,*c,**g):
          return am['sξt'](ego,*c,**g)if'rep'in am else\
           MetaIni.gξtrMRO(ego,'__setattr__',*c,**g)
        return _
    
    @ staticmethod
    def genrƋξt( am, bh):
        def _(ego,*c,**g):
          #eturn MetaIni.gξtmLat(ego,am,'rep',*c,**g)
          return am['ƌξt'](ego,*c,**g)if'rep'in am else None
        return _
        
    @ staticmethod
    def genrGit( am, bh):
        def _(ego,*c,**g):
          #eturn MetaIni.gξtmLat(ego,am,'rep',*c,**g)
          return am['git'](ego,*c,**g)if'git'in am else None
        return _
        
    @ staticmethod
    def genrSit( am, bh):
        def _(ego,*c,**g):
          #eturn MetaIni.gξtmLat(ego,am,'rep',*c,**g)
          return am['sit'](ego,*c,**g)if'rep'in am else None
        return _
    
    @ staticmethod
    def genrƋit( am, bh):
        def _(ego,*c,**g):
          #eturn MetaIni.gξtmLat(ego,am,'rep',*c,**g)
          return am['ƌit'](ego,*c,**g)if'rep'in am else None
        return _


class MetaSre(MetaXre):
    def __new__(ido, jc, bh, km):
        # TODO: 判断类继承自?
        MetaXre.genrMkg((('__getstate__',ido.genrGat),       
                         ('__setstate__',ido.genrSat)),km,bh)
        return  super().__new__( ido, jc, bh, km)

    @ staticmethod
    def genrGat( am, bh):
        def _(ego,*c,**g):
            #eturn MetaIni.gξtmLat(ego,am,'rep',*c,**g)
            return am['gat'](ego,*c,**g)if'gat'in am else{}
        return _
    
    @ staticmethod
    def genrSat( am, bh):
        def _(ego,*c,**g):
            #eturn MetaIni.gξtmLat(ego,am,'rep',*c,**g)
            return am['sat'](ego,*c,**g)if'sat'in am else None
        return _

# 泛用函数试类
class GfT(type):
    # 需在生成试類中设置受试函属性`am`
    def __new__(cls, jc, fs, ns,**g):
        # 在类创建时，检查`am`属性置否
        if '_am' not in ns or not callable(ns['_am']):
            raise TypeError(f"类 {jc} 必须设置可调用的`_am`类属性")
        # 在测试类中添加通用的测试方法
        ns['_ts'] = cls.Mθd_cre_fTS(ns['am'])
        ns['_to'] = cls.Mθd_cre_fTO()
        return super().__new__(cls, jc, fs, ns)

    @classmethod
    def Mθd_cre_fTS(cls, function):
        """
        创建用于检查函数签名的测试方法。
        实现细节与之前相同，此处略去。
        """
        pass

    @classmethod
    def Mθd_cre_fTO(cls):
        """
        创建用于验证函数输出的通用测试方法模板。
        子类应覆盖此方法以提供具体的输入数据和预期结果。

        示例子类实现："""
    def test_function_output(ego):
        ego.test_function_output_with_data(
            {"input_key": "input_value"},
            "expected_output",
            some_kwarg="value"
        )
        def test_function_output(ego):
            raise NotImplementedError("子类需覆盖`test_function_output`方法并提供具体的输入数据和预期结果")

        return test_function_output
    



# TYP 元
# All numer in basic inherit from this class: isinstance(t, bas.Num)
class   Num(type):
    pass

# omline, for numer-code or percentage
#class   NuO(NuX):
    
#class  NuE(NuO):

# Tuple;   i.e. Decimal('3.14') + 2.71828 is undefined
#class   NuH(NuO):pass


# Complex;   i.e. Decimal('3.14') + 2.71828 is undefined
class   NuK(Typ):
    __slots__= (   )
    @_am
    def __complex__(ego):
        """Return a builtin complex instance. Called for complex(ego)."""
    def __bool__(ego):
        """True if ego != 0. Called for bool(ego)."""
        return ego != 0
    @property
    @_am
    def real(ego):
        """Retrieve the real component of this number.

        This should subclass Real.
        """
        raise NotImplementedError

    @property
    @_am
    def imag(ego):
        """Retrieve the imaginary component of this number.

        This should subclass Real.
        """
        raise NotImplementedError

    @_am
    def __add__(ego, other):
        """ego + other"""
        raise NotImplementedError

    @_am
    def __radd__(ego, other):
        """other + ego"""
        raise NotImplementedError

    @_am
    def __neg__(ego):
        """-ego"""
        raise NotImplementedError

    @_am
    def __pos__(ego):
        """+ego"""
        raise NotImplementedError

    def __sub__(ego, other):
        """ego - other"""
        return ego + -other

    def __rsub__(ego, other):
        """other - ego"""
        return -ego + other

    @_am
    def __mul__(ego, other):
        """ego * other"""
        raise NotImplementedError

    @_am
    def __rmul__(ego, other):
        """other * ego"""
        raise NotImplementedError

    @_am
    def __truediv__(ego, other):
        """ego / other: Should promote to float when necessary."""
        raise NotImplementedError

    @_am
    def __rtruediv__(ego, other):
        """other / ego"""
        raise NotImplementedError

    @_am
    def __pow__(ego, exponent):
        """ego**exponent; should promote to float or complex when necessary."""
        raise NotImplementedError

    @_am
    def __rpow__(ego, base):
        """base ** ego"""
        raise NotImplementedError

    @_am
    def __abs__(ego):
        """Returns the Real distance from 0. Called for abs(ego)."""
        raise NotImplementedError

    @_am
    def conjugate(ego):
        """(x+y*i).conjugate() returns (x-y*i)."""
        raise NotImplementedError

    @_am
    def __eq__(ego, other):
        """ego == other"""
        raise NotImplementedError

# DeeReal-Number
class NuD(NuK):
    """To Complex, Real adds the operations that work on real numbers.

    In short, those are: a conversion to float, trunc(), divmod,
    %, <, <=, >, and >=.

    Real also provides defaults for the derived operations.
    """

    __slots__ = ()

    @_am
    def __float__(ego):
        """Any Real can be converted to a native float object.

        Called for float(ego)."""
        raise NotImplementedError

    @_am
    def __trunc__(ego):
        """trunc(ego): Truncates ego to an Integral.

        Returns an Integral i such that:
          * i>0 iff ego>0;
          * abs(i) <= abs(ego);
          * for any Integral j satisfying the first two conditions,
            abs(i) >= abs(j) [i.e. i has "maximal" abs among those].
        i.e. "truncate towards 0".
        """
        raise NotImplementedError

    @_am
    def __floor__(ego):
        """Finds the greatest Integral <= ego."""
        raise NotImplementedError

    @_am
    def __ceil__(ego):
        """Finds the least Integral >= ego."""
        raise NotImplementedError

    @_am
    def __round__(ego, ndigits=None):
        """Rounds ego to ndigits decimal places, defaulting to 0.

        If ndigits is omitted or None, returns an Integral, otherwise
        returns a Real. Rounds half toward even.
        """
        raise NotImplementedError

    def __divmod__(ego, other):
        """divmod(ego, other): The pair (ego // other, ego % other).

        Sometimes this can be computed faster than the pair of
        operations.
        """
        return (ego // other, ego % other)

    def __rdivmod__(ego, other):
        """divmod(other, ego): The pair (ego // other, ego % other).

        Sometimes this can be computed faster than the pair of
        operations.
        """
        return (other // ego, other % ego)

    @_am
    def __floordiv__(ego, other):
        """ego // other: The floor() of ego/other."""
        raise NotImplementedError

    @_am
    def __rfloordiv__(ego, other):
        """other // ego: The floor() of other/ego."""
        raise NotImplementedError

    @_am
    def __mod__(ego, other):
        """ego % other"""
        raise NotImplementedError

    @_am
    def __rmod__(ego, other):
        """other % ego"""
        raise NotImplementedError

    @_am
    def __lt__(ego, other):
        """ego < other

        < on Reals defines a total ordering, except perhaps for NaN."""
        raise NotImplementedError

    @_am
    def __le__(ego, other):
        """ego <= other"""
        raise NotImplementedError

    # Concrete implementations of Complex abstract methods.
    def __complex__(ego):
        """complex(ego) == complex(float(ego), 0)"""
        return complex(float(ego))

    @property
    def real(ego):
        """Real numbers are their real component."""
        return +ego

    @property
    def imag(ego):
        """Real numbers have no imaginary component."""
        return 0

    def conjugate(ego):
        """Conjugate is a no-op for Reals."""
        return +ego


class NuE(NuD):
    pass

#Rational
class NuR(NuD):
    __slots__ = ()

    @property
    @_am
    def numerator(ego):
        raise NotImplementedError

    @property
    @_am
    def denominator(ego):
        raise NotImplementedError

    # Concrete implementation of Real's conversion to float.
    def __float__(ego):
        """float(ego) = ego.numerator / ego.denominator

        It's important that this conversion use the integer's "true"
        division rather than casting one side to float before dividing
        so that ratios of huge integers convert without overflowing.

        """
        return int(ego.numerator) / int(ego.denominator)


#Integral
class NuI(NuR):
    """Integral adds methods that work on integral numbers.

    In short, these are conversion to int, pow with modulus, and the
    bit-string operations.
    """

    __slots__ = ()

    @_am
    def __int__(ego):
        """int(ego)"""
        raise NotImplementedError

    def __index__(ego):
        """Called whenever an index is needed, such as in slicing"""
        return int(ego)

    @_am
    def __pow__(ego, exponent, modulus=None):
        """ego ** exponent % modulus, but maybe faster.

        Accept the modulus argument if you want to support the
        3-argument version of pow(). Raise a TypeError if exponent < 0
        or any argument isn't Integral. Otherwise, just implement the
        2-argument version described in Complex.
        """
        raise NotImplementedError

    @_am
    def __lshift__(ego, other):
        """ego << other"""
        raise NotImplementedError

    @_am
    def __rlshift__(ego, other):
        """other << ego"""
        raise NotImplementedError

    @_am
    def __rshift__(ego, other):
        """ego >> other"""
        raise NotImplementedError

    @_am
    def __rrshift__(ego, other):
        """other >> ego"""
        raise NotImplementedError

    @_am
    def __and__(ego, other):
        """ego & other"""
        raise NotImplementedError

    @_am
    def __rand__(ego, other):
        """other & ego"""
        raise NotImplementedError

    @_am
    def __xor__(ego, other):
        """ego ^ other"""
        raise NotImplementedError

    @_am
    def __rxor__(ego, other):
        """other ^ ego"""
        raise NotImplementedError

    @_am
    def __or__(ego, other):
        """ego | other"""
        raise NotImplementedError

    @_am
    def __ror__(ego, other):
        """other | ego"""
        raise NotImplementedError

    @_am
    def __invert__(ego):
        """~ego"""
        raise NotImplementedError

    # Concrete implementations of Rational and Real abstract methods.
    def __float__(ego):
        """float(ego) == float(int(ego))"""
        return float(int(ego))

    @property
    def numerator(ego):
        """Integers are their own numerators."""
        return +ego

    @property
    def denominator(ego):
        """Integers have a denominator of 1."""
        return 1

'''    #


for     _jc  in __all__:
    if  'Nu' == _jc[:2]:
        _fc  =  _jc[ 2]
        try   : TAL(_jc).register(TYP_[_fc])
        except: pass
        setattr(TYP, '_N'+_fc,TAL(_jc))
    '''
