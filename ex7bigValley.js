
//RUN THIS WHOLE THING.  THE BOTTOM WILL ANIMATE IT.
function Vector(x, y) {
  this.x = x;
  this.y = y;
}
Vector.prototype.plus = function(other) {
  return new Vector(this.x + other.x, this.y + other.y);
};

Vector.prototype.times = function(multiplier) {
  return new Vector(this.x * multiplier, this.y * multiplier);
};

function Grid(width, height) {
  this.space = new Array(width * height);
  this.width = width;
  this.height = height;
}
Grid.prototype.isInside = function(vector) {
  return vector.x >= 0 && vector.x < this.width &&
         vector.y >= 0 && vector.y < this.height;
};
Grid.prototype.get = function(vector) {
  return this.space[vector.x + this.width * vector.y];
};
Grid.prototype.set = function(vector, value) {
  this.space[vector.x + this.width * vector.y] = value;
};

var directions = {
  "n":  new Vector( 0, -1),
  "ne": new Vector( 1, -1),
  "e":  new Vector( 1,  0),
  "se": new Vector( 1,  1),
  "s":  new Vector( 0,  1),
  "sw": new Vector(-1,  1),
  "w":  new Vector(-1,  0),
  "nw": new Vector(-1, -1)
};

function randomElement(array) {
  return array[Math.floor(Math.random() * array.length)];
}

var directionNames = "n ne e se s sw w nw".split(" ");

function elementFromChar(legend, ch) {
  if (ch == " ")
    return null;
  var element = new legend[ch]();
  element.originChar = ch;
  return element;
}

function charFromElement(element) {
  if (element == null)
    return " ";
  else
    return element.originChar;
}

function World(map, legend) {
  var grid = new Grid(map[0].length, map.length);
  this.grid = grid;
  this.legend = legend;
  this.year = 0;

  map.forEach(function(line, y) {
    for (var x = 0; x < line.length; x++)
      grid.set(new Vector(x, y),
               elementFromChar(legend, line[x]));
  });
}

World.prototype.toString = function() {
  var output = "";
  for (var y = 0; y < this.grid.height; y++) {
    for (var x = 0; x < this.grid.width; x++) {
      var element = this.grid.get(new Vector(x, y));
      output += charFromElement(element);
    }
    output += "\n";
  }
  return output;
};


Grid.prototype.forEach = function(f, context) {
  for (var y = 0; y < this.height; y++) {
    for (var x = 0; x < this.width; x++) {
      var value = this.space[x + y * this.width];
      if (value != null)
        f.call(context, value, new Vector(x, y));
    }
  }
};

World.prototype.turn = function() {
  this.year++;
  var acted = [];
  this.grid.forEach(function(critter, vector) {
    if (critter.act && acted.indexOf(critter) == -1) {
      acted.push(critter);
      this.letAct(critter, vector);
    }
  }, this);
};

World.prototype.letAct = function(critter, vector) {
  var action = critter.act(new View(this, vector));
  if (action && action.type == "move") {
    var dest = this.checkDestination(action, vector);
    if (dest && this.grid.get(dest) == null) {
      this.grid.set(vector, null);
      this.grid.set(dest, critter);
    }
  }
};

World.prototype.checkDestination = function(action, vector) {
  if (directions.hasOwnProperty(action.direction)) {
    var dest = vector.plus(directions[action.direction]);
    if (this.grid.isInside(dest))
      return dest;
  }
};

function View(world, vector) {
  this.world = world;
  this.vector = vector;
}
View.prototype.look = function(dir) {
  var target = this.vector.plus(directions[dir]);
  if (this.world.grid.isInside(target))
    return charFromElement(this.world.grid.get(target));
  else
    return "#";
};
View.prototype.findAll = function(ch) {
  var found = [];
  for (var dir in directions)
    if (this.look(dir) == ch)
      found.push(dir);
  return found;
};
View.prototype.find = function(ch) {
  var found = this.findAll(ch);
  if (found.length == 0) return null;
  return randomElement(found);
};

View.prototype.scout = function(dir, distance) {
  var target = this.vector.plus(directions[dir].times(distance));
  if (this.world.grid.isInside(target))
    return charFromElement(this.world.grid.get(target));
  else
    return "#";
};

View.prototype.migrate = function(ch) {
  var found = [];
  var path = [];
  for (var i = 0; i < 10; i++) {
	    for (var dir in directions)
			if (this.scout(dir, i) == ch)
				found.push(dir);
		if (found.length > 0)
			break;
  }
  for (var j = 0; j < found.length; j++)
	  if (this.look(found[j]) == " ")
		  path.push(found[j]);
  return randomElement(path);
};

function LifelikeWorld(map, legend) {
  World.call(this, map, legend);
  
}
LifelikeWorld.prototype = Object.create(World.prototype);

var actionTypes = Object.create(null);

