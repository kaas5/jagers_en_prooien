# Boids Simulator

This is a simple Python implementation of a Predator Prey simulation using the Boids algorithm. Boids are artificial life-forms that exhibit collective behavior by following a set of rules related to separation, alignment, and cohesion. In this simulation, the boids represent prey animals, and there is an option to include a predator, which follows the boids based on these rules.

## Getting Started

Make sure you have Python and Pygame installed on your system. You can install Pygame using pip:

```console
pip install pygame
```

You'll also need the NumPy library for mathematical operations:

```console
pip install numpy
```

## Running the Simulation

Run the simulation by executing the provided code. This will open a Pygame window that shows a population of boids moving on the screen. You can adjust various parameters using the sliders on the right side of the screen.

- Separation: Controls how much boids avoid each other.
- Alignment: Controls how much boids align their velocity with nearby boids.
- Cohesion: Controls how much boids move towards the center of nearby boids.
- Turning: Controls how much boids turn when reaching screen edges.
- Visual Range: Sets the maximum distance at which boids consider other boids in their calculations.
You can modify these parameters and observe how they affect the behavior of the boids in the simulation.

![Simulator](https://github.com/edouardrolland/Boids_Simulator/blob/main/boids.png)

## Key Components

- Boid class: Represents an individual boid, with attributes like position, velocity, and speed limits. It has methods for avoiding edges, calculating distances between boids, implementing separation, alignment, cohesion, and more.

- Sliders and Textboxes: These are part of the user interface to adjust the parameters of the simulation interactively.

- Pygame: Used for creating the simulation window, drawing boids, and updating the display.

## Simulation Rules
The boids follow three main rules:

- Separation: Boids avoid getting too close to each other.
- Alignment: Boids align their velocity with nearby boids.
- Cohesion: Boids move towards the center of nearby boids.

By adjusting the parameters using the sliders, you can control how strongly these rules influence the boids' behavior.

## Customization

Feel free to customize the code and experiment with different parameters and behaviors. You can also add new features or modify existing ones to create your own variations of the simulation.

Enjoy the Predator Prey Simulation with Boids! 🐦🔴🎮
