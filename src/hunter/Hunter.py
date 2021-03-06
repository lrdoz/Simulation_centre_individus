import sys
from src.core.Agent import Agent
from operator import itemgetter
from pynput import keyboard


"""
Implémentation d'un agent ayant le comportement d'un Chasseur
"""
class Hunter(Agent):
    def __init__(self, posX, posY, data):
        # position initiale de la particule
        super(Hunter, self).__init__(posX, posY)

        # Gestation
        self.delay = data[0]
        self.form = "circle"
        self.fearMode = False
        self.nfear = 0
        self.maxfear = 5

    def decide(self, env):
        """
        Méthode qui permet à un agent de décider de son comportement

        :param env: Environement de l'agent
        """
        #notion de délai pour les hunters
        self.time +=1


        if self.delay <= self.time :
            self.time = 0

            nearPos = env.vonNeumman(self.posX, self.posY) # essaye de chasser la cible

            #Supprime tous les mur
            nearPos = [ agent for agent in nearPos if agent[2] != -1]

            #Si l'agent peut bouger
            if nearPos:

                if not self.fearMode:
                    self.nfear = 0
                    newPos = min(nearPos, key=itemgetter(2))
                else:
                    self.nfear += 1
                    if self.nfear >= self.maxfear:
                        self.fearMode = False
                    newPos = max(nearPos, key=itemgetter(2))

                if (newPos[1] != None and newPos[1].getType() == 0):
                    env.kill(newPos[0][0], newPos[0][1])
                    env.setAgentPosition(self, newPos[0][0], newPos[0][1])
                    self.posX, self.posY = newPos[0]
                else:
                    while len(nearPos) != 0:
                        #On regarde si c'est un mur
                        if(newPos[1] != None):
                            nearPos.remove(newPos)
                            if (nearPos == []):
                                return
                            newPos = min(nearPos, key=itemgetter(2))
                        else:
                            env.setAgentPosition(self, newPos[0][0], newPos[0][1])
                            self.posX, self.posY = newPos[0]
                            return
    def on_press(self, key):
        #On change le vector du pac man
        if key == keyboard.KeyCode.from_char('a'):
            if self.delay > 0:
                self.delay -=1
        elif key == keyboard.KeyCode.from_char('z'):
            self.delay += 1

    def getColor(self):
        """
        Retourne la couleur de l'agent

        :return: Couleur de l'agent
        """
        return "red"

    def getType(self):
        """
        Retourne le type de l'agent

        :return: Retourne le type de l'agent
        """
        return 2
