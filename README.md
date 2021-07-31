# **Double Pendulum**

This repo contains the code for creating an animation of a Double Pendulum using Manim Community Edition

## **Usage**


_This guide assumes you have a resonably new version of **python3** and **pip** installed._

To get started, we have to first install the necessary dependencies.

But before that we have to create and activate a virtual environment. See [_this_](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/) for more information.

Once the virtualenv has been created, we can now proceed to install everything.

The _requirements.txt_ contains all the dependencies. So install it using the following commands in the terminal:

1. > `cd path/to/folder/`

2. > `pip install -r requirements.txt`

Now check if manim is installed:

-   > `manim --version`

If the command throws no errors then manim has been installed successfully.

Now to compile the code use these commands:

-   > `manim -pqh doublePend.py DoublePendulum`

Here `-pqh` tells manim to render it in high quality (`-ql` flag) and to preview (`-p` flag) it after compilation.

Click [_here_](https://docs.manim.community/en/stable/tutorials/configuration.html#command-line-arguments) to see what CLI flags can be used to change render quality.

## **Configuring the initial conditions of pendulum**

---

The following quantities can be configured in the `__init__` function of the `DoublePendulum` class:

-   masses of the balls,
-   lengths of the rigid massless rods
-   acceleration due to gravity
-   initial angles
-   factor that determines energy dissipation
-   frame rate of the video
-   how long the animation should run
-   seconds history of the trail