LifelikeWorld.prototype.letAct = function(critter, vector) {
  var action = critter.act(new View(this, vector));
  var handled = action &&
    action.type in actionTypes &&
    actionTypes[action.type].call(this, critter,
                                  vector, action);
  if (!handled) {
    critter.energy -= 0.2;
    if (critter.energy <= 0)
      this.grid.set(vector, null);
  }
};

// ACTION TYPES
actionTypes.grow = function(critter) {
  critter.energy += 0.5;
  return true;
};

actionTypes.move = function(critter, vector, action) {
  var dest = this.checkDestination(action, vector);
  if (dest == null ||
      critter.energy <= 1 ||
      this.grid.get(dest) != null)
    return false;
  critter.energy -= 1;
  this.grid.set(vector, null);
  this.grid.set(dest, critter);
  return true;
};

actionTypes.eat = function(critter, vector, action) {
  var dest = this.checkDestination(action, vector);
  var atDest = dest != null && this.grid.get(dest);
  if (!atDest || atDest.energy == null)
    return false;
  critter.energy += atDest.energy;
  this.grid.set(dest, null);
  return true;
};

actionTypes.reproduce = function(critter, vector, action) {
  var baby = elementFromChar(this.legend,
                             critter.originChar);
  var dest = this.checkDestination(action, vector);
  if (dest == null ||
      critter.energy <= 2 * baby.energy ||
      this.grid.get(dest) != null)
    return false;
  critter.energy -= 2 * baby.energy;
  this.grid.set(dest, baby);
  return true;
};

actionTypes.germinate = function(critter, vector, action) {
  var seed = elementFromChar(this.legend, "*");
  seed.energy = 5
  var dest = this.checkDestination(action, vector);
  if (dest == null ||
      critter.energy <= 2 * seed.energy ||
      this.grid.get(dest) != null)
    return false;
  critter.energy -= 2 * seed.energy;
  this.grid.set(dest, seed);
  return true;
};

// CRITTER TYPES
function Rock() {
	this.energy = 1;
}

Rock.prototype.act = function(view) {
	if (this.energy > 10 && Math.random() > .8) {
		var space = view.find(" ");
		if (space)
			return {type: "germinate", direction: space};
	}
	this.energy += 2 * Math.random();
}

function Plant() {
  this.energy = 5 + Math.random() * 4;
}
Plant.prototype.act = function(view) {
  if (this.energy > 5) {
    var space = view.find(" ");
    if (space)
      return {type: "reproduce", direction: space};
  }
  if (this.energy < 20)
    return {type: "grow"};
};

function Bison() {
  this.energy = 20;
}
Bison.prototype.act = function(view) {
  var space = view.find(" ");
  if (this.energy > 60 && space)
    return {type: "reproduce", direction: space};
  var plant = view.find("*");
  if (plant)
    return {type: "eat", direction: plant};
  var foodSource = view.migrate("*");
  if (foodSource)
	return {type: "move", direction: foodSource};
  if (space)
    return {type: "move", direction: space};
};

//new CRITTERS
function Beast(size, hunger) {
  if (size == undefined)
	  size = 50;
  if (hunger == undefined)
	  hunger = .5;
  this.energy = size;
  this.originChar = "@";
  this.hunger = hunger; // between 0 and 1
}
Beast.prototype.act = function(view) {
  var space = view.find(" ");
  //reproduce won't work if Beast isn't in the legend
  /*if (this.energy > 120 && space)
    return {type: "reproduce", direction: space}; */
  var grub = view.find("O");
  if (!grub)
	  grub = view.find("x");
  if (!grub)
	  grub = view.find("$");
  if (grub)
    return {type: "eat", direction: grub};
  if (space) {
	this.energy = this.energy - 4*this.hunger;
    return {type: "move", direction: space};
  }
};

function Rabbit() {
  this.energy = 15;
}
Rabbit.prototype.act = function(view) {
  var space = view.find(" ");
  var mate = view.find("x");
  // this is pretty crazy reproduction.  switch the 15 and 20 to slow it down.
  if (this.energy > 15 && mate && space) {
	this.energy += 20
    return {type: "reproduce", direction: space};
  }
  //immaculate bunny generation.  haven't tried yet.
  if (this.energy > 15 && Math.random() < .1 && space) {
	this.energy += 20
    return {type: "reproduce", direction: space};
  }
  var loveInterest = view.migrate("x");
  if (loveInterest && this.energy > 15)
	return {type: "move", direction: loveInterest};
  var plant = view.find("*");
  if (plant) {
	this.energy += 2.1; //nibble
	if (Math.random() < .001)
		return {type: "eat", direction: plant};
  }
  var foodSource = view.migrate("*");
  if (foodSource)
	return {type: "move", direction: foodSource};
  if (space)
    return {type: "move", direction: space};
};

