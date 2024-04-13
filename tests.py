import unittest
import write_replay as wr

class TestBallCalculations(unittest.TestCase):
    def test_ball_angle(self):
        velocity = [-2.07524824142456,-0.605385303497314,-4.46962261199951]
        print(wr.calculate_angles(velocity=velocity))

    def test_ball_rotation(self):
        v = [-2.07524824142456,-0.605385303497314,-4.46962261199951]
        r = [3290.71875,-5926.55712890625,-4750.791015625]
        #v=(1.13098478317261,-0.759728908538818,5.86662006378174)
        #r=(-7587.90576171875,-7277.6123046875,4291.7255859375)
        print(wr.calculate_spin_rate(velocity=v, rotation=r))

    def test_ball_speed(self):
        v=(1.13098478317261,-0.759728908538818,5.86662006378174)
        print(wr.calculate_speed_value(v))

if __name__ == '__main__':
    unittest.main()