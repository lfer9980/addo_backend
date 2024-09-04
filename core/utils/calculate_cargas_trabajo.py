import functools

class CargasCalc:

    @staticmethod
    async def calculate_ct(cte: float, tcve: float, ce: int) -> float:
        return (cte / tcve) * ce
    
    @staticmethod
    async def calculate_tcve_from_ct(cte: int, ce: int, ct: float) -> float:
        return (cte * ce) / ct
    
    @staticmethod
    async def calculate_tcve(tareas: list[int], new_tarea: int | None = None) -> float:
        tareas_list= [tarea.to_dict()["complejidad"] for tarea in tareas]
        
        if new_tarea is not None:
            tareas_list.append(new_tarea)

        return functools.reduce(lambda a, b: a + b, tareas_list, 0)