(function () {
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var canvas = document.createElement('canvas');
  canvas.id = 'sakura-canvas';
  canvas.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:9999;';
  document.body.appendChild(canvas);
  var ctx = canvas.getContext('2d');
  var petals = [];
  var W, H;
  function resize() {
    W = canvas.width = window.innerWidth;
    H = canvas.height = window.innerHeight;
  }
  window.addEventListener('resize', resize);
  resize();
  var COUNT = W < 768 ? 24 : 45;
  var colors = ['rgba(255,183,197,', 'rgba(255,214,224,', 'rgba(255,153,178,'];
  function makePetal(anywhere) {
    return {
      x: Math.random() * W,
      y: anywhere ? Math.random() * H : -30 - Math.random() * 80,
      size: 6 + Math.random() * 8,
      speed: 0.6 + Math.random() * 1.4,
      sway: 20 + Math.random() * 30,
      swaySpeed: 0.005 + Math.random() * 0.015,
      phase: Math.random() * Math.PI * 2,
      rot: Math.random() * Math.PI * 2,
      rotSpeed: (Math.random() - 0.5) * 0.03,
      alpha: 0.35 + Math.random() * 0.45,
      color: colors[Math.floor(Math.random() * colors.length)]
    };
  }
  for (var i = 0; i < COUNT; i++) petals.push(makePetal(true));
  function draw(p) {
    ctx.save();
    ctx.translate(p.x, p.y);
    ctx.rotate(p.rot);
    ctx.fillStyle = p.color + p.alpha + ')';
    ctx.beginPath();
    ctx.moveTo(0, -p.size);
    ctx.bezierCurveTo(p.size * 0.8, -p.size * 0.6, p.size * 0.8, p.size * 0.6, 0, p.size);
    ctx.bezierCurveTo(-p.size * 0.8, p.size * 0.6, -p.size * 0.8, -p.size * 0.6, 0, -p.size);
    ctx.fill();
    ctx.restore();
  }
  function loop() {
    ctx.clearRect(0, 0, W, H);
    for (var i = 0; i < petals.length; i++) {
      var p = petals[i];
      p.y += p.speed;
      p.x += Math.sin(p.phase) * 1.2;
      p.phase += p.swaySpeed;
      p.rot += p.rotSpeed;
      if (p.y > H + 50) { petals[i] = makePetal(false); continue; }
      if (p.x < -60) p.x = W + 40; else if (p.x > W + 60) p.x = -40;
      draw(p);
    }
    requestAnimationFrame(loop);
  }
  loop();
})();
