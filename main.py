from event_handler import EventHandler
from simulation import Simulation


def initialize():
    return Simulation(), EventHandler()


def run(simulation, event_handler):
    while simulation.running:
        event_handler.handle_events(simulation)
        simulation.clock.tick(simulation.frame_rate)
        simulation.draw()
        simulation.update()


if __name__ == '__main__':
    sim, _event_handler = initialize()
    sim.start()
    run(sim, _event_handler)
