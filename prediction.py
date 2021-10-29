import logging
from blinker import signal
import time

from mqttclient import MQTTClient
import pandas as pd
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor


class MyIA():

    # knn = KNeighborsClassifier(n_neighbors=5)
    # regr = LinearRegression()
    clf=RandomForestRegressor(n_estimators=100)

    def apprendre(self):
        frame = pd.read_csv("stats.csv")
        y = frame['chance_de_win']
        x = frame[['age','taille','poids','nb_win','nb_lose']]
        #Train the model using the sets
        self.clf.fit(x, y)
    
    def predict(self, msg):
        Rframe = pd.DataFrame([
        {'age': msg['player1']['age'], 
        'taile': msg['player1']['height'], 
        'poids': msg['player1']['weight'], 
        'nb_win': msg['player1']['nbWin'], 
        'nb_lose': msg['player1']['nbLos']},
        {'age': msg['player2']['age'], 
        'taile': msg['player2']['height'], 
        'poids': msg['player2']['weight'], 
        'nb_win': msg['player2']['nbWin'], 
        'nb_lose': msg['player2']['nbLos']}
        ])
        print(Rframe)
        yres = self.clf.predict(Rframe)
        print('Score 1 : ')
        print(yres[0])
        print('Score 2 : ')
        print(yres[1])

        #chance1 = ((yres[0]+1)/(yres[0]+yres[1]+2))*100
        chance1 = ((yres[0])/(yres[0]+yres[1]))*100
        chance1 = round(chance1)
        return chance1

    
class MyApp():

    #nomD = "rien"

    def __init__(self):

        self.nomD = "rien"
        # pass

    
    # Sending a MQTT Message through blinker signals
    def run(self):
        ii = 0
        print("recep prete")
        while ii < 20:
            print("recep : " + self.nomD)
            time.sleep(5)
            ii = ii+1


def main():

    # ---------------------------------
    # Initializing MQTT
    mqtt_client = MQTTClient(['prediction/infos'])
    mqtt_client.setup()
    mqtt_client.run()
    
    app = MyApp()
    IA = MyIA()
    IA.apprendre()
    print('Apprentissage fini')

    def on_predi(msg):
        print("message predi reçu")
        app.nomD = app.nomD + "+"
        # app.nomD = msg["nom"]
        chance1 = IA.predict(msg)
        chance2 = 100 - chance1
        sig = signal('message')
        sig.send({'topic': "client/prediction", 'body': {'player1': chance1,'player2': chance2} })
        print("message envoyé")


    sig_2 = signal('prediction/infos')
    sig_2.connect(on_predi)

    # ---------------------------------
    # TODO: Start my application
    
    app.run()

    # ---------------------------------
    # Closing connection
    mqtt_client.stop()

if __name__ == "__main__":
    main()