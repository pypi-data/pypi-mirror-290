"""
 #  bas-muti :: deps_basic 公集
 @  E.C.Ares
 !  MIT DIVIƷON
 `  __deps_ builtin basic-python 极简我语：只述知，不应算，不杂念
"""

import   os,sys
import builtins                        as _bt
import     time                        as _ti
import     copy                        as _cp
import     math                        as _ma
import operator                        as _op
import   pickle                        as _pk
from       enum import Enum            as _um,\
                       EnumMeta        as _ut
from   argparse import Namespace       as _ym
from frozendict import frozendict      #FrozenDict ImmutableDict
import                 inspect         as _in
import                 types           as _ty
import                 numbers         as _nm
import                 typing          as _tp
import                 ctypes          as _tq
import                 collections     as _ts
import                 collections.abc as _tc
import                 warnings        as war
import                 functools       as _fm
import   xmlrpc.server                 as _xs
import   xmlrpc.client                 as _xc
from        abc import ABC             as _ax,\
                       ABCMeta         as _at,\
                       abstractmethod 

JH_VER=sys.version_info
if JH_VER >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ['JH_VER']

# 幻方初：重载 Built-in Functions
def initKam():
  # TODO: 上下文管理、序列化、比较、拷贝、反射等 __special__
  OBP = breakpoint
  OCO = compile
  OCN =   print
  OIN =   input
  OIF =    open
  VDO =    eval
  #LIX=      id # HEL=help del
  ZAC =   ascii
  #ZCI,ZIC,ZhI,ZoI,ZIP,ZBC=chr,ord,hex,oct,zip,bin
  #FRL,FRO,ZRL,ZЯL,ZUL,ZQL=all,any,max,min,sum,len
  ZFD =   round
  ZHD =  divmod
  #VAB,POW=abs,pow TODO: 运算符重载
  ZCR =  format
  STD =  sorted
  ZHX =    hash
  DET =    iter
  DIT =lambda x:range(len(x))
  NXT =    next
  NXD =lambda x:next(iter(x))
  # any-Exs
  JXN =    repr
  T_R =    vars
  TCR =  locals
  TGR = globals
  VZR = os.getenv
  TZR = os.environ
  TZ_ =lambda*c: TZR
  SΞ_ = setattr
  GΞ_ = getattr
  ƋΞ_ = delattr
  BΞ_ = hasattr
  #BΞL=lambda o: BΞ_(o,'__len__'    )# Quanable
  BEI =lambda o:BΞ_(o,'__getitem__' )# Indyable
  BEΞ =lambda o:BΞ_(o,'__getattr__' )# Ξtrbable
  BES =lambda o:BΞ_(o,'__getstate__')# Statable
  BEC =callable                      # Callable
  #BEH=lambda o:BΞ_(o,'__hash__')    # Hashable  不行，必须不可变
  SI_ =lambda o,*x :o.__setitem__(*x)
  GI_ =lambda o, k :o.__getitem__( k)
  ƋI_ =lambda o, k :o.__delitem__( k)
  VAL =lambda o:GΞ_(o, 'value' ,None)
  JYM =lambda o:GΞ_(o,'__name__','_')   # _jc _jc_nym
  NYM =lambda o:GΞ_(o,  'name'  ,'_')   # nym [0].hed
  GIF =     sys._getframe
  TGF =lambda o:o.f_globals
  TCF =lambda o:o.f_locals
  ZFB =lambda o:o.f_back
  CWD =      os.getcwd
  GST =     _ti.time
  ZCL = os.path.join    # join 除格转 有他辑排异
  ACL = os.path.splitext
  AC_ =lambda c,x='_': c.split(x)
  FCL = os.path.basename
  JCL =lambda c:ACL(FCL(c))[0]
  TG_ =lambda i:TGF(GIF(i))
  TC_ =lambda i:TCF(GIF(i))
  #LCL= os.path.dirname
  # Z系 : 纯格转(常可逆),无事务 包括小函
  #ZCX=     str
  ZBC =     str.encode
  ZCB =   bytes.decode
  ZLC =     str.lower
  ZΓC =     str.upper
  Z_C =lambda c,x='_': x+c
  ZCA =lambda*c,x='_': x.join([str(i) for i in c])
  ZCO =lambda o:o.__str__()
  ZCQ =lambda o:o.__class__.__str__()
  ZDO =lambda o:dict(o.__dict__)
  ZDQ =lambda o:dict(o.__class__.__dict__)  
  ZTR =lambda a,t=str:t(a)if t in[list, tuple, dict, set, bytes, bytearray]\
            else''.join(a)if t == str   else a
  Z0A =lambda*c:c[0]if c else None
  Z_O =lambda o,c:o.__dict__[c]
  ZBO =     _pk.dumps
  ZOB =     _pk.loads
  ZIB =     int.from_bytes
  ZBI =     int.to_bytes
  QII =     int.bit_length
  QI1 =     int.bit_count
  GIT =lambda o,*c:o.get(*c) # 
  RVT =    dict.values
  RCT =    dict.keys
  RGT =    dict.items
  SED =    dict.setdefault
  ACT =lambda o:list(RCT(o)) # lambda 不带属性
  AVT =lambda o:list(RVT(o))
  AGT =lambda o:list(RGT(o))
  WAR =     war.warn
  RΞ_ =     _in.getmembers
  OFC =     _in.currentframe
  OS_ =     _in.stack
  # B系：Bool判断
  BT_ =         isinstance
  BB_ =         issubclass
  BU_ =     set.issubset
  BUT =     set.issuperset  # BU‾
  BTS =     _in.isclass
  BTW =     _in.isfunction   # callable
  BTM =     _in.ismethod
  BTF =     _in.isframe
  BTD =     _in.ismodule
  BTG =     _in.isgenerator
  BTB =     _in.isbuiltin
  BTQ =     _in.iscode
  BPC =lambda t,c='__': str.startswith(t,c)
  # COPY
  CPY =     _cp.copy
  CPD =     _cp.deepcopy
  CPL =lambda o:ZOB(ZBO( o ))
  CP_ = dict(
    _ = CPY,
    l = CPL,
    d = CPD)
  # V系 : 纯运算
  #VUI=     set.intersection
  #VUE=     set.union
  #VUB=     set.difference
  #VUD=     set.symmetric_difference
  # O系 : 纯操作,轻返回
  OPO =    os.popen
  ODO =    exec
  # NPCALL
  ONA=lambda o,d:ODO(f"{o} +=d")
  ONB=lambda o,d:ODO(f"{o} -=d")
  ONC=lambda o,d:ODO(f"{o} *=d")
  OND=lambda o,d:ODO(f"{o} /=d")
  ONE=lambda o,d:ODO(f"{o} |=d")
  ONP=lambda o,d:ODO(f"{o}//=d")
  ONF=lambda o,d:ODO(f"{o} %=d")
  ONX=lambda o,d:ODO(f"{o} ^=d")
  ONI=lambda o,d:ODO(f"{o} &=d")
  ONЯ=lambda o,d:ODO(f"{o}<<=d")
  ONR=lambda o,d:ODO(f"{o}>>={d}")
  #ODR=lambda q,*c,**g:ODO()
  OYP=lambda j,  q       :ODO(f"{j}=_am('{j}'               )",
                 q.update({'_am':_tp.TypeVar         }) or q)
  #q.update({'_am':_tp.NamedTuple})or q
  O0H=lambda j,s,q,d=None:ODO(f"{j}=_am('{j}',{s},defaults=d)",
                 q.update({'_am':_ts.namedtuple,'d':d}) or q)
  
  # UPDATE
  OUA =lambda o,d:o.append(d) # list
  OUB =lambda o,d:o.remove(d)
  OUC =lambda o:  o.clear(  )
  OUD =lambda o,d:o.update(d) # if BT_(n,dict,set)
  #copy(d).update(a)
  OUΔ =lambda o,d:{ **o, **d} #for k,v in d.items():if k not in o: o[k] = v 不建议
  OUL =    list.extend
  OUP =lambda o,d:  o.push( )
  OUT =lambda o, *c:o.pop(*c)
  RXN =lambda o  :  o.iter(  )
  QI_ =lambda e,o:  o.count(e)
  CPT =lambda t: {c: v for c, v in RGT(t) if not BPC(c)}
  NO_ =lambda*c: None
  EXM =lambda*c:  ...
  FRM =lambda*c: True
  FЯM =lambda*c:False
  OLC =lambda h:_xc.ServerProxy(f"http://{h[0]}:{h[1]}")
  OLS =lambda h:_xs.SimpleXMLRPCServer(h)

  # Map of abitems
  TAM = dict(
    C =lambda     : TCF(ZFB(OFC())) ,  #inspect.currentframe().f_back.f_locals
    G =lambda     : TGF(ZFB(OFC())) ,  #inspect.currentframe().f_back.fglobals
    C_=lambda x=1 : TCF(OS_()[x][0]),  #inspect.stack(  )[ x ][ 0   ].f_locals
    G_=lambda x=1 : TGF(OS_()[x][0]),  #inspect.stack(  )[ x ][ 0   ].fglobals
    #A=vars()
    Z =lambda     : TZR              ) #     os.environ
  #MAXX= {f:lambda _:v for f,v in TAM.items()} # LAMBDA表达式v不计算 一直指向global v
  MAXX=lambda F:lambda _:TAM[F]
  @MAXX("Z")
  def vzr(): pass
  @MAXX("G")
  def vgr(): pass
  @MAXX("C")
  def vcr(): pass
  # 小函 非core逻辑不套用标签 #TODO:批成
  ## 参数处理
  z_c =lambda*c:c if len(c)>1 else c[0]if len(c)else None
  zhc =lambda*c:                   c   if len(c)else()
  z_g =lambda   **g:               g   if len(g)else None
  zhg =lambda   **g:   tuple(g.items())if len(g)else()
  z__ =lambda*c,**g:(z_c(*c),g)if len(c)and len(g)else g if len(g)else z_c(*c)
  zh_ =lambda*c,**g: zhc(*c)+zhg(**g)
  ## 迭代处理
  ae_ =lambda a,b=z__:next((    e for e in a if           b(e)), None) # 元苛b(:保兑b
  an_ =lambda a,b=z__:next(( True for e in a if           b(e)),False) # 右苛b(:保兑b
  al_ =lambda a,b=z__:next((False for e in a if           b(e)), True) # 右苛b(:保兑b
  aee =lambda a      :next((    e for e in a if None is not e ), None) # 元苛有:苛无'单'
  #any=lambda a      :next(( True for e in a if             e ),False) # 右苛兑:anorm yes
  #all=lambda a      :next((False for e in a if         not e ), True) # 左苛左:alert left
  ane =lambda a      :next(( True for e in a if None is not e ),False) # 右苛有:anorm exist
  aln =lambda a      :next((False for e in a if None is     e ), True) # 左苛无:alert none
  fe_ =lambda a,b=z__:filter(b,a)
  g1_ =lambda a,b=z__: sum(     1 for _ in filter(b,a)) #不用len防外溢 # 计b(
  g1e =lambda a      : sum(     1 for e in a if None is not e )        # 计有
  g1n =lambda a      : sum(     1 for e in a if None is     e )        # 计无



  def updlSaf( ox, ux, ig='__', am=(z__,SI_)): # TODO PALL  (ZDO,SΞ_)
    _od          = am[0](ux)
    def _sm( jc) : am[1](ox, jc, _od[jc])
    if not ig:
      for _jc in _od.keys(): _sm(_jc)
    else:
      for _jc in _od.keys():
        if not BPC(_jc,ig): _sm( _jc)
  def updfSaf(ox, ux, ig='__', am=(z__,SI_)):
    updlSaf( ox, ux, ig=ig, am=am)
    return ox

  Cal = lambda m,*c,**g: m(*c,**g)
  Her = lambda c=__name__: c=="__main__" # betrHer default False
  def ASS(*c,**g): pass
  def _me(c=__file__,q=7): OCN(f"[{JCL(c)[:q]:_^7}] : 此 {c}")
  
  
  # 注册尾
  def reg(o,d=TAM["C"]()): # 括号打在哪层是哪层
    OUL(__all__,ACT(d))
    #OUD(  o   ,CPT(d))
    updlSaf(o,      d)
  #return reg
  reg(TAM["G"](),TAM["C"]())

