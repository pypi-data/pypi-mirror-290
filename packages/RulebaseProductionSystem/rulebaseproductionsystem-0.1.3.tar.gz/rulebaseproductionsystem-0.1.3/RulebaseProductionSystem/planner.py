import re
from random import randint

# Global User Inputs

init_state = []
general_facts = []
pos = {}
constraints_list = []
fin_state = []

# End of User Input

history = []
rejected_states = []
itr_limit = 1000


# Utility Functions

def replaceWordsFromText(regex_pattern, values_map, text):
  return regex_pattern.sub(lambda m: values_map[re.escape(m.group(0))], text)

def getRandomNumberFromRange(max, min = 0):
  if min == max: return 0
  return randint(min, max)

# End of Utility Functions


def getMovableActor(general_facts, init_state):
  """
  Check if any agent is specified from the init_state in facts that must move at every step and return all.
  Unless there is only one agent in the init_state then it returns only that one.
  
  :param general_facts: list of general facts
  :param init_state: the initial state
  :return: list of all the actors names
  """
  agents = []
  if len(init_state) == 1:
    agents.append(init_state[0].split(" ")[0])
  else:
    for fact in general_facts:
      fact_arr = fact.split(" ")
      if fact_arr[1] == "moves":
        agents.append(fact_arr[0])
  return list(set(agents))

def totalNumbersOfMovableActors(general_facts, movable_agents = []):
  """
  Check if total number of movable agents is specified in the facts, if not set to 1 by default.
  Returns length of returned list from getMovableActor() or specified count, whatevers bigger.
  
  :param general_facts: list of general facts
  :param movable_agents: returned value of getMovableActor() # optional
  :return: list of all the actors names
  """

  count = 1
  for fact in general_facts:
    fact_arr = fact.split(" ")
    if fact_arr[1] == "can_move":
      count = int(fact_arr[0])

  len_movable_agents = len(movable_agents)
  if len_movable_agents != 0:
    if count < len_movable_agents: 
      return len_movable_agents 
  return count

def updateConstraintWithValues(constraint, variables_values):
  """
  Replace constraint vairables with the values

  :param constraint: list of constraint strings from one constraint item
  :param variables_values: variables with values as key/value pairs
  :return: updated constraint strings list
  """

  pattern = re.compile("|".join(variables_values.keys()))
  return [replaceWordsFromText(pattern, variables_values, text) for text in constraint]

def isAnyConstraintFailing(constraint_objs, state):
  """
  Check if any constraint is failing from the list of constraints.

  :param constraint_objs: list of constraint from input
  :param state: state to verify against constraints
  :return: returns either False or the Failed constraint 
  """

  for constraint_obj_item in constraint_objs:
    variables_values = {
      "var_actor_1": "",
      "var_actor_2": "",
      "var_pos_1": "",
    }

    facts, constraint_list = constraint_obj_item["facts"], constraint_obj_item["constraint"]
    for fact in facts:
      source_of_truth = list(state)
      source_of_truth.append(fact)

      fact_arr = fact.split(" ")
      if "can_eat" in fact:
        variables_values["var_actor_1"] = fact_arr[0]
        variables_values["var_actor_2"] = fact_arr[2]
      
      for position in pos["values"]:
        variables_values["var_pos_1"] = position

        updated_constraints = updateConstraintWithValues(constraint_list, variables_values)
        constraint_applied = True
        for constraint in updated_constraints:
          if "NOT" in constraint:
            inversed = constraint.replace("NOT ", "")
          
            if inversed in source_of_truth:
              constraint_applied = False
          else:
            if constraint not in source_of_truth:
              constraint_applied = False
      
        if constraint_applied: return constraint_obj_item
    return False

def getRandomPositionExcept(current, pos):
  """
  Select random position except the current one.

  :param current: the current position of the agent
  :param pos: position dictionary from the input
  :return: a random position except the current one. 
  """

  positionPositions = [p for p in pos["values"] if p != current]
  return positionPositions[getRandomNumberFromRange(len(positionPositions) - 1)]

def isStateInTheList(state, list_of_states):
  """
  Check if an item is present in the list.

  :param state: item to check
  :param list_of_states: list to check the item in
  :return: returns True if item is in list otherwise False
  """
  
  if state in list_of_states:
    return True
  return False

def isGoalAchieved(state, final_state):
  """
  Check if the state is equal to the goal from input

  :param state: current state to compare with
  :param final_state: goal from the input
  :return: returns True if state is equal to goal otherwise False
  """
  if state == final_state:
    return True
  return False

def generateRandomIndex(state, changed_idxs):
  """
  Returns a random index from state list except the ones already present in the list provided

  :param state: current state
  :param changed_idxs: already selected indexes list, excluded options to select.
  :return: return a random index which is not present in 'changed_idxs' 
  """

  num = getRandomNumberFromRange(len(state) - 1)
  return generateRandomIndex(state, changed_idxs) if num in changed_idxs else num

