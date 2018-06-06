from blink1.blink1 import Blink1
import time


class State():
    def __init__(self,
                 colour='#000000',
                 secondary_colour='#000000',
                 blink_cluster=0,
                 short_gap=200,
                 long_gap=1000):
        self.colour = colour
        self.secondary_colour = secondary_colour
        self.short_gap = short_gap
        self.long_gap = long_gap
        self.blink_cluster = blink_cluster


class StateMachine():
    def __init__(self):
        self.current_state = State()

    def transition(self, target_state, transition_time=0):
        b1 = Blink1()
        std_transition = 1000
        if target_state == self.current_state:
            b1.close()
            return
        b1.fade_to_color(std_transition, 'black')
        if target_state.blink_cluster == 0:
            b1.fade_to_color(std_transition, target_state.colour)
            b1.close()
            return
        b1.writePatternLine(target_state.long_gap,
                            target_state.secondary_colour,
                            0)
        for line in range(1, target_state.blink_cluster * 2 + 1):
            if line % 2:
                b1.writePatternLine(target_state.short_gap,
                                    target_state.colour,
                                    line)
            else:
                b1.writePatternLine(target_state.short_gap,
                                    target_state.secondary_colour,
                                    line)
        print("Here's what we've got from 0 to {}:"
              "".format(target_state.blink_cluster * 2 + 1))
        for line in range(target_state.blink_cluster * 2 + 1):
            print(b1.readPatternLine(line))
        if target_state.blink_cluster > 7:
            b1.play(1, target_state.blink_cluster * 2)
        else:
            b1.play(0, target_state.blink_cluster * 2)
        b1.close()

    def shutdown(self):
        b1 = Blink1()
        b1.off()
        b1.close()


if __name__ == '__main__':
    s1 = StateMachine()
    print("State machine initialized.")
    s1.transition(State(colour='#FF0000',
                        blink_cluster=3,
                        short_gap=400,
                        long_gap=1000))
    print("Transitioned to three blinks red.")
    time.sleep(30)
    s1.transition(State(colour='#FFFF00',
                        blink_cluster=2,
                        short_gap=500,
                        long_gap=2000))
    print("Transitioned to 2 blinks yellow")
    time.sleep(30)
    s1.transition(State(colour='#0000FF', blink_cluster=0))
    print("Transitioned to solid blue")
    time.sleep(30)
    s1.transition(State(colour='#FFFF00',
                        blink_cluster=8,
                        short_gap=500,
                        long_gap=2000,
                        secondary_colour='#FF0000'))
    print("Transitioned to alternating red and yellow")
    s1.shutdown()