__g=initKam() #__g()

# 国象初：归集
def initDep():
  #To-nYm-Abs 类  LAS or LAM (LAR)
  class TYA(_ym):
    _OT = type     # 型类  纇 isinstance
    _OM = object   # 象类  類 isinstance
    #LAM= function # 函类   
    _AT = _at      # 虚类  ABCMeta
    _AX = _ax      # 虚伪  ABC
    _UT = _ut      # 常型  
    _UM = _um      # 常象  enum AOH  值互斥
    _YM = _ym      # 变象  namespace 
    # TODO: fll pyt,byd pyt
  #To-nYm-Bas 基   .__class__ or .__bases__ is from TYA
  class TYB(TYA._YM):
    #   TypeBase
    #L__= ellipsis
    #NOT= NoneType
    #ObjectBase
    _0B=bool
    _0I=int
    _0F=float
    #OD= dreal    # num by performence (not embedding) 
    _0K= complex
    _0O= bytes
    _0H= tuple    # 由于不可变，不是组织容器
    _0Q= frozenset
    _0G= _ty.MappingProxyType
    ASX= list     # _0X仅由0X元素组成
    TSX= dict
    USX= set
    A0C= str      # code 没有 0C
    MAP= map
    A0O= bytearray
    TOC= _ts.namedtuple('TOC', ['nid','nym'])
    FUP= _ts.namedtuple('FUP', ['lam','ifc','ifg']) # FIXME Name
    RSI= range
    ASI= slice
    FIL= filter
    VOO= memoryview
    #HM=    cache,..   #属法 の 饰
    _HM=_fm.lru_cache  #Holdmθd Map
    _PM=   property    #Proprty Map
    _CM=   classmethod #Clasmθd Map
    _SM=  staticmethod #Statmθd Map
    _AM=abstractmethod #Abstmθd Map
    RIT= reversed
    ENU= enumerate    # FIXNAME
    SOX= super
    _ON= BaseException
    # TODO: contextlib.ContextManager


  # To-nYm-Collection
  class TYC(TYA._YM):
    _EN = Exception
    MOX = _ty.MethodType
    _QX = _tq.Structure
    _CB = _tq.c_bool
    _CI = _tq.c_int
    _CF = _tq.c_float
    _CD = _tq.c_double
    #_CK= _tq.c_complex
    _CC = _tq.c_char
    _CG = _tq.c_char_p
    _CH = _tq.c_float
    _CU = _tq.c_uint
    _CO = _tq.c_ubyte
    _CA = _tq.c_ushort
    A2X = _ts.deque
    TDX = _ts.defaultdict
    T2X = _ts.OrderedDict
    T3X = _ts.ChainMap
    CCC = _ts.Counter
    _ET = TypeError

  class MUT(TYA._UT):
    def __new__(ido,las,bas,cig):
      cig['_jc']=TYB._CM(lambda ego,val:NYM(ego._value2member_map_.get(val)))
      cig['_ug']=TYB._PM(lambda ego:tuple(_eg for _eg in ego if not BPC(NYM(_eg),'_')))
      return super().__new__(ido,las,bas,cig)
    
  class EUA(TYA._UM, metaclass =MUT): pass

  # So-nYm-A # 搜名
  class SYA(EUA):
    # 无
    EXS = Ellipsis # 有
    NON = None     # 冇
    FRB = True     # 右
    FЯB =False     # 左
    NIN = NotImplemented
    # 伪
    ZRO =   0      # 口 0X00
    ZRI =   1      # ZЯO 工(!= 0)
    ZЯO =   0XFF   # 
    ZRC =  '_'     #
    ZЯC =  '-'     #
    NAC ='nan'     #
    MRC ='inf'     #

  class SYB(EUA):
    JRO = TYB._0O([VAL(SYA.ZRO)])# B满 # 容(0~255)
    JЯO = TYB._0O([VAL(SYA.ZЯO)])# B空 FIXME != 0
    NAN = TYB._0F( VAL(SYA.NAC) )
    MRF = TYB._0F( VAL(SYA.MRC) )
    MЯF = TYB._0F( VAL(SYA.ZЯC)+VAL(SYA.MRC))

  class SYC(EUA):
    C00 = chr(0)   # 编号 0
    C01 = chr(1)   # 源数之门 一
    C02 = chr(2)   # 源数之门 二
    C03 = chr(3)   # 源数之门 三
    C04 = chr(4)   # 源数之门 四
    '''
    AND     = '&'
    OR      = '|'
    XOR     = '^'
    RSHIFT  = '>>'
    LSHIFT  = '<<'
    ADD     = '+'
    SUB     = '-'
    MUL     = '*'
    TRUEDIV = '/'
    FLOORDIV= '//'
    MOD     = '%'
    POW     = '**'
    EQ      = '=='
    NE      = '!='
    LT      = '<'
    GT      = '>'
    LE      = '<=' 
    GE      = '>='
    '''
  
  class OAR(TYA._YM):
    #ABS=_op.abs # abs()
    pass


  # 因缩写有重，而魔法须之，故辟此名間
  class OBR(TYA._YM):
    EQ =_op.eq         # ==
    NE =_op.ne         # !=
    GT =_op.gt         # >
    LT =_op.lt         # <
    GE =_op.ge         # >=
    LE =_op.le         # <=
    RSHIFT =_op.rshift # >>
    LSHIFT =_op.lshift # <<
    OR =_op.or_        # |
    AND=_op.and_       # &
    XOR=_op.xor        # ^
    ADD=_op.add        # +
    SUB=_op.sub        # -
    MUL=_op.mul        # *
    POW=_op.pow        # **
    MOD=_op.mod        # %
    TRUEDIV,FLOORDIV=TYB._SM(_op.truediv),TYB._SM(_op.floordiv) #/,//
    _qi= 18
    _ym=lambda jc:'__'+jc.lower()+'__'
    
  
  class SYP(EUA):
    _0B = bool
    _0I = int
    _0F = float
    #_OD= dreal    # num by performence (not embedding) 
    _0K = complex
    _0O = bytes
    _0H = tuple    # 由于不可变，不是组织容器
    _0Q = frozenset
    #_0M= MappingProxy
    ASX = list     # _0X仅由0X元素组成
    TSX = dict
    USX = set
    A0C = str      # code 没有 0C


  class CAR(TYA._UM):
    DDD = ':'
    BBB = '='
  # FIXME CBR to CBR_ALB(+-*/) and CBR_CPR (<>==) 

  #class CBR(TYA._UM):

  # FIXME what's Real
  TYP_=dict(
    B = TYB._0B,
    I = TYB._0I,
    F = TYB._0F,
    D = TYB._0F, # FIXME TYB._0D
    #R= TYB._0R,
    #E= TYB._0E, # 夼:对称闭集
    K = TYB._0K)
  TYP_0N = tuple(TYP_.values())
  TYP_.update(
    H = TYB._0H,
    O = TYB._0O)
  _YP_0X = tuple(TYP_.values())
  #_YP_ITR = list, dict, set
  TYP_.update(
    C = TYB.A0C)
  
  '''
  _   基本型
  abc 组织型(容器)
  w   函数型
  mw  泛型
  '''

  class TYM_(TYA._YM):
    ABC=_tp.ABCMeta
    Wra=_tp.WrapperDescriptorType
    Met=_tp.MethodWrapperType
    Met=_tp.MethodDescriptorType
    Gan=_tp.GenericAlias
    NoR=_tp.NoReturn
    #Nev=_tp.Never #311+
    #Sel=_tp.Self  #311+
    #Lit=_tp.LiteralString#311+
    Cla=_tp.ClassVar
    Fin=_tp.Final
    Uni=_tp.Union
    Opt=_tp.Optional
    Lit=_tp.Literal
    Typ=_tp.TypeAlias
    Con=_tp.Concatenate
    Typ=_tp.TypeGuard
    For=_tp.ForwardRef
    #Typ=_tp.TypeVar
    #Typ=_tp.TypeVarTuple#311+
    Par=_tp.ParamSpecArgs
    Par=_tp.ParamSpecKwargs
    Par=_tp.ParamSpec
    #Unp=_tp.Unpack#311+
    Gen=_tp.Generic
    Pro=_tp.Protocol
    Ann=_tp.Annotated
    Has=_tp.Hashable
    Awa=_tp.Awaitable
    Cor=_tp.Coroutine
    Asy=_tp.AsyncIterable
    Asy=_tp.AsyncIterator
    Ite=_tp.Iterable
    Ite=_tp.Iterator
    Rev=_tp.Reversible
    Siz=_tp.Sized
    Con=_tp.Container
    Col=_tp.Collection
    Cal=_tp.Callable
    Abs=_tp.AbstractSet
    Mut=_tp.MutableSet
    Map=_tp.Mapping
    Mut=_tp.MutableMapping
    Seq=_tp.Sequence
    Mut=_tp.MutableSequence
    Tup=_tp.Tuple
    Map=_tp.MappingView
    Key=_tp.KeysView
    Ite=_tp.ItemsView
    Val=_tp.ValuesView
    Con=_tp.ContextManager
    Asy=_tp.AsyncContextManager
    Gnr=_tp.Generator
    Asy=_tp.AsyncGenerator
    Nam=_tp.NamedTuple
    Typ=_tp.TypedDict
    New=_tp.NewType
    Pat=_tp.Pattern
    Mat=_tp.Match
    Any=_tp.AnyStr
    Byt=_tp.ByteString
    Lis=_tp.List
    Deq=_tp.Deque
    Set=_tp.Set
    Fro=_tp.FrozenSet
    Dic=_tp.Dict
    Def=_tp.DefaultDict
    Ord=_tp.OrderedDict
    Cou=_tp.Counter
    Cha=_tp.ChainMap
    Tex=_tp.Text
    #Req=_tp.Required#311+
    #Not=_tp.NotRequired#311+



  #class TYP(TYA._UM):
  class TYP(TYA._YM):
    _OT = _tp.Type            # 型伪
    ΛOT = _tp._GenericAlias
    NOR = _tp.NoReturn
    NON = None # 不用NoneType
    NST = _tp.TypeVar('NST')
    NSX = _tp.Any
    WSX = _tp.Callable[...,NSX]
    ITR = _tp.Iterable
    ABS = _tp.AbstractSet
    ANT = _tp.Annotated
    A1B = _tp.BinaryIO
    AIO = _tp.ByteString
    Y1X = _tp.ChainMap
    DDD = _tp.ContextManager
    N0B = _tp.Optional[TYB._0B] # Optional[bool]
    N0I = _tp.Optional[TYB._0I] # Optional[int]
    N0d = _tp.Optional[TYB._0F] # Optional[float]
    N0K = _tp.Optional[TYB._0K] # Optional[complex]
    N0H = _tp.Optional[TYB._0H] # Optional[tuple]
    N0C = _tp.Optional[TYB.A0C] # Optional[str]
    NFG = _tp.Optional[TYB.TSX] # Optional[dict]
    #_1o= one-hot
    #_JI= IntegralConstant
    A2C=_tp.AnyStr # str or bytes
    _SI=_tp.SupportsInt
    _SF=_tp.SupportsFloat
    _SK=_tp.SupportsComplex
    _SB=_tp.SupportsBytes
    _SJ=_tp.SupportsIndex
    _SA=_tp.SupportsAbs
    _SR=_tp.SupportsRound
    IO_=_tp.IO
    IOB=_tp.BinaryIO
    IOC=_tp.TextIO
    #_0X =_tp.Union[*_YP_0X]
    #_0X=_tp.Union[  TYB._0B,
    #                TYB._0I,
    #                TYB._0F,
    #                TYB._0K,
    #                TYB._0H,
    #                TYB._0O]
    #N0X = _tp.Union[*(_tp.Optional[_] for _ in _YP_0X)]
    A0I = _tp.List[int]
    A0S = _tp.List[str]
    A0d = _tp.List[float]
    A0K = _tp.List[complex]
    A0H = _tp.List[tuple]
    #A0X = _tp.Union[*(_tp.List[_] for _ in _YP_0X)]
    #A0X = _tp.Union[_tp.List[int]]
    ΛUX = _tp.Union[list, tuple]
    AUX = _tp.Union[list, tuple, str, bytearray]
    TUX = _tp.Union[dict, TYA._YM]
    T0I = _tp.Dict[str,int]
    T0d = _tp.Dict[str,float]
    T0K = _tp.Dict[str,complex]
    T0H = _tp.Dict[str,tuple]
    #T0X = _tp.Union[*(_tp.Dict[str,_] for _ in _YP_0X)]
    TOT = _tp.Dict[str,type]
    NJC = _tp.Dict[str,str]
    TCX = _tp.Dict[str,NSX]
    _FH = _tp.Tuple[_tp.Callable[[NST],NSX],NST]
    _BH = _tp.Tuple[_SF,_SF] # min max
    WAR = _tp.Optional[_tp.Type[Warning]]
    _QH = _tp.Optional[_tp.Sequence[int]]
    
    #DDD= Sequence Queue
    #_2H = MultiVar
    #L-Tuple
    # TODO Optinal[T]
  for _y in [TYA,TYB,TYC]: updlSaf(TYP,_y, am=(ZDO,SΞ_))
  for _y in [SYA,SYB,SYC]: updlSaf(TAM['C'](),{_j:VAL(_v)for _j,_v in RGT(ZDO(_y)) if not BPC(_j,VAL(SYA.ZRC))})
  reg(TAM['G'](),TAM['C']())
