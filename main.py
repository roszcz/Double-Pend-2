import manim as M
import pandas as pd

from pendulum.scenes import main as pendulum_scenes


def scene_from_trajectory(df):
    # Pixels
    resolution = 500, 500
    M.config['video_dir'] = 'media/'
    M.config['images_dir'] = 'media/'
    # M.config['save_last_frame'] = True

    dt = 0.01
    l1 = 1.5
    l2 = 0.5

    # NumberPlane units (2 * "radius")
    M.config['frame_width'] = 2 * (l1+l2) * 1.1
    M.config['frame_height'] = 2 * (l1+l2) * 1.1

    output_name = 'cycle-search-0x08-small'
    M.config['output_file'] = output_name
    M.config['format'] = 'gif'
    # M.config['format'] = None

    # Make each movie in different resultion
    M.config['pixel_width'] = resolution[0]
    M.config['pixel_height'] = resolution[1]
    scene = pendulum_scenes.DoublePendulum(l1=l1, l2=l2, df=df, dt=dt)
    scene.render()
    print('Finished rendering for:', l2)
    print('==' * 40)


if __name__ == '__main__':
    df = pd.read_csv('cycle-0x08.csv')
    scene_from_trajectory(df)
