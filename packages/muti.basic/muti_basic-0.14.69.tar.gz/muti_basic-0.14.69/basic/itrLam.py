"""
 # 
 @
 !
 ` 分为两部分，一个是修饰迭代器得到新的迭代器，一个是修饰迭代器循环里的工作流
"""

from typing import Any
from   tqdm import trange, tqdm as _dm
from functools import wraps
import sys
from collections.abc import Iterator

def is_iterator(obj):
    return isinstance(obj, Iterator)

MAFX=lambda F:lambda a:lambda C:F(C)


#MARX=lambda c:lambda C:RSX(C,c)
#MARX
TM1=lambda V:lambda a,v=V:lambda*c,**g:v(a(*c,**g))

class TDDM:
    def __init__(ego,od,qi=67,jc='',zc=''):
        ego._em=range(od)if isinstance(od,int)else od
        ego._qi=qi
        ego._1e=1/float(getattr(ego._em,'__len__',lambda:ego._qi)())
        ego._1d=ego._qi* ego._1e
        ego._jc=jc
        ego._zc=zc
        ego._li=0  # Current count
        ego._le=0.0
        ego._ld=0.0
        ego.ocn_=dict(
            n = ego.ocn_rnt,
        )

    def __call__(ego,*c,**g) -> Any:
        for _ in ego._em:ego.upd(_)

    def upd(ego, gi=1, fc='n'):
        ego._li+=gi
        ego._le+=ego._1e
        ego._ld+=ego._1d
        ego.ocn_[fc]()

    def ocn_rnt(ego):
        _qi_fil=round(ego._ld)
        if _qi_fil >= ego._qi: _qi_fil = ego._qi -1
        text = "\rProgress: [{}] {:.2f}‰".format(
            "#"*_qi_fil+"-"*(ego._qi-_qi_fil), ego._le*1000)
        sys.stdout.write(text)
        sys.stdout.flush()
        #if _qi_fil > ego._qi: sys.stdout.write('\n')
    def ocn(ego):
        _qi_fil=int(ego._qi * ego._li // ego._gi)
        bar = '='*_qi_fil + '-' * (ego._gi - _qi_fil)
        percent = f"{ego._li / ego._gi * 100:.1f}%"
        print(f"\r{ego._jc}: [{bar}] {ego._li}/{ego._gi} {percent} {ego._zc}", end='', flush=True)

    def close(ego):
        print()  # Move to the next line after done

class TIST:
    def __init__(ego,od):
        ego._em=list()
    def upd(ego, ox):
        ego._em.append( ox)

    def __call__(ego,*c,**g) -> Any:
        for _ in ego._em:ego.upd(_) # 将环中变量添入列
        return   ego._em





# catch-return the yield value
def tddmEld( rs):             # 可迭代对象
    return TDDM( rs)()

# catch-return the yield value
def catrEld( rs):             # 可迭代对象
    return TIST( rs)()

# catch-return the yield value
def tqdmEld( rs):             # 可迭代对象
    for _ in _dm(rs,total=getattr(rs,'__len__',lambda:67)(),ncols=67):pass # 将环中变量添入列

def DDD( rs, ar):
    return ar(rs)()


def get_iterator( it, am):
    return am(it)if isinstance(it,Iterator)else\
           am(it[0](*it[1:]))if isinstance(it,tuple)else am(it)


def add_tqdm_decorator(func):
    @wraps(func)
    def wrapper( *c,**g):
        # 获取函数体内的for循环迭代器, 修改为传入迭代器或使用闭包
        if'it'in g:g['it']=get_iterator(g['it'],_dm)
        elif c:c= (get_iterator(c[0],_dm),)+c[1:]
        return func(*c, **g) # 调用原始函数
    return wrapper


TMyRM1=TM1(_dm)
TMyTDD=TM1(tddmEld)
TMyTQD=TM1(tqdmEld)
TMyCAT=TM1(catrEld)

if __name__ == '__main__':
    #pbar = TDDM(od=total_iters, jc="Progress", unit="items")


    @add_tqdm_decorator
    def odo_RSI( *c, it=(range,5)):
        if isinstance(it,tuple):it=it[0](*it[1:])
        for _ in it: pass # do by*c
    
    def eld_RSI( *c, it=(range,5)):
        if isinstance(it,tuple):it=it[0](*it[1:])
        for _ in it: yield _

    odo_RSI(range(5000000000))