def updateThePosition(itr_agent, itr_idx, agent, changed_idxs):
  """
  Update the position of the an agent in state

  :param itr_agent: agent to change position
  :param itr_idx: index of agent from the state
  :param agent: agent name to compare
  :param changed_idxs: list of indexes, updated with the agent index when the position is updated
  :return: returns the agent state with updated position otherwise returns the previous position 
  """

  itr_agent_arr = itr_agent.split(" isat ")
  if itr_agent_arr[0] == agent and itr_agent not in changed_idxs:
    updated_itr_agent = itr_agent.replace(itr_agent_arr[1], getRandomPositionExcept(itr_agent_arr[1], pos))
    changed_idxs.append(itr_idx)
    return updated_itr_agent
  else:
    return itr_agent

def getInchargeAgent(general_facts):
  """
  Check and return if there is any incharge agent defined in the facts. i.e. 'man moves all' makes man the incharge agent.

  :param general_facts: facts list from the input
  :return: return the list of agent who are defined as incharge in the facts
  """

  incharge_agent = [agent.replace(" moves all", "") for agent in general_facts if agent.split(" ")[1] == "moves" and agent.split(" ")[2] == "all"]
  return incharge_agent[0]

iteration = 0

def step(state, agents, no_of_movable_agents):
  """
  Method used to calculate the next step of the agent(s).

  :param state: current_state of the scenario
  :param agents: list of agent who are incharge who must move in every step i.e. 'man moves' makes man moveable in every step
  :param no_of_movable_agents: total number of agents that should move, as defined inside the facts i.e. '2 can_move' means upto 2 agents can move in a single step
  :return: returns a next step of the state
  """

  global iteration
  global rejected_states
  global history
  global itr_limit
  changed_idxs = []
  
  if (iteration >= itr_limit):
    print("Its taking too long, let's try again!!!")
    state = init_state
    history = []
    iteration = 0
    history.append(init_state)

  possible_new_state = list(state)
  iteration += 1

  random_number_of_movable_agents = 0
  if no_of_movable_agents > len(agents):
    random_number_of_movable_agents = getRandomNumberFromRange(no_of_movable_agents - len(agents)) + len(agents)

  incharge_agent_position = [s for s in state if getInchargeAgent(general_facts) in s][0].split(" isat ")[1]
  for agent in agents:
    possible_new_state = [updateThePosition(itr_agent, idx, agent, changed_idxs) for idx, itr_agent in enumerate(possible_new_state)]

  if random_number_of_movable_agents > len(agents):
    while random_number_of_movable_agents > len(changed_idxs):
      random_idx = generateRandomIndex(state, changed_idxs)
      single_state = possible_new_state[random_idx]
      single_state_arr = single_state.split(" isat ")

      if incharge_agent_position == single_state_arr[1]:
        possible_new_state[random_idx] = single_state.replace(single_state_arr[1], getRandomPositionExcept(single_state_arr[1], pos))
        changed_idxs.append(random_idx)

  is_rejected_state = isStateInTheList(possible_new_state, rejected_states)
  is_looping = isStateInTheList(possible_new_state, history)

  if not is_looping and not is_rejected_state:
    return possible_new_state
  return step(state, agents, no_of_movable_agents)

# Main

def apply_action(action, state):
  """
  Apply action to the state and returns the new one.

  :param action: action to apply
  :param state: current_state to apply the action on
  :return: new state with action applied
  """

  if action == "undo":
    return history[-1]
  else:
    return state

def planner(initial_state, facts, positions, constraints, final_state, iteration_limit = 1000):
  """
  Planner method receives the input of the problem scenario and calculate the steps that'll be used to solve the problem, returns a plan with a list of list.

  :param initial_state: initial state of the agent(s)
  :param facts: list of general facts
  :param positions: total number of position that are available in the problem
  :param constraints: list of total constraints of the problem
  :param final_state: goal of the problem
  :param iteration_limit: iteration limit to refresh the planner if the state is stuck in a deadlock
  :return: list of states as a plan to solve the problem
  """

  global current_state
  global init_state
  global general_facts
  global pos
  global constraints_list
  global fin_state
  global history
  global rejected_states
  global itr_limit

  init_state = initial_state
  general_facts = facts
  pos = positions
  constraints_list = constraints
  fin_state = final_state
  itr_limit = iteration_limit

  current_state = init_state
  history.append(current_state)
  
  movable_agents = getMovableActor(general_facts, init_state)
  total_no_of_movable_agents = totalNumbersOfMovableActors(general_facts, movable_agents)

  while True:
    constraint_passed = False
    if isGoalAchieved(current_state, final_state):
      print("Goal is achieved!!!")
      break
    while not constraint_passed:
      current_state = list(step(current_state, movable_agents, total_no_of_movable_agents))
      constraint_applied = isAnyConstraintFailing(constraints_list, current_state)
      if constraint_applied == False:
        history.append(current_state)
        constraint_passed = True
      else:
        after_action_state = apply_action(constraint_applied["action"], current_state)
        rejected_states.append(current_state)
        current_state = list(after_action_state)
    
    print("No. of rejected states: ", len(rejected_states)) 
    rejected_states = []
  return history