import manim as M

from pendulum import cycles as pendulum_cycles
from pendulum.scenes import main as pendulum_scenes


def scene_from_trajectory(df, state, name):
    # Pixels
    resolution = 500, 500
    M.config['video_dir'] = 'media/'
    M.config['images_dir'] = 'media/'
    # M.config['save_last_frame'] = True

    dt = 0.01
    l1 = state['L1']
    l2 = state['L2']

    # NumberPlane units (2 * "radius") + margin for the ball width
    M.config['frame_width'] = 2 * (l1+l2) * 1.1
    M.config['frame_height'] = 2 * (l1+l2) * 1.1

    M.config['output_file'] = name
    M.config['format'] = 'gif'
    # M.config['format'] = None

    # Make each movie in different resultion
    M.config['pixel_width'] = resolution[0]
    M.config['pixel_height'] = resolution[1]
    scene = pendulum_scenes.DoublePendulum(l1=l1, l2=l2, df=df, dt=dt)
    scene.render()
    print('Finished rendering for:', name)
    print('==' * 40)


if __name__ == '__main__':
    # df = pd.read_csv('cycle-0x08.csv')
    cycles = pendulum_cycles.find_cycles()
    for it, cycle in enumerate(cycles):
        df = cycle['df']
        state = cycle['state']
        best_cycle = cycle['best_cycle']

        left = int(best_cycle.tortoise)
        right = int(best_cycle.hare)

        df_cycle = df[left: right]

        name = f'cycle_{it}'
        scene_from_trajectory(df_cycle, state, name)
