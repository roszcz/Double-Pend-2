import manim as M
import pandas as pd
# import numpy as np


class DoublePendulum(M.Scene):
    def __init__(self, l1, l2, df, dt):
        # Masses of the ball
        self.m1 = 2
        self.m2 = 5
        # Length of the rigid massless rods
        self.l1 = l1
        self.l2 = l2
        self.traj_color = '#2E8B57'

        # timestep
        self.dt = dt
        # runtime represents how long each frame should run. runtime = 1/fps
        # Change frame rate from here
        M.config.frame_rate = 30
        # do not change this
        self.runtime = 1 / M.config.frame_rate
        # time_max represents for how long (in seconds) the overall animation should run
        self.time_max = 5
        # Initial angles of the masses
        # number of seconds before current time to show trail
        self.trail_seconds = 0.5

        self.trajectory = df
        super().__init__()

    def getline(self, Point1, Point2):
        """[Generates a line between the center of the given Circles which represent the masses]

        Args:
            Point1 ([Circle]): [Circle represent the first mass]
            Point2 ([Circle]): [Circle represent the second mass]

        Returns:
            [Line]: [Returns a line between the center of two masses]
        """
        start_point = Point1.get_center()
        end_point = Point2.get_center()
        line = M.Line(start_point, end_point).set_stroke(width=2)
        return line
        
    def get_initial_traj(self):
        start_idx = self.trajectory.shape[0] - int(self.trail_seconds / self.dt)
        end_idx = self.trajectory.shape[0]
        step = int(self.runtime / self.dt)
        traj_points = [
                    self.trajectory.iloc[num].x2 * M.RIGHT + self.trajectory.iloc[num].y2 * M.UP
                    for num in range(start_idx, end_idx, step)
                ]
        traj_points.append(self.Circle2.get_center())
        return M.VGroup().set_points_smoothly(traj_points).set_stroke(color=self.traj_color, width=1)

    def construct(self):
        # Error checking of the times used
        if self.trail_seconds >= self.time_max:
            raise Exception(
                "Seconds of trail must be smaller than time of animation"
            )
        elif self.trail_seconds < self.runtime:
            raise Exception(
                "Seconds of trail must be greater than runtime of each frame"
            )

        # Adding the axes
        axes = M.NumberPlane(
            x_range=(-4, 4, 1),
            y_range=(-4, 4, 1)
        )
        axes = axes.set_opacity(0.05)
        self.add(axes)

        # Pendulum Motion
        Center = M.Dot()
        first = self.trajectory.iloc[0]
        x1_initial, y1_initial = first.x1, first.y1
        x2_initial, y2_initial = first.x2, first.y2

        # Circles representing the masses
        c1_color = '#40E0D0'
        self.Circle1 = (
            M.Dot(radius=0.04 * self.m1, z_index=10)
            .move_to(x1_initial * M.RIGHT + y1_initial * M.UP)
            .set_color(c1_color)
        )
        c2_color = '#008080'
        self.Circle2 = (
            M.Dot(radius=0.04 * self.m2, z_index=10)
            .move_to(x2_initial * M.RIGHT + y2_initial * M.UP)
            .set_color(c2_color)
        )

        # Initializing the lines and adding update functions
        Line1 = self.getline(Center, self.Circle1)
        Line1.add_updater(
            lambda mob: mob.become(self.getline(Center, self.Circle1))
        )
        Line2 = self.getline(self.Circle1, self.Circle2)
        Line2.add_updater(
            lambda mob: mob.become(self.getline(self.Circle1, self.Circle2))
        )

        # Adding the lines, masses and center dot to the screen
        self.add(Line1, Line2, Center, self.Circle1, self.Circle2)
        traj = self.get_initial_traj()

        # Adding the index referenced by for loop here so it can be used by
        # the trajectory update function
        it = 0

        # Update function for the trajectory
        def traj_update(mob):
            step = int(self.runtime / self.dt)
            start_idx = max(it - int(self.trail_seconds / self.dt), 0)
            end_idx = it - step
            if end_idx > start_idx:
                # Adding the points history of trajectory
                traj_points = [
                    self.trajectory.iloc[num].x2 * M.RIGHT + self.trajectory.iloc[num].y2 * M.UP
                    for num in range(start_idx, end_idx, step)
                ]
                traj_points.append(self.Circle2.get_center())

                # Creating VGroup for the trajectory
                updated_traj = M.VGroup().set_points_smoothly(traj_points)
                updated_traj.set_stroke(color=self.traj_color, width=1)
                mob.become(updated_traj)

        traj.add_updater(traj_update)
        self.add(traj)

        # Animating the masses moving
        for it in range(0, self.trajectory.shape[0], int(self.runtime / self.dt)):
            row = self.trajectory.iloc[it]
            self.play(
                self.Circle1.animate.move_to(row.x1 * M.RIGHT + row.y1 * M.UP),
                self.Circle2.animate.move_to(row.x2 * M.RIGHT + row.y2 * M.UP),
                run_time=self.runtime,
                rate_func=M.linear,
            )
