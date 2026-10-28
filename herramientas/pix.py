# Utilidades de pixel art: lienzo en baja resolución, contorno automático y escalado sin suavizado.
from PIL import Image, ImageDraw
def hexc(h, a=255):
    h=h.lstrip('#'); return (int(h[0:2],16),int(h[2:4],16),int(h[4:6],16),a)
class Canvas:
    def __init__(s,w,h): s.w,s.h=w,h; s.im=Image.new('RGBA',(w,h),(0,0,0,0)); s.px=s.im.load()
    def p(s,x,y,c):
        if 0<=x<s.w and 0<=y<s.h: s.px[x,y]=hexc(c) if isinstance(c,str) else c
    def rect(s,x0,y0,x1,y1,c):
        for y in range(y0,y1+1):
            for x in range(x0,x1+1): s.p(x,y,c)
    def ellipse(s,cx,cy,rx,ry,c):
        for y in range(int(cy-ry)-1,int(cy+ry)+2):
            for x in range(int(cx-rx)-1,int(cx+rx)+2):
                if ((x-cx)/max(rx,.01))**2+((y-cy)/max(ry,.01))**2<=1.0: s.p(x,y,c)
    def grid(s,rows,pal,ox=0,oy=0):
        for y,row in enumerate(rows):
            for x,ch in enumerate(row):
                if ch!='.' and ch in pal: s.p(ox+x,oy+y,pal[ch])
    def outline(s,c='#1a1020'):
        src=s.im.copy(); sp=src.load(); col=hexc(c)
        for y in range(s.h):
            for x in range(s.w):
                if sp[x,y][3]==0:
                    for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
                        nx,ny=x+dx,y+dy
                        if 0<=nx<s.w and 0<=ny<s.h and sp[nx,ny][3]>0 and sp[nx,ny][:3]!=col[:3]:
                            s.px[x,y]=col; break
        return s
    def out(s,scale): return s.im.resize((s.w*scale,s.h*scale),Image.NEAREST)
def save(im,path): im.save(path)
