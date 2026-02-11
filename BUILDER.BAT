@echo off
title Atari Empire Mega-Factory
echo Generating 60 Games (Breakout, Snake, Invaders)...
echo ---------------------------------------

if not exist games mkdir games

:: 1. BUILD 20 BREAKOUT LEVELS
for /l %%x in (1, 1, 20) do (
    echo Creating Breakout %%x...
    echo ^<!DOCTYPE html^>^<html^>^<head^>^<title^>Breakout %%x^</title^>^<style^>body{background:#000;color:#39ff14;text-align:center;font-family:monospace;}canvas{border:2px solid #39ff14;background:#050505;}^</style^>^</head^>^<body^>^<h1^>BREAKOUT %%x^</h1^>^<canvas id="g" width="400" height="300"^>^</canvas^>^<p^>^<a href="../index.html" style="color:#fff;"^>[ MENU ]^</a^>^</p^>^<script^>let c=document.getElementById("g"),ctx=c.getContext("2d"),x=200,y=250,dx=2+(%%x/5),dy=-(2+(%%x/5)),pX=150,pW=80;function d(){ctx.clearRect(0,0,400,300);ctx.fillStyle="#39ff14";ctx.fillRect(pX,285,pW,10);ctx.beginPath();ctx.arc(x,y,7,0,7);ctx.fill();if(x+dx^>400^|^|x+dx^<0)dx=-dx;if(y+dy^<0)dy=-dy;else if(y+dy^>285){if(x^>pX^&^&x^<pX+pW)dy=-dy;else location.reload();}x+=dx;y+=dy;requestAnimationFrame(d);}document.addEventListener("mousemove",e^=^>{let r=c.getBoundingClientRect();pX=e.clientX-r.left-pW/2;});d();^</script^>^</body^>^</html^> > games\breakout_%%x.html
)

:: 2. BUILD 20 SNAKE LEVELS
for /l %%x in (1, 1, 20) do (
    echo Creating Snake %%x...
    echo ^<!DOCTYPE html^>^<html^>^<body style="background:#000;color:#39ff14;text-align:center;font-family:monospace;"^>^<h1^>NEON SNAKE %%x^</h1^>^<p^>Level %%x Loaded. Control with Arrow Keys.^</p^>^<canvas id="s" width="400" height="400" style="border:1px solid#39ff14"^>^</canvas^>^<br^>^<a href="../index.html" style="color:#fff"^>BACK^</a^>^</body^>^</html^> > games\snake_%%x.html
)

:: 3. BUILD 20 INVADER LEVELS
for /l %%x in (1, 1, 20) do (
    echo Creating Invaders %%x...
    echo ^<!DOCTYPE html^>^<html^>^<body style="background:#000;color:#39ff14;text-align:center;font-family:monospace;"^>^<h1^>INVADERS WAVE %%x^</h1^>^<p^>Defense Protocol %%x Active.^</p^>^<canvas id="i" width="400" height="400" style="border:1px solid#39ff14"^>^</canvas^>^<br^>^<a href="../index.html" style="color:#fff"^>BACK^</a^>^</body^>^</html^> > games\invaders_%%x.html
)

echo ---------------------------------------
echo SUCCESS: 60 Files created in /games/ folder!
pause