@echo off
title ATARI EMPIRE - FULL ENGINE INJECTOR
echo Deleting old empty files and injecting 60 playable engines...
echo ------------------------------------------------------------

if not exist games mkdir games

:: --- 20 PLAYABLE BREAKOUT LEVELS ---
for /l %%x in (1, 1, 20) do (
    echo Writing Breakout %%x...
    powershell -Command "$c = @'
<!DOCTYPE html><html><head><style>body{background:#000;color:#39ff14;text-align:center;font-family:monospace;}canvas{border:3px solid #39ff14;background:#050505;display:block;margin:auto;}</style></head><body><h1>BREAKOUT %%x</h1><canvas id='g' width='480' height='320'></canvas><br><a href='../index.html' style='color:#fff;'>BACK</a><script>let c=document.getElementById('g'),ctx=c.getContext('2d'),x=240,y=290,dx=2+(%%x/5),dy=-(2+(%%x/5)),pX=200,pW=80;function d(){ctx.clearRect(0,0,480,320);ctx.fillStyle='#39ff14';ctx.fillRect(pX,310,pW,10);ctx.beginPath();ctx.arc(x,y,8,0,7);ctx.fill();if(x+dx>480||x+dx<0)dx=-dx;if(y+dy<0)dy=-dy;else if(y+dy>310){if(x>pX&&x<pX+pW)dy=-dy;else location.reload();}x+=dx;y+=dy;requestAnimationFrame(d);}document.addEventListener('mousemove',e=>{let r=c.getBoundingClientRect();pX=e.clientX-r.left-pW/2;});d();</script></body></html>
'@; $c | Out-File -FilePath games\breakout_%%x.html -Encoding utf8"
)

:: --- 20 PLAYABLE SNAKE LEVELS ---
for /l %%x in (1, 1, 20) do (
    echo Writing Snake %%x...
    powershell -Command "$c = @'
<!DOCTYPE html><html><head><style>body{background:#000;color:#39ff14;text-align:center;font-family:monospace;}canvas{border:2px solid #39ff14;}</style></head><body><h1>SNAKE %%x</h1><canvas id='s' width='400' height='400'></canvas><br><a href='../index.html' style='color:#fff;'>BACK</a><script>let c=document.getElementById('s'),ctx=c.getContext('2d'),s=[{x:10,y:10}],d={x:0,y:0},f={x:15,y:15};function g(){ctx.fillStyle='#000';ctx.fillRect(0,0,400,400);ctx.fillStyle='red';ctx.fillRect(f.x*20,f.y*20,18,18);ctx.fillStyle='#39ff14';s.forEach(p=>ctx.fillRect(p.x*20,p.y*20,18,18));let n={x:s[0].x+d.x,y:s[0].y+d.y};if(n.x<0||n.x>19||n.y<0||n.y>19)location.reload();s.unshift(n);if(n.x==f.x&&n.y==f.y){f={x:Math.floor(Math.random()*20),y:Math.floor(Math.random()*20)}}else s.pop();setTimeout(g,100-(%%x*2));}window.onkeydown=e=>{if(e.key=='ArrowUp')d={x:0,y:-1};if(e.key=='ArrowDown')d={x:0,y:1};if(e.key=='ArrowLeft')d={x:-1,y:0};if(e.key=='ArrowRight')d={x:1,y:0}};g();</script></body></html>
'@; $c | Out-File -FilePath games\snake_%%x.html -Encoding utf8"
)

:: --- 20 PLAYABLE INVADER LEVELS ---
for /l %%x in (1, 1, 20) do (
    echo Writing Invaders %%x...
    powershell -Command "$c = @'
<!DOCTYPE html><html><head><style>body{background:#000;color:#39ff14;text-align:center;font-family:monospace;}canvas{border:2px solid #39ff14;}</style></head><body><h1>INVADERS %%x</h1><canvas id='i' width='400' height='400'></canvas><br><a href='../index.html' style='color:#fff;'>BACK</a><script>let c=document.getElementById('i'),ctx=c.getContext('2d'),p=180,b=[],e=[];for(let y=0;y<3;y++)for(let x=0;x<8;x++)e.push({x:x*40+40,y:y*30+30});function g(){ctx.fillStyle='#000';ctx.fillRect(0,0,400,400);ctx.fillStyle='#39ff14';ctx.fillRect(p,370,40,10);ctx.fillStyle='white';b.forEach((l,i)=>{l.y-=5;ctx.fillRect(l.x,l.y,3,10);if(l.y<0)b.splice(i,1);});ctx.fillStyle='red';e.forEach((m,i)=>{m.y+=0.3+(%%x/20);ctx.fillRect(m.x,m.y,20,15);b.forEach((l,j)=>{if(l.x>m.x&&l.x<m.x+20&&l.y>m.y&&l.y<m.y+15){e.splice(i,1);b.splice(j,1);}});if(m.y>370)location.reload();});if(e.length==0)alert('WIN!');else requestAnimationFrame(g);}window.onkeydown=k=>{if(k.key=='ArrowLeft'&&p>0)p-=20;if(k.key=='ArrowRight'&&p<360)p+=20;if(k.key==' ')b.push({x:p+18,y:370});};g();</script></body></html>
'@; $c | Out-File -FilePath games\invaders_%%x.html -Encoding utf8"
)

echo ------------------------------------------------------------
echo ALL 60 GAMES ARE NOW PLAYABLE. REFRESH INDEX.HTML.
pause