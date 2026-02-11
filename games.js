// This script automatically builds the list of 60 games for your menu
var gameData = [];

// 1. GENERATE 20 BREAKOUT LEVELS
for (var i = 1; i <= 20; i++) {
    gameData.push({
        "title": "Breakout Level " + i,
        "link": "games/breakout_" + i + ".html",
        "desc": "Speed Level: " + (2 + (i / 5)).toFixed(1) + "x"
    });
}

// 2. GENERATE 20 NEON SNAKE LEVELS
for (var j = 1; j <= 20; j++) {
    gameData.push({
        "title": "Neon Snake V" + j,
        "link": "games/snake_" + j + ".html",
        "desc": "Slither Mode: Phase " + j
    });
}

// 3. GENERATE 20 INVADERS STRIKE LEVELS
for (var k = 1; k <= 20; k++) {
    gameData.push({
        "title": "Invaders Wave " + k,
        "link": "games/invaders_" + k + ".html",
        "desc": "Defense Protocol: " + k
    });
}

// Console log to confirm 60 games are loaded
console.log("Atari Empire Database: " + gameData.length + " games active.");