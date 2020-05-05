import json
import re
import string
import sys

import pandas as pd
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from unidecode import unidecode


class AssinanteTwitter(StreamListener):
    def __init__(self):
        super().__init__()
        self.df = pd.DataFrame(columns=['date', 'text'])
        self.counter = 0

    def on_data(self, data):
        conteudoJSON = json.loads(data)
        if "text" in conteudoJSON:
            print(conteudoJSON["text"])
            text = self.remove_basic(unidecode(conteudoJSON["text"]))
            print(text)
            date = conteudoJSON['created_at']
            if len(text) > 10:
                if self.counter > 10000:
                    sys.exit()
                self.df.loc[self.counter] = [date, text]
                if not self.counter % 10:
                    self.df.to_csv('log.csv', index=False)
                self.counter = self.counter + 1
        return True

    def remove_basic(self, text):
        return text.replace('\r', ' ').replace('\n', ' ').replace(',', ' ').replace("'", '')

    def remove_punct(self, text):
        text = "".join([char for char in text if char not in string.punctuation])
        text = re.sub('[0-9]+', '', text)
        return text

    # Essa funÃ§Ã£o serÃ¡ invocada automaticamente toda vez que ocorrer um erro
    def on_error(self, status):
        print(status)


# dados de autenticação
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

# Para executar esse exemplo Ã© preciso possuir uma conta no twitter, caso nÃ£o possua crie uma.
# Entre no site http://apps.twitter.com e crie uma nova applicaÃ§Ã£o preenchendo as informaÃ§Ãµes
# SerÃ¡ gerado o consumer key e o consumer secret, que sÃ£o a identificaÃ§Ã£o de sua aplicaÃ§Ã£o no twitter.
print("Inicio do programa")

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, AssinanteTwitter())
stream.filter(track=['quarentena', 'isolamento', 'carentena'], languages=['pt'])
