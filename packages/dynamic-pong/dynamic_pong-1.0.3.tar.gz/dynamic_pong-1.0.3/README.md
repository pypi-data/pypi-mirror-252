# Dynamic Pong

Dynamic Pong is a modern rendition of the classic arcade game Pong, crafted with Python using the Pygame library. It offers an engaging and interactive gaming experience, featuring responsive paddle controls and dynamic game speed adjustments. This project is an excellent showcase of Python programming skills, game design, and software development principles.

## Features

- **Adaptive Gameplay**: The game's difficulty increases as you progress, offering a challenging and engaging experience.
- **Collision Detection**: Implements collision logic for paddles and game boundaries.
- **Score Tracking**: Real-time score display for both the player and the computer-controlled opponent.
- **Customizability**: Adjustable game window size and element proportions to fit various screens.

## Installation

To play Dynamic Pong, you need to have Python and Pygame installed on your system.

1. **Install Python**: Download and install Python from [python.org](https://www.python.org/downloads/).
2. **Install Pygame**: Run `pip install pygame` in your command line.
3. **Download the Game**: Clone or download this repository to your local machine.

## How to Play

1. Navigate to the directory containing the game files.
2. Run the script `python dynamic_pong.py`.
3. Control the left paddle using the `Up` and `Down` arrow keys or the `W` and `S` keys.
4. The game continues indefinitely until manually exited.

## Code Examples

```python
# Creating a block representing a paddle
block = Block("white", 20, 100, 50, 300)
```

```python
# Initializing a player paddle
player = Player("white", 20, 140, 5)
```

```python
# Handling a ball collision with the top edge of the screen
ball = Ball("white", 30, 30, paddle_group)
ball.rect.top = -5
ball.speed_y = -5
ball.collisions()
```

## Contributing

Contributions to Dynamic Pong are welcome! If you have suggestions for improvements or encounter any issues, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## About the Author

Adamya Singh - Aspiring software developer with a passion for game development and Python programming. Feel free to connect with me on [LinkedIn](https://www.linkedin.com/in/adamya-singh-0a8746184/).