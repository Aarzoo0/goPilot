let plane;
let obstacles;
let luckPoints;
let luckPointSpeed = 200;
let score = 0;
let planeSpeed = 300;
let obstacleSpeed = 200;
let isMessageDisplaying = false;
let messageText;
let messageStartTime;
let messageDuration = 2000; // 2 seconds message display duration
let gameStarted = false;  // Track if the game has started

let instructionText;  // Store reference to the instruction text

function preload() {
    // Load images and scale them down
    this.load.image('plane', 'assets/plane.png');
    this.load.image('bird', 'assets/bird.png');
    this.load.image('star', 'assets/star.png');
}

function create() {
    // Background gradient
    this.cameras.main.setBackgroundColor(0x87ceeb);  // Light sky-blue color

    // Plane setup
    plane = this.physics.add.image(100, 300, 'plane').setOrigin(0.5).setCollideWorldBounds(true);
    plane.setScale(0.1); // Scale down plane image to 10% of original size

    // Create groups for obstacles and luck points
    obstacles = this.physics.add.group();
    luckPoints = this.physics.add.group();

    // Display welcome message with custom font
    messageText = this.add.text(400, 200, "Welcome to GoPilot Md.Adill Ibrahim!", { 
        fontSize: '32px', 
        fill: '#081375', 
        fontFamily: 'Comic Neue', 
        fontStyle: 'bold' 
    }).setOrigin(0.5);

    // Instructions with smaller text
    instructionText = this.add.text(400, 300, "Click here to start", { 
        fontSize: '20px', 
        fill: '#595A5B', 
        fontFamily: 'Comic Neue',
    }).setOrigin(0.5);

    // Make the welcome message and instructions interactive
    messageText.setInteractive();
    instructionText.setInteractive();

    // Add event listeners for clicking or pressing Enter
    messageText.on('pointerdown', startGame);
    instructionText.on('pointerdown', startGame);

    // Add keyboard controls for plane movement
    this.input.keyboard.on('keydown-UP', () => {
        if (gameStarted) plane.setVelocityY(-planeSpeed);
    });

    this.input.keyboard.on('keydown-DOWN', () => {
        if (gameStarted) plane.setVelocityY(planeSpeed);
    });
}

function update() {
    // Check for message duration and hide it after time is up
    if (isMessageDisplaying) {
        if (Phaser.Math.Distance.Between(messageStartTime, this.time.now) > messageDuration) {
            isMessageDisplaying = false; 
            messageText.setVisible(false);  // Hide message after duration
        }
    }

    // Randomly create obstacles and luck points
    if (Phaser.Math.Between(1, 100) < 2 && gameStarted) {
        createObstacle(this);
    }

    if (Phaser.Math.Between(1, 100) < 2 && gameStarted) {
        createLuckPoint(this);
    }

    // Check for collisions between plane and obstacles (physical collision, not just overlap)
    if (gameStarted) {
        this.physics.collide(plane, obstacles, gameOver, null, this);  // Use collide instead of overlap
        this.physics.overlap(plane, luckPoints, collectLuckPoint, null, this);  // Overlap for collecting luck points
    }

    // Move obstacles and luck points
    obstacles.children.iterate(obstacle => {
        obstacle.setVelocityX(-obstacleSpeed);
        if (obstacle.x < -obstacle.width) {
            obstacle.destroy();  // Remove obstacle if it goes off-screen
        }
    });

    luckPoints.children.iterate(luckPoint => {
        luckPoint.setVelocityX(-luckPointSpeed);
        if (luckPoint.x < -luckPoint.width) {
            luckPoint.destroy();  // Remove luck point if it goes off-screen
        }
    });
}

// Create an obstacle
function createObstacle(scene) {
    let obstacle = scene.physics.add.image(800, Phaser.Math.Between(100, 500), 'bird');
    obstacle.setScale(0.1); // Scale down the bird image to 10% of original size
    obstacle.setVelocityX(-obstacleSpeed);
    obstacles.add(obstacle);
}

// Create a luck point (star)
function createLuckPoint(scene) {
    let luckPoint = scene.physics.add.image(800, Phaser.Math.Between(100, 500), 'star');
    luckPoint.setScale(0.1); // Scale down the star image to 10% of original size
    luckPoint.setVelocityX(-luckPointSpeed);
    luckPoints.add(luckPoint);
}

// Handle game over logic
function gameOver() {
    // Stop the game and show Game Over message
    messageText = this.add.text(400, 200, 'Game Over!But Not the examssss', { 
        fontSize: '32px', 
        fill: '#FF0000', 
        fontFamily: 'Comic Neue', 
        fontStyle: 'bold'
    }).setOrigin(0.5);
    isMessageDisplaying = true;
    messageStartTime = this.time.now;

    // Display "All the best" message after a brief delay
    this.time.delayedCall(1500, () => {
        messageText = this.add.text(400, 300, 'All the best Diluu! Jao phod denaa💪', { 
            fontSize: '32px', 
            fill: '#181C43', 
            fontFamily: 'Comic Neue', 
            fontStyle: 'bold'
        }).setOrigin(0.5);
    });

    gameStarted = false; // Stop the game from updating further
}

// Handle luck point collection
function collectLuckPoint(plane, luckPoint) {
    luckPoint.destroy(); // Remove collected luck point
    score += 1; // Increase score

    // Display "Keep flying high!" message in a different location to avoid collision
    messageText = this.add.text(400, 100, "Keep flying high!", { 
        fontSize: '32px', 
        fill: '#FFFF00', 
        fontFamily: 'Comic Neue', 
        fontStyle: 'bold'
    }).setOrigin(0.5);
    
    messageStartTime = this.time.now;
    isMessageDisplaying = true;  // Show the message for a limited time

    // Hide the message after 1 second
    this.time.delayedCall(1000, () => {
        messageText.setVisible(false);  // Hide the message after 1 second
    });
}

// Start the game when the welcome message is clicked
function startGame() {
    // Hide the welcome and start messages when the game starts
    messageText.setVisible(false);
    instructionText.setVisible(false); // Hide the instruction text as well

    // Reset the score
    score = 0;

    // Clear any existing obstacles or luck points
    obstacles.clear(true, true);
    luckPoints.clear(true, true);

    // Mark the game as started
    gameStarted = true;

    // Restart the scene to ensure everything is set up properly
    this.scene.restart();
}

// Create the Phaser game configuration
const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 0 },
            debug: false
        }
    },
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};

// Start the Phaser game
const game = new Phaser.Game(config);
