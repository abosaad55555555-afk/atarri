Set fso = CreateObject("Scripting.FileSystemObject")
If Not fso.FolderExists("games") Then fso.CreateFolder("games")

'--- ENGINES ---
'Breakout engine with responsive resizing and touch/mouse logic
breakout_js = "let c=document.getElementById('canvas'),ctx=c.getContext('2d'),x,y,dx,dy,pX,pW=100; function res(){c.width=window.innerWidth;c.height=window.innerHeight*0.8;x=c.width/2;y=c.height-30;dx=4;dy=-4;pX=c.width/2-pW/2;} window.onresize=res;res(); function d(){ctx.clearRect(0,0,c.width,c.height);ctx.fillStyle='#39ff14';ctx.fillRect(pX,c.height-20,pW,10);ctx.beginPath();ctx.arc(x,y,10,0,Math.PI*2);ctx.fill();if(x+dx>c.width||x+dx<0)dx=-dx;if(y+dy<0)dy=-dy;else if(y+dy>c.height-20){if(x>pX&&x<pX+pW)dy=-dy;else location.reload();}x+=dx;y+=dy;requestAnimationFrame(d);} function mv(e){let t=e.touches?e.touches[0].clientX:e.clientX;pX=t-pW/2;if(e.touches)e.preventDefault();} c.addEventListener('mousemove',mv);c.addEventListener('touchmove',mv,{passive:false});d();"

'Snake engine with swipe detection and grid scaling
snake_js = "let c=document.getElementById('canvas'),ctx=c.getContext('2d'),s=[{x:10,y:10}],d={x:0,y:0},f={x:15,y:15},sz; function res(){c.width=c.height=Math.min(window.innerWidth,window.innerHeight*0.7);sz=c.width/20;} window.onresize=res;res(); function g(){ctx.fillStyle='#000';ctx.fillRect(0,0,c.width,c.height);ctx.fillStyle='red';ctx.fillRect(f.x*sz,f.y*sz,sz-2,sz-2);ctx.fillStyle='#39ff14';s.forEach(p=>ctx.fillRect(p.x*sz,p.y*sz,sz-2,sz-2));let n={x:s[0].x+d.x,y:s[0].y+d.y};if(n.x<0||n.x>19||n.y<0||n.y>19)location.reload();s.unshift(n);if(n.x==f.x&&n.y==f.y){f={x:Math.floor(Math.random()*20),y:Math.floor(Math.random()*20)}}else s.pop();setTimeout(g,100);} window.addEventListener('keydown',e=>{if(e.key=='ArrowUp'&&d.y!=1)d={x:0,y:-1};if(e.key=='ArrowDown'&&d.y!=-1)d={x:0,y:1};if(e.key=='ArrowLeft'&&d.x!=1)d={x:-1,y:0};if(e.key=='ArrowRight'&&d.x!=-1)d={x:1,y:0};}); let tsX,tsY;c.addEventListener('touchstart',e=>{tsX=e.touches[0].clientX;tsY=e.touches[0].clientY;});c.addEventListener('touchmove',e=>{if(!tsX||!tsY)return;let dx=tsX-e.touches[0].clientX,dy=tsY-e.touches[0].clientY;if(Math.abs(dx)>Math.abs(dy)){if(dx>0&&d.x!=1)d={x:-1,y:0};else if(d.x!=-1)d={x:1,y:0};}else{if(dy>0&&d.y!=1)d={x:0,y:-1};else if(d.y!=-1)d={x:0,y:1};}tsX=tsY=null;e.preventDefault();},{passive:false});g();"

'Invaders engine with tap-to-shoot and horizontal movement
invaders_js = "let c=document.getElementById('canvas'),ctx=c.getContext('2d'),p,b=[],e=[]; function res(){c.width=window.innerWidth;c.height=window.innerHeight*0.7;p=c.width/2;} window.onresize=res;res(); for(let y=0;y<3;y++)for(let x=0;x<8;x++)e.push({x:x*50+50,y:y*30+30}); function g(){ctx.fillStyle='#000';ctx.fillRect(0,0,c.width,c.height);ctx.fillStyle='#39ff14';ctx.fillRect(p-20,c.height-30,40,10);ctx.fillStyle='white';b.forEach((l,i)=>{l.y-=5;ctx.fillRect(l.x,l.y,3,10);if(l.y<0)b.splice(i,1);});ctx.fillStyle='red';e.forEach((m,i)=>{m.y+=0.3;ctx.fillRect(m.x,m.y,20,15);b.forEach((l,j)=>{if(l.x>m.x&&l.x<m.x+20&&l.y>m.y&&l.y<m.y+15){e.splice(i,1);b.splice(j,1);}});if(m.y>c.height-30)location.reload();});if(e.length==0)alert('WIN!');else requestAnimationFrame(g);} window.addEventListener('keydown',e=>{if(e.key=='ArrowLeft')p-=20;if(e.key=='ArrowRight')p+=20;if(e.key==' ')b.push({x:p,y:c.height-30});}); c.addEventListener('touchstart',e=>{let t=e.touches[0].clientX;if(t<c.width*0.3)p-=25;else if(t>c.width*0.7)p+=25;else b.push({x:p,y:c.height-30});e.preventDefault();}); g();"

For i = 1 To 20
    WriteFile "breakout_" & i, "BREAKOUT " & i, breakout_js
    WriteFile "snake_" & i, "SNAKE " & i, snake_js
    WriteFile "invaders_" & i, "INVADERS " & i, invaders_js
Next

Sub WriteFile(n, t, j)
    Set f = fso.CreateTextFile("games\" & n & ".html", True)
    f.WriteLine "<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no'><style>body{background:#000;color:#39ff14;text-align:center;font-family:monospace;margin:0;overflow:hidden;}canvas{display:block;margin:auto;touch-action:none;border-bottom:2px solid #39ff14;}</style></head><body>"
    f.WriteLine "<h2>" & t & "</h2><canvas id='canvas'></canvas><br><a href='../index.html' style='color:#fff;font-size:20px;text-decoration:none;'>[ EXIT ]</a>"
    f.WriteLine "<script>" & j & "</script></body></html>"
    f.Close
End Sub
MsgBox "All 60 Game Files Created!"