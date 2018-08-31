
class ObjectiveAI(object):

    def __init__(self,objective = None):

        if objective == None:
            objective = {
                    'damage':1,
                    'hp':-4,
                    'kill':999,
                    }

        self.objective = objective

    def Cardplay
