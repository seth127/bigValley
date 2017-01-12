
//make it go
for (var turn = 0; turn < 5; turn++) {
	world.turn();
	console.log(world.toString());
}

//sow the seeds
LifelikeWorld.prototype.sowTheSeeds = function(num) {
	for (var i = 0; i < num; i++) {
		var newPlant = elementFromChar(this.legend, "*");
		var dest = new Vector(
				Math.floor(Math.random() * this.grid.width),
				Math.floor(Math.random() * this.grid.height));
		if (this.grid.get(dest) == null)
			this.grid.set(dest, newPlant);
	}
}
//Math.floor(Math.random() * valley.grid.width)

//God object
var God = {
	speak: function(wordOfGod) {console.log("This is God. " + wordOfGod);},
	bounty: function(world, num) {
			for (var i = 0; i < num; i++) {
				var newPlant = elementFromChar(world.legend, "*");
				var dest = new Vector(
						Math.floor(Math.random() * world.grid.width),
						Math.floor(Math.random() * world.grid.height));
				if (world.grid.get(dest) == null)
					world.grid.set(dest, newPlant);
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

God.checkAnimals = function(world) {
		world.grid.forEach(function(critter, vector) {
			if (critter.energy > 0 && critter.originChar != "*")
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

God.wolfCount = function(world) {
	var count = 0;
	var Energy = [];
	world.grid.forEach(function(critter, vector) {
		if (critter.originChar == "$") {
			count++;
			Energy.push(critter.energy);
		}
	}, world);
	var avgEnergy = Math.floor(Energy.reduce(function(a,b) {return a+b;}) / Energy.length);
	console.log(count + " wolves with avg energy " + avgEnergy);
}

God.rabbitCount = function(world) {
	var count = 0;
	var Energy = [];
	world.grid.forEach(function(critter, vector) {
		if (critter.originChar == "x") {
			count++;
			Energy.push(critter.energy);
		}
	}, world);
	var avgEnergy = Math.floor(Energy.reduce(function(a,b) {return a+b;}) / Energy.length);
	console.log(count + " rabbits with avg energy " + avgEnergy);
}

God.cowCount = function(world) {
	var count = 0;
	var Energy = [];
	world.grid.forEach(function(critter, vector) {
		if (critter.originChar == "O") {
			count++;
			Energy.push(critter.energy);
		}
	}, world);
	var avgEnergy = Math.floor(Energy.reduce(function(a,b) {return a+b;}) / Energy.length);
	console.log(count + " cows with avg energy " + avgEnergy);
}

God.plantCount = function(world) {
	var count = 0;
	var Energy = [];
	world.grid.forEach(function(critter, vector) {
		if (critter.originChar == "*") {
			count++;
			Energy.push(critter.energy);
		}
	}, world);
	var avgEnergy = Math.floor(Energy.reduce(function(a,b) {return a+b;}) / Energy.length);
	console.log(count + " plants with avg energy " + avgEnergy);
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

//this was for something
//Object.getPrototypeOf(valley.grid.get(new Vector(23,10))) == Plant.prototype

//new animals
function Beast(size, hunger) {
  this.energy = size;
  this.originChar = "@";
  this.hunger = hunger;
}
Beast.prototype.act = function(view) {
  var space = view.find(" ");
  //reproduce won't work if Beast isn't in the legend
  /*if (this.energy > 120 && space)
    return {type: "reproduce", direction: space}; */
  var grub = view.find("O");
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
  var plant = view.find("*");
  if (plant) {
	this.energy += 3; //nibble
	if (Math.random() < .05)
		return {type: "eat", direction: plant};
  }
  if (space)
    return {type: "move", direction: space};
};

function DireWolf() {
  this.energy = 50;
}
DireWolf.prototype.act = function(view) {
  var space = view.find(" ");
  if (this.energy > 120 && space)
    return {type: "reproduce", direction: space};
  var cow = view.find("O");
  if (cow) {
	this.energy += 30
    return {type: "eat", direction: cow};
  }
  var bunny = view.find("x");
  if (bunny) {
	// this.energy += 5
	// this.energy -=5 //wasting energy chasing rabbits
    return {type: "eat", direction: bunny};
  }
  if (space)
    return {type: "move", direction: space};
};

var bigValley = new LifelikeWorld(
  ["######################################",
   "#####                           ######",
   "##   ***                          **##",
   "#   *##**                   **  O  *##",
   "#    ***               O    ##**    *#",
   "#       O                   ##***    #",
   "#                           ##**     #",
   "#                 $                  #",
   "#       ***                          #",
   "#      ****               #**        #",
   "#     ***                 #*         #",
   "#                       **#*         #",
   "#            ***       **##          #",
   "#                      **#           #",
   "#        ***          O       $      #",
   "#                           **       #",
   "#   O       #*        ***            #",
   "#*          #**          ***    x  x #",
   "#***        ##**    O         x   ***#",
   "##****     ###***    x          x**###",
   "######################################"],
  {"#": Wall,
   "O": PlantEater,
   "*": Plant,
   "$": DireWolf,
   "x": Rabbit}
);

bigValley.turn(); bigValley.toString();

God.wolfCount(bigValley);
God.rabbitCount(bigValley);
God.cowCount(bigValley);
God.plantCount(bigValley);

// FROM THE WEBSITE, THE COMPLETE CODE
var plan = ["############################",
            "#      #    #      o      ##",
            "#                          #",
            "#          #####           #",
            "##         #   #    ##     #",
            "###           ##     #     #",
            "#           ###      #     #",
            "#   ####                   #",
            "#   ##       o             #",
            "# o  #         o       ### #",
            "#    #                     #",
            "############################"];

function Vector(x, y) {
  this.x = x;
  this.y = y;
}
Vector.prototype.plus = function(other) {
  return new Vector(this.x + other.x, this.y + other.y);
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

function BouncingCritter() {
  this.direction = randomElement(directionNames);
};

BouncingCritter.prototype.act = function(view) {
  if (view.look(this.direction) != " ")
    this.direction = view.find(" ") || "s";
  return {type: "move", direction: this.direction};
};

function elementFromChar(legend, ch) {
  if (ch == " ")
    return null;
  var element = new legend[ch]();
  element.originChar = ch;
  return element;
}

function World(map, legend) {
  var grid = new Grid(map[0].length, map.length);
  this.grid = grid;
  this.legend = legend;

  map.forEach(function(line, y) {
    for (var x = 0; x < line.length; x++)
      grid.set(new Vector(x, y),
               elementFromChar(legend, line[x]));
  });
}

function charFromElement(element) {
  if (element == null)
    return " ";
  else
    return element.originChar;
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

function Wall() {}

var world = new World(plan, {"#": Wall,
                             "o": BouncingCritter});
//   #      #    #      o      ##
//   #                          #
//   #          #####           #
//   ##         #   #    ##     #
//   ###           ##     #     #
//   #           ###      #     #
//   #   ####                   #
//   #   ##       o             #
//   # o  #         o       ### #
//   #    #                     #
//   ############################

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

function dirPlus(dir, n) {
  var index = directionNames.indexOf(dir);
  return directionNames[(index + n + 8) % 8];
}

function WallFollower() {
  this.dir = "s";
}

WallFollower.prototype.act = function(view) {
  var start = this.dir;
  if (view.look(dirPlus(this.dir, -3)) != " ")
    start = this.dir = dirPlus(this.dir, -2);
  while (view.look(this.dir) != " ") {
    this.dir = dirPlus(this.dir, 1);
    if (this.dir == start) break;
  }
  return {type: "move", direction: this.dir};
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

function Plant() {
  this.energy = 3 + Math.random() * 4;
}
Plant.prototype.act = function(view) {
  if (this.energy > 15) {
    var space = view.find(" ");
    if (space)
      return {type: "reproduce", direction: space};
  }
  if (this.energy < 20)
    return {type: "grow"};
};

function PlantEater() {
  this.energy = 20;
}
PlantEater.prototype.act = function(view) {
  var space = view.find(" ");
  if (this.energy > 60 && space)
    return {type: "reproduce", direction: space};
  var plant = view.find("*");
  if (plant)
    return {type: "eat", direction: plant};
  if (space)
    return {type: "move", direction: space};
};

var valley = new LifelikeWorld(
  ["############################",
   "#####                 ######",
   "##   ***                **##",
   "#   *##**         **  O  *##",
   "#    ***     O    ##**    *#",
   "#       O         ##***    #",
   "#                 ##**     #",
   "#   O       #*             #",
   "#*          #**       O    #",
   "#***        ##**    O    **#",
   "##****     ###***       *###",
   "############################"],
  {"#": Wall,
   "O": PlantEater,
   "*": Plant}
);
