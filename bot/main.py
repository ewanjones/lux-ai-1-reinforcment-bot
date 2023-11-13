from agent import _agent, Agent


class Observation:
    def __init__(self, inputs) -> None:
        self.player = int(inputs[0])
        self.updates = inputs
        self.step = 0


def read_inputs():
    """
    Reads input from stdin until D_DONE is received
    """
    inputs = []

    while True:
        try:
            message = input()
        except EOFError as eof:
            raise SystemExit(eof)

        if message == "D_DONE":
            return inputs

        inputs.append(message)


if __name__ == "__main__":

    step = 0
    agent = None

    while True:
        # Get new game state from stdin
        inputs = read_inputs()

        if step == 0:
            # Get initial inputs and initialise observation
            observation = Observation(inputs=inputs)
            agent = Agent(observation=observation)
        else:
            if not agent:
                raise ValueError("Cannot ")

            observation.updates = inputs
            agent.update(observation=observation)

        # TODO: Remove this when agent working
        actions = _agent(observation, None)

        step += 1
        observation.step = step

        print(",".join(actions))
        print("D_FINISH")