initDep()

# 麻雀初：成役  M_X 就是形如3(m_i)lam形的可定制方法，需要函数名现身 D就是 3(xmi)lambda D需要函数
def initMθd():
  ##多暗刻单骑U:x=aee\all.. 暗刻e骑m取x
  MU_X=lambda m,x=aee:lambda _:lambda   a,*c,**g:x(m(  e,*c,**g)for e in a) #模m行MU_X以_名命  m 主操作
  MUOX=lambda m,x=aee:lambda _:lambda o,a,*c,**g:x(m(o,e,*c,**g)for e in a) #o必在a前，没办法
  DU_X=lambda   x=aee:lambda m:lambda   a,*c,**g:x(m(  e,*c,**g)for e in a) #X形式的U作用于m
  DUOX=lambda   x=aee:lambda m:lambda o,a,*c,**g:x(m(o,e,*c,**g)for e in a) #X形式的U作用于m f(x={x1,x2,..})=(f(x1),f(x2),..)
  DUD =               lambda m:lambda a,*c,**g:{e[0]:m(e[1],*c,**g)for e in a.items()} #FD是组织对象
  ##多暗杠单骑F:x=fe_\fn_.. 暗杠e骑m取x  # feutre:入谓和象，返迭象合谓∈ m 谓词 返回置信率 默离:0(False),1(True)
  MF_X=lambda m,x=fe_:lambda _:lambda a,*c,**g:x(a,   lambda e:m(e,*c,**g))            # for dict c.__contains__(e[0])
  DFD =               lambda m:lambda a,*c,**g:filter(lambda e:m(e,*c,**g), a.items()) # lambda e:m(e[1],*c,**g) 外套dict
  ##小三元两听I:[if-lif-lse]三元mbd听bd same c 默认不行返回None
  MIFX=lambda   m=z__,b=z__,d=NO_:lambda _:\
       lambda*c,m= m ,b= b ,d= d :b(*c)if m(*c)else d(*c)  # [if-else] m 可加随机 random.random() < 0.5
  ##大三元两听I:[if-lif-lse]三元mbd听bd  # 
  def MTFX(m,b=NON,d=FЯB,e='Err'):
    if d is None:d=RuntimeError(e) #False
    def DTF(_):
      #global d
      def _(*c,m=m,b=b,d=d): # M方法需要细化返回函数的参数
        try   :     a=m(*c) # e.g.Fup(*c)()
        except:return d(*c)if callable(d)else d
        return        b(*c)if callable(b)else a if b is None else b
      return _
    return DTF
  def DTFX(b=NON,d=FЯB,e='Err'):
    e=RuntimeError(e) # False
    def DTF(m):
      def _(*c):        # b=b,d=d D方法返回函数的参数不重要
        try   :     a=m(*c) # e.g.Fup(*c)()
        except:return d(*c)if callable(d)else e if d is None else d
        return        b(*c)if callable(b)else a if b is None else b
      return _
    return DTF

  @MTFX(hash,b=True)
  def BEH():pass

  # MLFX=lambda M,B,D:lambda _:lambda *c:B(*c)if M(*c)else D(*c)

  # - - - - - - # 一些例子, FIXME 转移到子.py
  
  @MF_X(list.__contains__)
  def MRA(): pass
  @MF_X(lambda e,t:t.__contains__(e[0]))
  def MRT(): pass
  ZTR_DIC=lambda x,c:ZTR(MRT(x.items(),c),dict)

  # TODO 给出函数的对偶函数

  # FIXME
  NXD_EXS  = lambda x: NXD(x) if len(x) else NON
  #NXD_EGO = lambda x: NXD(x) if len(x) else x

  reg(TAM['G'](),TAM['C']())