function DireWolf() {
  this.energy = 60;
}
DireWolf.prototype.act = function(view) {
  var space = view.find(" ");
  if (this.energy > 120 && space)
    return {type: "reproduce", direction: space};
  var Bison = view.find("O");
  if (Bison) {
	//this.energy += 30;
    return {type: "eat", direction: Bison};
  }
  var Rabbit = view.find("x");
  if (Rabbit) {
	// this.energy += 5
	this.energy -=5; //wasting energy chasing rabbits
    return {type: "eat", direction: Rabbit};
  }
  var prey = view.migrate("O");
  //if (!prey) 
	// var prey = view.migrate("x");
  if (prey) {
	this.energy -=5;
	return {type: "move", direction: prey};
  }
  if (space) {
	this.energy -=1.5;
    return {type: "move", direction: space};
  }
};


//GOD OBJECT
var God = {
	speak: function(wordOfGod) {console.log("This is God. " + wordOfGod);},
	time: function(world, years) {
			//console.log("year " + world.year);
			for (var turn = 0; turn < years; turn++) {
				world.turn();
				console.log(world.toString());
			}
			console.log("year " + world.year);
			this.lifeSum(world);
		},
	lifeSum: function(world) {
			for (var ch in world.legend) {
				var count = 0;
				var Energy = [];
				world.grid.forEach(function(critter, vector) {
					if (critter.originChar == ch) {
						count++;
						Energy.push(critter.energy);
					}
				}, world);
				if (Energy.length > 0) {
					var avgEnergy = Math.floor(Energy.reduce(function(a,b) {return a+b;}) / Energy.length);
					console.log(count + " " + ch + "'s with avg energy " + avgEnergy);
				}
				else
					console.log("no " + ch + " left");
			}
		},
	bounty: function(world, ch, num) {
			if (num == undefined)
				num = 10
			for (var i = 0; i < num; i++) {
				var newLife = elementFromChar(world.legend, ch);
				var dest = new Vector(
						Math.floor(Math.random() * world.grid.width),
						Math.floor(Math.random() * world.grid.height));
				if (world.grid.get(dest) == null)
					world.grid.set(dest, newLife);
			}
		}, 
	plague: function(world, strength) {
		for (var y = 0; y < world.grid.height; y++) {
			for (var x = 0; x < world.grid.width; x++) {
				if (world.grid.get(new Vector(x, y)) != null) {
					if (world.grid.get(new Vector(x, y)).energy < 50 &&
						world.grid.get(new Vector(x, y)).originChar != "*" &&
						Math.random() < strength)
							world.grid.set(new Vector(x, y), null);
					//console.log("found one at " + x + ", " + y);
				}	
			}
		}
	}
}

God.yell = function(wordOfGod) {console.log("THIS IS GOD! " + wordOfGod);}

God.check = function(world, ch) {
		world.grid.forEach(function(critter, vector) {
			if (critter.energy > 0 
				&& critter.originChar == ch)
					console.log("found a " + critter.originChar +
						" with " + Math.floor(critter.energy) + " energy at " +
						vector.x + ", " + vector.y + ".");
		}, world);
}

God.checkAll = function(world) {
		world.grid.forEach(function(critter, vector) {
			if (critter.energy > 0 )
					console.log("found a " + critter.originChar +
						" with " + Math.floor(critter.energy) + " energy at " +
						vector.x + ", " + vector.y + ".");
		}, world);
}

God.sendBeast = function(world, size, hunger) {
	var den = [];
	world.grid.space.forEach(function(spot, i) {
		if (spot == null) {
			den.push(i);
		}
	});
	world.grid.space[den[0]] = new Beast(size, hunger);
	
}

God.lifeCount = function(world, ch) {
	var count = 0;
	var Energy = [];
	world.grid.forEach(function(critter, vector) {
		if (critter.originChar == ch) {
			count++;
			Energy.push(critter.energy);
		}
	}, world);
	if (Energy.length > 0) {
		var avgEnergy = Math.floor(Energy.reduce(function(a,b) {return a+b;}) / Energy.length);
		console.log(count + " " + ch + "'s with avg energy " + avgEnergy);
	}
	else
		console.log("no " + ch + " left");
}


//CREATE THE WORLD
var bigValley = new LifelikeWorld(
  ["######################################",
   "#####                           ######",
   "##   ***                          **##",
   "#  $*##**  O                **  O  *##",
   "#    ***               O    ##**    *#",
   "#       O                   ##***    #",
   "#                           ##**     #",
   "#                 $                  #",
   "#       ***                          #",
   "#      ****               #**        #",
   "#     ***   #             #*         #",
   "#           #           **#*         #",
   "#           $***       **##          #",
   "#                      **#           #",
   "#        ***          O       $      #",
   "#                           **       #",
   "#   O       #*        ***            #",
   "#* x        #**          ***    x  x #",
   "#***   x    ##**    O         x   ***#",
   "##****  x  ###***    x          x**###",
   "######################################"],
  {"#": Rock,
   "O": Bison,
   "*": Plant,
   "$": DireWolf,
   "x": Rabbit}
);


bigValley.turn(); bigValley.toString();

//God.time(bigValley, 5);

//bigValley.grid.set(new Vector(19,12), {originChar: "!"});
//var here = new View(bigValley, new Vector(19,12));