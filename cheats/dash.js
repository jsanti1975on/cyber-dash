let frames = [];
let speechframes = [];
let frameindex = 0;
let speechIndex = 0;
let typingSpeed = 50;
let lineDelay = 2000;

async function loadAssets() {
  try {
    const framesRes = await fetch("assets/tux-frames.txt");
    const framesText = await frameRes.text();
    frames = framesText.split("---").map(f => f.trim());
    console.log("Frames loaded:", frames);

    const speechRes = await fetch("assets/tux-speech.txt");
    const speechText = await speechRes.text();
    speechLines = speechText.split("\n").filter(line => line.trim().length > 0);
    console.log("Speech lines loaded:", speechLines);

    startAnimation();
   