initMθd()
def initLas():
  #CEG := abC_dEf_Ghi for default
  # TYP LAR = 娄(variable) 
  class LAR(TYA._OT): pass
  # TYP LAM = 函(function)
  class LAM(TYA._OT):
    def __new__(o,j,b,k):
      _F = FЯB
      for _B in b:
        # BΞ_(_B,'_am')
        if BEC(GΞ_(_B,'_am',NON)):
          _F = FRB
          break
      # 查'_am'方法
      if not _F and ('_am' not in k or not BEC(k['_am'])): raise TYC._ET("函宣，必可使'_am'调")
      # 添 __call__ 方法
      k['__call__']=lambda s,*c,**g: s._am(*c,**g)
      # 添 reset 方法
      def resnLAM(s,am):
        if not BEC( am): raise TYC._ET("必可使am调")
        s._am  =    am  
      k['res'] = resnLAM
      # ret-super TYB.SOX()
      return super().__new__(o,j,b,k)
  # Doo
  class Exc(metaclass = LAM):
    def _am(o,c,*d, fb= FRB):
      if fb:return VDO(c,*d)
      else:        ODO(c,*d)

  class AGG():
    @TYB._SM
    def TAZ(): return TZR
    @TYB._SM
    def TAC(): return _in.stack()[1].frame.f_locals
    @TYB._SM
    def TAG(): return _in.stack()[1].frame.f_globals

  # 量局，实时计算 vars() 的引申
  class Xar():
    # Map of abitems
    _JC_DIC = dict(
      Z = 'os.environ'       ,
      B = 'builtins.__dict__',
      G = 'globals()'        ,
      C =  'locals()'        ,
      G1= '_in.stack()[1].frame.f_globals',
      C1= '_in.stack()[1].frame.f_globals',
      Gb= 'OFC().f_back.f_globals',
      Cb= 'OFC().f_back.f_locals' )
    def __init__(o, Z='Z'):
      o._fc = Xar._JC_DIC[Z] if Z in Xar._JC_DIC else Xar._JC_DIC['C']
      o._am = Exc()
    __setstate__=__init__
    def __getstate__(o):  return o._fc
    __repr__=__getstate__
    def __getitem__(o,j:str  )->TYP.NSX: return o._am(f"{o._fc}.get('{j}')")
    def __setitem__(o,j:str,v)->TYP.NON:        o._am(f"{o._fc}")[    j] = v
    get=__getitem__
    def sed(o,j:str,v)->TYP.NON: # 如果有不能更改，更改用 __setitem__
      if BT_(v,str):o._am(f"{o._fc}.setdefault('{j}','{v}')",fb=FЯB)
      else:         o._am(f"{o._fc}.setdefault('{j}', {v} )",fb=FЯB)
    def __call__(o,Z='G'):                return Xar(Z)
  # instance Formation 左
  class IfЯ():
    def __init__(o,ec=NON):o._ec=ec
    def __bool__(o):return FЯB
    def __str__(o):return o._ec
    def __repr__(o):return f"IfЯ {str(o)}"
  # 量局，维护内部字典
  class Tal():
    def __init__(     o,Z='G')->TYP.NON:o.O=TAM[Z] if Z in TAM else TAM["C"] # 增值するG
    def __getstate__( o      )->TYP.TSX:return o.O()
    def __getitem__(o,c:str  )->TYP.NSX:return o.O()[c] if c in o.O() else NON
    def __setitem__(o,c:str,v)->TYP.NON:o.O()[c]=v
    def __getattr__(o,c:str  )->TYP.NSX:return o.O()[c] if c in o.O() else NON
    #def __setattr__(o,c:str,v)->TYP.NON:o.O()[c]=v
    def rec(o,Z='G'):return Tal(Z)
    #def __call__(     o,Z='G'):         o.O=TAM["G"]()
    def __str__(): return"TAC,TAG,TAZ=TAM['C'](),TAM['G'](),TAM['Z']()"
   
  #reg(TAM["G"](),TAM["C"]())
  TAM['G']()['AGG'] = AGG
  TAM['G']()['TAL'] = Tal()
  TAM['G']()['VAR'] = Xar()
  OUA(__all__,'AGG')
  OUA(__all__,'TAL')
  OUA(__all__,'VAR')
initLas()

if Her():Cal(_me)