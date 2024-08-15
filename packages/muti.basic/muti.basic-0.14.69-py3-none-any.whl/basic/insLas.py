import  inspect
from itertools import groupby

def fmrtInp( am, *c,**g):
    sig = inspect.Signature.from_callable( am)
    _c,_g=[],None
    # 迭代时分组
    for k,r in groupby(reversed(sig.parameters.items()),
        lambda h:'KEYWO'if h[1].default!=inspect.Parameter.empty else str(h[1].kind)[:5]if'ego'!=h[0]else'EGO'):
        if   _g is None and k.startswith('VAR_K'):_g=g
        elif _g is None and k.startswith(    'K'):
                #不能这么写 _g=dict(filter(lambda i:i[0]in dict(r),g.items()))：dict(r)重耗且脱变
                                                  r =dict(r)
                                                  _g=dict(filter(lambda i:i[0]in r,g.items()))
        elif _g is None                          :_g={}
        elif                k.startswith('VAR_P'):
                                                  _c=c
                                                  break#c_k=False #FIXME POSITIONAL_OR_KEYWORD
        elif                k.startswith(    'P'):
                                                  _c=c[:len(list(r))]
                                                  break
    return _c,_g

def getrLam( ox, *c,**g):
    h = fmrtInp( ox, *c,**g)
    return ox(*h[0],**h[1])

def getrLas( ox, *c,**g):
    h = fmrtInp( ox.__init__, *c,**g)
    return ox(*h[0],**h[1])


if'__main__'==__name__:
    class A():
        def __init__(ego,m,n,x=4,y=5,z=6):
            print('A',m,n,x,y,z)

    '''
    class B(A,metaclass=MetaIni):
        def ini(ego,m,n,o,x=15):
            ego.a=m
            print(ego.a)
    '''
    def foo(a,b=1,*c,d,**kw):pass
 
    # 获取函数参数返回一个有序字典
    parms = inspect.signature(foo).parameters
    print(parms)
    #
    # 获取参数名，参数属性，参数默认值
    for name,parm in parms.items():
        print(name,parm.kind,parm.default)

    b=getrLas(A,7,8,9,x=14,t=111)