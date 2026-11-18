import json
B=0.412
sh=[("518",0.5,4),("550",2.0,8),("507",0.5,12),("518",4.0,14),("550",10.0,20),("518",6.0,25),("507",8.0,30),
    ("507",14.0,36),("518",12.5,40),("518",21.0,44),("518",27.0,48),("518",37.0,53),("518",42.5,57),
    ("518",49.6,61),("507",40.8,66),("550",12.0,71),("550",32.0,76),("515",0.2,81)]
shots=[dict(src=f"raw/{s}.mp4",**{"in":i},until=round(k*B,3)) for s,i,k in sh]
json.dump(shots,open("shots.json","w"),indent=1)
T=lambda k:round(k*B,3)
FACE=[180,200,720,1000]
fx=[dict(type="flicker",t=0.824,frames=10,mode="white",mask=dict(auto="skin",box=FACE,feather=6)),
 dict(type="flicker",t=2.47,frames=12,mode="invert",blink=True,mask=dict(auto="skin",box=FACE,feather=3)),
 dict(type="frameflick",t=T(8),frames=10,box=[135,520,810,880]),
 dict(type="maskframe",t=T(14),frames=12,grid=[3,2],order=[0,4,2,3,1,5]),
 dict(type="flicker",t=7.0,frames=12,mode="glow",mask=dict(auto="skin",box=FACE,feather=4)),
 dict(type="frameflick",t=T(20),frames=10,box=[90,600,900,800]),
 dict(type="maskframe",t=T(25),frames=12,grid=[2,3],order=[0,3,4,1,2,5]),
 dict(type="frameflick",t=T(36),frames=10,box=[135,480,810,960]),
 dict(type="flicker",t=16.9,frames=12,mode="glow",mask=dict(auto="sat",thr=90,box=[120,150,840,950],feather=4)),
 dict(type="maskframe",t=T(48),frames=12,grid=[3,3],order=[4,0,8,2,6,1,7,3,5]),
 dict(type="flicker",t=20.6,frames=12,mode="glow",mask=dict(auto="sat",thr=90,box=[120,150,840,950],feather=4)),
 dict(type="frameflick",t=T(57),frames=10,box=[180,560,720,820]),
 dict(type="flicker",t=24.3,frames=12,mode="glow",mask=dict(auto="skin",box=FACE,feather=4)),
 dict(type="maskframe",t=T(66),frames=12,grid=[3,3],order=[0,8,2,6,4,1,7,3,5]),
 dict(type="frameflick",t=T(71),frames=10,box=[135,520,810,880]),
 dict(type="flicker",t=31.6,frames=12,mode="invert",blink=True,mask=dict(auto="skin",box=FACE,feather=3))]
ov=[
 dict(type="stack",start=0.3,end=1.65,y=0.22,lines=[dict(text="Skincare cả chục bước",style="small")]),
 dict(type="stack",start=1.65,end=3.3,y=0.22,lines=[dict(text="Skincare cả chục bước",style="small"),dict(text="mà da vẫn xỉn?",style="caps",color="#FFB347",size=86)]),
 dict(type="stack",start=3.37,end=5.77,y=0.22,lines=[dict(text="có khi lỗi nằm ở",style="small"),dict(text="bước rửa mặt",style="serif",color="#F7C6D9",size=124)]),
 dict(type="stack",start=5.85,end=8.24,y=0.22,lines=[dict(text="tối nào mình cũng dùng",style="small"),dict(text="Halio 5 in 1",style="caps",color="#BFE6F7",size=90)]),
 dict(type="label",start=8.55,end=12.36,text="Bước 1 · Rửa mặt",color="yellow",y=0.16,size=44),
 dict(type="stack",start=12.43,end=14.75,y=0.22,lines=[dict(text="sạch kỹ",style="small"),dict(text="mà vẫn êm da",style="serif",color="#F7C6D9",size=124)]),
 dict(type="label",start=14.75,end=16.1,text="Bước 2 · Thoa serum",color="pink",y=0.16,size=44),
 dict(type="label",start=16.15,end=19.78,text="Ấm 42° · đèn đỏ · massage",color="pink",y=0.16,size=44),
 dict(type="label",start=19.94,end=23.4,text="Bước 3 · Mát 16° · đèn xanh",color="blue",y=0.16,size=44),
 dict(type="stack",start=23.47,end=27.19,y=0.22,lines=[dict(text="da mềm",style="small"),dict(text="ẩm mướt",style="serif",color="#F7C6D9",size=132)]),
 dict(type="stack",start=27.32,end=29.3,y=0.22,lines=[dict(text="máy Halio",style="small"),dict(text="link ở giỏ hàng",style="caps",color="#FFB347",size=86)]),
 dict(type="stack",start=29.37,end=33.37,y=0.22,lines=[dict(text="bạn rửa mặt bằng",style="small"),dict(text="tay hay máy?",style="serif",color="#BFE6F7",size=132),dict(text="comment cho mình biết nha",style="small")]),
]
caps=[(0.3,2.3,"Skincare cả chục bước"),(2.3,3.37,"mà da vẫn xỉn?"),(3.37,5.8,"Có khi lỗi nằm ở bước rửa mặt."),
 (5.85,8.5,"Tối nào mình cũng dùng em Halio này."),(8.55,10.3,"Bước một, rửa mặt:"),(10.35,12.4,"đánh nhẹ cùng sữa rửa mặt,"),
 (12.43,14.7,"sạch kỹ mà vẫn êm da."),(14.75,16.1,"Thoa serum xong,"),(16.15,17.9,"bật chế độ ấm đèn đỏ,"),
 (17.93,19.85,"massage từ trong ra ngoài."),(20.0,21.9,"Vùng chữ T thì mình chuyển"),(21.95,23.4,"chế độ mát, đèn xanh."),
 (23.47,25.25,"Xong là da mềm,"),(25.29,27.25,"ẩm mướt, nhìn tươi hẳn."),(27.32,29.3,"Máy Halio để trong giỏ hàng nha."),
 (29.37,31.5,"Bạn rửa mặt bằng tay hay bằng máy?"),(31.55,32.9,"Comment cho mình biết nhé.")]
json.dump([dict(start=a,end=b,text=t) for a,b,t in caps],open("captions.json","w"),ensure_ascii=False,indent=1)
plan=dict(base="work/base.mp4",output="halio_flicker.mp4",grade="warm",audio="work/mix.wav",captions="captions.json",
  caption_style="pill",music=dict(src="music/flicker.mp3",volume=0.08),fx=fx,overlays=ov)
json.dump(plan,open("plan.json","w"),ensure_ascii=False,indent=1)
ev=[["anvil",0.05]]
for f in fx:
  t=f["t"]
  if f["type"]=="frameflick": ev.append(["glitch",round(t-0.33,3)])
  elif f["type"]=="maskframe": ev+= [["whoosh",round(t-0.45,3)],["click",round(t-0.4,3)]]
  else: ev.append(["shutter" if f.get("mode")=="white" else "click",t])
for o in ov:
  if o["start"]>1: ev.append(["pop",round(o["start"],3)])
ev.append(["sparkle",23.5])
ev.sort(key=lambda e:e[1])
json.dump(ev,open("sfx.json","w"))
