
def replace_agent(agent_list, agent, new_type):
    """
    Заменяет агента в списке на новый тип агента.

    Args:
        agent_list (list): Список всех агентов
        agent (Agent): Агент, который должен быть заменён
        new_type (str): Тип нового агента ('zombie' или 'recovered')
    """
    index = agent_list.index(agent)

    if new_type == "zombie":
        from ZombieAgent import ZombieAgent
        agent_list[index] = ZombieAgent(agent.id, agent.x, agent.y, agent.vision_radius, agent.vision_angle)
    elif new_type == "recovered":
        from RecoveredAgent import RecoveredAgent
        agent_list[index] = RecoveredAgent(agent.id, agent.x, agent.y)
