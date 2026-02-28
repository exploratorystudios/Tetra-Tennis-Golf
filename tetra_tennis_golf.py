def g(s,c=__import__('curses'),R=__import__('random').randint,rg=range,_qi=(lambda st,gc:lambda s:next((lk,k)for cur in[gc(s)]for lk in[(cur&{260}-st[0]and 260)or(cur&{261}-st[0]and 261)or(st[1]if st[1]in cur else 260*(260 in cur)or 261*(261 in cur)or-1)]for k in[next((v for v in[259,32,99]if v in cur and v not in st[0]),258 if 258 in cur else-1)]for _ in[st.__setitem__(0,cur),lk>0 and st.__setitem__(1,lk)]))([set(),-1],(lambda mv,u,D:lambda s:{v for v,k in zip([260,261,258],[0x25,0x27,0x28])if u(k)&0x8000}|{x for x in[D(mv)for _ in iter(mv.kbhit,0)]if x!=-1})(__import__('msvcrt'),__import__('ctypes').windll.user32.GetAsyncKeyState,lambda mv:(lambda r:{b'K':260,b'M':261,b'H':259,b'P':258,b' ':32,b'c':99}.get(mv.getch()if r in(b'\xe0',b'\x00')else r,-1))(mv.getch()))if __import__('os').name=='nt'else(lambda d,b:(lambda*kc:lambda s:{v for v,k in zip([260,261,259,258,32,99],kc)if b(d.query_keymap(),k)}|{*iter(s.getch,-1)})(*[d.keysym_to_keycode(x)for x in[0xff51,0xff53,0xff52,0xff54,0x20,0x63]]))(__import__('Xlib.display',fromlist=[0]).Display(),lambda m,k:bool(m[k>>3]&(1<<(k&7))))if __import__('importlib.util',fromlist=[0]).find_spec('Xlib')else lambda s:{*iter(s.getch,-1)})):
 not[s.nodelay(1),c.start_color(),c.use_default_colors(),(AR:=c.A_REVERSE),(CP:=c.color_pair)]+[c.init_pair(i+1,[51,27,208,226,46,196,201][i],-1)for i in rg(7)]+[c.curs_set(0)]
 H,W,BX=40,10,s.getmaxyx()[1]//2-10
 B=[[0]*W for _ in rg(42)]
 P=[[15,4369],[113,275,71,802],[116,785,23,547],[51],[54,561],[39,562,114,305],[99,306]]
 F=lambda m:[(r,cc)for r in rg(4)for cc in rg(4)if m>>r*4+cc&1]
 C=lambda m,x,y:any(y+r*2+1>=H or not(0<=x+cc<W)or B[y+r*2][x+cc]or B[y+r*2+1][x+cc]for r,cc in F(m))
 x,y,m,sc,t,npi,hp,hu,lk=3,0,P[pi:=R(0,6)][ri:=0],0,0,R(0,6),-1,0,-1
 while 1:
  lk,k=_qi(s)
  _y,_H=y&~1,rg(H//2)
  x,y,m,pi,hp,npi,ri,hu=next((3 if _h else x-1 if lk==260 and not C(m,x-1,_y)else x+1 if lk==261 and not C(m,x+1,_y)else x,0 if _h else next(i for i in rg(_y,H,2)if C(m,x,i+2))if k==32 else y,P[hp if hp>=0 else npi][0]if _h else m,(hp if hp>=0 else npi)if _h else pi,pi if _h else hp,(R(0,6)if hp<0 else npi)if _h else npi,0 if _h else ri,1 if _h else hu)for _h in[k==99 and not hu]for _y in[y&~1])
  if k==259 and not C(P[pi][(ri+1)%len(P[pi])],x,_y):m=P[pi][ri:=(ri+1)%len(P[pi])]
  if k in{258,32}or not t%max(1,10-sc//10):
   if C(m,x,(_y:=y&~1)+2):
    [B[_y+r*2+pr].__setitem__(x+cc,pi+1)for r,cc in F(m) for pr in[0,1]if 0<=_y+r*2+pr<H and 0<=x+cc<W]
    sc+=(n:=sum(all(B[tr*2])and all(B[tr*2+1])for tr in _H))
    B[:]=[[0]*W for _ in rg(2*n)]+[rw for p in zip(B[:H:2],B[1:H:2])if not(all(p[0])and all(p[1]))for rw in p]+[[0]*W]*2
    x,y,m,pi,npi,hu=3,0,P[npi][ri:=0],npi,R(0,6),0
    if C(m,x,0):s.addstr(10,BX+6,"GAME OVER") or s.refresh() or c.napms(2000) or exit()
   else:y+=2 if k==258 and not C(m,x,_y+4) else 1
  s.erase() or not[s.addstr(0,BX,'╔'+'═'*(W*2)+'╗',AR),s.addstr(H//2+1,BX,'╚'+'═'*(W*2)+'╝',AR),s.addstr(0,BX+1,f"Score:{sc}",AR),s.addstr(2,BX+W*2+3,"NEXT"),s.addstr(2,BX-9,"HOLD")]+[s.addstr(tr+1,BX,'║',AR)or s.addstr(tr+1,BX+W*2+1,'║',AR)for tr in _H]+[s.addstr(tr+1,BX+cc*2+1,next(' ▄▀█'[qt*2+qb]if qt or qb else' ▄▀█'[bool(B[tr*2][cc])*2+bool(B[tr*2+1][cc])]if B[tr*2][cc]or B[tr*2+1][cc]else'▒'if(tr*2,cc)in G or(tr*2+1,cc)in G else' 'for qt in[(tr*2,cc)in Q]for qb in[(tr*2+1,cc)in Q])*2,CP(pi+1 if(tr*2,cc)in Q or(tr*2+1,cc)in Q else B[tr*2][cc]or B[tr*2+1][cc]or(pi+1 if(tr*2,cc)in G or(tr*2+1,cc)in G else 0)))for gy in[next(i for i in rg(y&~1,H,2)if C(m,x,i+2))]for G in[{(gy+r*2+pr,x+cc)for r,cc in F(m) for pr in[0,1]}]for Q in[{(y+r*2+pr,x+cc)for r,cc in F(m) for pr in[0,1]}]for tr in _H for cc in rg(W)]
  not[s.addstr(r+4,BX+W*2+3+cc*2,'██',CP(npi+1))for r,cc in F(P[npi][0])]+[s.addstr(r+4,BX-9+cc*2,'██',CP(hp+1))for r,cc in(F(P[hp][0])if hp>=0 else[])] or s.refresh() or not[t:=t+1]
  c.napms(99)
__import__("curses").wrapper(g)
