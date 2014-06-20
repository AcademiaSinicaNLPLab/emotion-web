function polyfillRequestAnimFrame (window) {
    var lastTime = 0;
    var vendors = ['ms', 'moz', 'webkit', 'o'];
    for(var x = 0; x < vendors.length && !window.requestAnimationFrame; ++x) {
        window.requestAnimationFrame = window[vendors[x]+'RequestAnimationFrame'];
        window.cancelAnimationFrame =
          window[vendors[x]+'CancelAnimationFrame'] || window[vendors[x]+'CancelRequestAnimationFrame'];
    }

    if (!window.requestAnimationFrame)
        window.requestAnimationFrame = function(callback, element) {
            var currTime = new Date().getTime();
            var timeToCall = Math.max(0, 16 - (currTime - lastTime));
            var id = window.setTimeout(function() { callback(currTime + timeToCall); },
              timeToCall);
            lastTime = currTime + timeToCall;
            return id;
        };

    if (!window.cancelAnimationFrame)
        window.cancelAnimationFrame = function(id) {
            clearTimeout(id);
        };
}
polyfillRequestAnimFrame(window);


// Get the canvas DOM element along with it's 2D context
// which is basically what we do our work on

var canvas = document.getElementById('canvas'),
    ctx = canvas.getContext('2d'),
    window_width = window.innerWidth,
    window_height = window.innerHeight;

// Set canvas's width and height to that
// of window (the view port)
canvas.width = window_width;
canvas.height = window_height;

// Just a random object name to store some utility
// functions that we can use later
var $$ = {
  // Get a random integer from a range of ints
  // Usage: $$.randomInt(4, 8) -> would return
  // 4 or 5 or 6 or 7 or 8
  randomInt: function(min, max) {
    return Math.floor( Math.random() * (max - min + 1) + min );
  }
};

var mousePos = { x: (window_width/2), y: (window_height/2) }

// Pool of particles. Basically an array that stores all
// our particles
var particles = [];

// The object that'll serve as the prototype
// of every particle we create!
var Particle = {
  x: mousePos.x,
  y: mousePos.y,
  x_speed: 2,
  y_speed: 2,
  radius: 3,
  x_curve: 0,
  y_curve: 0,
  colorStart: 0,
  b: 50,
  _position: {},
  
  // Draw the particle
  draw: function() {
    // Begin Drawing Path
    ctx.beginPath();
    // Background color for the object that we'll draw
    ctx.fillStyle = this.bg_color;       
    // Draw the arc
    // ctx.arc(x, y, radius, start_angle, end_angle, anticlockwise)
    // angle are in radians
    // 360 degrees = 2π radians or 1 radian = 360/2π = 180/π degrees
    ctx.arc(this.x, this.y, this.radius, 0, Math.PI*2, false);
    // Close Drawing Path
    ctx.closePath();
    // Fill the canvas with the arc
    ctx.fill();


  },
  
  // These are just some helpers that
  // I've created, got no use in this
  // creation. These might give you some idea
  // to do some funky things .. Who knows ? :)
  trackPosition: function() {
    var position = {x: this.x, y: this.y};
    
    this._position.x = this.x;
    this._position.y = this.y;
  },
  getPosition: function() {
    return this._position;
  }
};

function createParticle() {
  // Create a particle object and use `Particle`
  // as the prototype of the object. I hope you know
  // about prototypes right ? Prototypal Inheritance, nope ? :S
  var particle = Object.create(Particle);
  
  // Random number between -5 and 5 using
  // our utility function, that was defined above.
  particle.colorStart = $$.randomInt(0, 128); 
  // particle.x = mousePos.x;
  particle.x = -50;
  // particle.y = mousePos.y;
  particle.y = canvas.height;
  particle.radius = $$.randomInt(4,10);
  particle.x_speed = $$.randomInt(-1, 1);
  particle.y_speed = $$.randomInt(-1, 1);
  particle.x_curve = ($$.randomInt(0, 40) / 100),
  particle.y_curve = ($$.randomInt(-20, 20) / 100),
  // Push the newly created particle
  // into our master array
  particles.push(particle);
}

function repaint() {
  // Clear the entire Canvas
  // ctx.fillStyle = 'rgba(238,238,238,0.5)';
  ctx.fillStyle = 'rgba(23,23,23,0.5)';
  ctx.fillRect(0, 0, window_width, window_height);
  
  // Re-draw all particles we have in our bag!
  for (var i = 0; i < particles.length; i++) {
    var particle = particles[i];
    
    // Set the new particle's background color
    // HSLA FTW!
    particle.b -= 0.6;
    particle.bg_color = "hsla("+((i)+particle.colorStart)+", 90%, 50%, "+(particle.b/50)+")";
    
    // This restriction makes sure
    // that your computer does not
    // run out of RAM and hence slows down.
    if (particles.length > 500) {
      particles.shift();
    }
    
    particle.draw();

    // Changing x and y co-ordinates which
    // are random (generated in createParticle())
    //
    // This is cool, as we get different
    // speed for each particles then!
    particle.x_speed += particle.x_curve/1.1;
    particle.y_speed += particle.y_curve/1.6;
    particle.x = particle.x + particle.x_speed;
    particle.y = particle.y + particle.y_speed;
    
    // Track new position
    // Just a helper that might give you some
    // cool ideas to make some unique twists to this
    // experiment.
    particle.trackPosition();
  }
}

window.onmousemove = function (event) {
    event = event || window.event; // IE-ism
    mousePos.x = event.clientX;// - (window_width/2);
    mousePos.y = event.clientY;// - (window_height/2);
}
  

// Magic method for animation!
function animate () {
  var i = 4;
  while ( !!i ) {
    createParticle();
    i--;
  }
  repaint();

  window.requestAnimationFrame(animate);
}
window.requestAnimationFrame(animate);