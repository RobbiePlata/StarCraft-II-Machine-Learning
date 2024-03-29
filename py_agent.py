from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions, features, units
from absl import app
import random

class PyAgent(base_agent.BaseAgent):
    
    def step(self, obs):
        super(PyAgent, self).step(obs)

        if buildPylon(self, obs):
            x = random.randint(0, 83)
            y = random.randint(0, 83)
            return actions.FUNCTIONS.Build_Pylon_screen('now', (x, y))

        if buildGateway(self, obs):
            x = random.randint(0, 83)
            y = random.randint(0, 83)
            return actions.FUNCTIONS.Build_Gateway_screen('now', (x, y))
        
        workers = [unit for unit in obs.observation['feature_units']
            if unit.unit_type == units.Protoss.Probe
        ]
        if len(workers) > 0:
            worker = random.choice(workers)
            return actions.FUNCTIONS.select_point("select_all_type", (worker.x, worker.y))


        return actions.FUNCTIONS.no_op()

    def get_units_by_type(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units 
            if unit.unit_type == unit_type]

    def unit_type_is_selected(self, obs, unit_type):
        if (len(obs.observation.single_select) > 0 and obs.observation.single_select[0].unit_type == unit_type):
            return True

        if (len(obs.observation.multi_select) > 0 and obs.observation.multi_select[0].unit_type == unit_type):
            return True
        return False

def buildPylon(self, obs):
    pylons = self.get_units_by_type(obs, units.Protoss.Pylon)
    if len(pylons) == 0:
        if self.unit_type_is_selected(obs, units.Protoss.Probe):
            if(actions.FUNCTIONS.Build_Pylon_screen.id in obs.observation.available_actions):
                return True
            return False

def buildGateway(self, obs):
    gateway = self.get_units_by_type(obs, units.Protoss.Gateway)
    if len(gateway) == 0:
        if self.unit_type_is_selected(obs, units.Protoss.Probe):
            if(actions.FUNCTIONS.Build_Gateway_screen.id in obs.observation.available_actions):
                return True
            return False

def main(unused_argv):
    agent = PyAgent()
    try:
        while True:
            with sc2_env.SC2Env(
                map_name="Simple64",
                players=[sc2_env.Agent(sc2_env.Race.protoss), 
                        sc2_env.Bot(sc2_env.Race.protoss, 
                        sc2_env.Difficulty.very_easy)],
                agent_interface_format=features.AgentInterfaceFormat(feature_dimensions=features.Dimensions(screen=84, minimap=64), use_feature_units=True),
                step_mul=8,
                game_steps_per_episode=0,
                visualize=True) as env:
                agent.setup(env.observation_spec(), env.action_spec())
                timesteps = env.reset()
                agent.reset()
                
                while True:
                    step_actions = [agent.step(timesteps[0])]
                    if timesteps[0].last():
                        break
                    timesteps = env.step(step_actions)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    app.run(main)