import json,os,urllib.request as W
S8=[q for q in range(120)if q%16<8]
ND=[33,31,18,14,-33,-31,-18,-14]
BD=[17,15,-17,-15]
RD=[16,1,-16,-1]
DD=[0,[15,17],ND,BD,RD,BD+RD,BD+RD]
V=[0,100,320,330,500,900,0]
CM={0:2,7:1,4:3,112:8,119:4,116:12}
def A(b,q,t):
    for a in range(1,7):
        for d in DD[a]:
            x=q-d*t
            while not x&136:
                if b[x]==a*t:return 1
                if b[x]or a in(1,2,6):break
                x-=d*t
    return 0
def Ev(b,s):
    v=n=k=0
    for q in S8:
        p=b[q]
        if p:
            a=abs(p);w=p//a;m=14-abs(2*(q&7)-7)-abs(2*(q>>4)-7)
            if a<6:v+=w*(V[a]+m*int("013201"[a])+(a<2)*7*(q>>4 if w>0 else 7-(q>>4)));n+=V[a]
            else:k+=w*m
    return(v+k*(4 if n<3500 else-3))*s
def G(b,s,c,q):
    M=[]
    def a(f,x):
        t=abs(b[x]);r=5*(p==1 and x%112<8)
        M.append(((1000+8*t-p if t else 0)+160*r,f,x,r))
    for f in S8:
        p=b[f]*s
        if p<1:continue
        if p==1:
            x=f+16*s
            if not b[x]:
                if not q or x%112<8:a(f,x)
                if not q and f>>4==3.5-s*2.5 and not b[x+16*s]:a(f,x+16*s)
            for d in(15,17):
                x=f+d*s
                if not x&136 and b[x]*s<0:a(f,x)
            continue
        if p==6 and not q and not A(b,f,-s):
            for w,u in(1,0),(-1,1):
                if c>>1-s&1+u and not any(b[f+w*i]for i in range(1,3+u))and not A(b,f+w,-s):a(f,f+2*w)
        for d in DD[p]:
            x=f+d
            while not x&136:
                t=b[x]*s
                if t<0 or t==0 and not q:a(f,x)
                if t or p in(2,6):break
                x+=d
    return M
def X(b,s,c,f,x,r):
    n=b[:];p=n[f]
    n[f]=0;n[x]=r*s or p
    if abs(p)==6 and abs(x-f)==2:i=x+1 if x>f else x-2;n[(f+x)//2]=n[i];n[i]=0
    return n,-s,c&~(CM.get(f,0)|CM.get(x,0))
def S(b,s,c,d,a,B,y):
    global N,BM
    N+=1
    if N>L:raise OverflowError
    ch=A(b,b.index(6*s),-s)
    d=max(d,ch);q=d<1;o=a;m0=0
    if q:
        best=Ev(b,s)
        if best>=B:return best
        a=max(a,best)
    else:
        k=(tuple(b),s)
        if y and k in R:return 0
        t=T.get(k)
        if t:
            m0=t[3];f=t[1]
            if y and t[0]>=d and(f<1 or f<2 and t[2]>=B):return t[2]
        if d>2 and y and not ch and Ev(b,s)>=B and any(1<x*s<6 for x in b):
            v=-S(b,-s,c,d-3,-B,1-B,y+1)
            if v>=B:return v
        best=-1e5;R.add(k)
    ms=G(b,s,c,q)
    ms.sort(key=lambda m:(m==m0,m[0]+(m[1:3]==K.get(y))*900,m),reverse=True)
    j=0;bm=0
    for m in ms:
        z,f,x,r=m
        n=X(b,s,c,f,x,r)
        if A(n[0],n[0].index(6*s),-s):continue
        j+=1
        r=j>3 and d>2 and z<1000
        v=-S(*n,d-1-r,-a-1 if r else-B,-a,y+1)
        if r and v>a:v=-S(*n,d-1,-B,-a,y+1)
        if v>best:
            best=v;bm=m
            if y<1:BM=m
            if v>a:
                a=v
                if a>=B:
                    if z<1000:K[y]=(f,x)
                    break
    if not q:
        R.discard(k)
        if not j:return(y-30000)*ch
        T[k]=(d,(best>=B)or 2*(best<=o),best,bm)
    return best
def F(z):
    p,t,c=z.split()[:3];b=[0]*128;i=112
    for g in p:
        if g=='/':i-=24
        elif g.isdigit():i+=int(g)
        else:b[i]="PNBRQK".find(g)+1 or-1-"pnbrqk".find(g);i+=1
    return b,2*(t>'b')-1,sum(1<<"KQkq".find(g)for g in c if g>'-')
H=set()
U=lambda q:chr(97+(q&7))+chr(49+(q>>4))
def pick(g):
    global N,L,R,T,K
    st=F(g["fen"])
    if g["plies"]<10:H.clear()
    N=0;L=60000;T={};K={};R=set(H);H.add((tuple(st[0]),st[1]))
    for d in range(1,40):
        if N*3>L:break
        try:S(*st,d,-1e5,1e5,0)
        except OverflowError:break
    _,f,x,r=BM
    return U(f)+U(x)+"q"[:r]
def P(p,o):return json.load(W.urlopen(os.environ["MAKEFUN_ENV_URL"]+p,json.dumps(o).encode()))
g=P("/game",{})
while g["status"]!="done":
    if g["status"]=="your_move":
        l=g["legal_moves"]
        try:m=pick(g)
        except:m=0
        if m not in l:m=l[0]
        g=P("/move",{"game":g["game"],"move":m})
    else:g=P("/game",{})
