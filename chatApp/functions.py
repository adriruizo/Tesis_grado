#Funciones necesarias para el modelo de regresión logística
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import load
import numpy as np

def open_text(archivo):
    with open(archivo, 'r') as file:
        text = file.read().splitlines()
        file.close()
    return text

def clean_text(archivo):
    with open(archivo, 'r') as file:
        text = file.read().splitlines()
        file.close()
    lineas1 = [w.lower() for w in text]# convertir a minúsculas
    lineas2=[w.replace('-', ' ') for w in lineas1]
    lineas=[w.replace('/', ' ') for w in lineas2]
    re_punt = re.compile('[¿%s]' % re.escape(string.punctuation))# prepare a regex para el filtrado de caracteres
    texto = [re_punt.sub('', w) for w in lineas]# eliminar la puntuación de cada palabra
    return texto

def clean(entrada):
    lineas1 = [w.lower() for w in entrada.splitlines()]# convertir a minúsculas
    #lineas2=[w.replace('-', ' ') for w in lineas1]
    #lineas=[w.replace('/', ' ') for w in lineas2]
    re_punt = re.compile('[¡¿%s]' % re.escape(string.punctuation))# prepare a regex para el filtrado de caracteres
    texto = [re_punt.sub('', w) for w in lineas1]# eliminar la puntuación de cada palabra
    return texto

def salida_chat(entrada, archivo):
    pregunta=str(clean(entrada))
    salir=False
    for j in range(0,len(archivo)):
        var=pregunta.find(archivo[j])
        if var!= -1:
            salir = True
            break
    return salir

model=load('C:/Users/ADRIANA/trabajo_grado/chatApp/TF-IDF_R.Log_Model.joblib')
respuestas=open_text('C:/Users/ADRIANA/trabajo_grado/chatApp/Respuestas.txt')
stopwords=open_text('C:/Users/ADRIANA/trabajo_grado/chatApp/Stop_List.txt')
text_preguntas=clean_text('C:/Users/ADRIANA/trabajo_grado/chatApp/Preguntas.txt')
arch_sal_chat=clean_text('C:/Users/ADRIANA/trabajo_grado/chatApp/Salir_Chat.txt')
cv=TfidfVectorizer(stop_words=stopwords)
vector=cv.fit_transform(text_preguntas)
vectorizer_preguntas = TfidfVectorizer(ngram_range=(1,1))
XP = vectorizer_preguntas.fit_transform(text_preguntas)

def chat_bot(pregunta):
    salida=salida_chat(pregunta,arch_sal_chat)
    if salida != True:
        word_vector=cv.transform([pregunta])
        c=np.count_nonzero(word_vector.toarray())
        entrada=clean(pregunta)
        if len(str(entrada).split()) == 1:#si se ingresa una sola palabra
            if entrada[0] == "si" or entrada[0] == "sí":
                respuesta="¿En qué puedo ayudarle?"
            elif entrada[0] == "no":
                respuesta="¿No requiere alguna otra información?"
            elif (entrada[0] == "excelente") or (entrada[0] == "teléfono") or (entrada[0] == "email") or (entrada[0] == "comprendo") or (entrada[0] == "saludo") or (entrada[0] == "hola") or (entrada[0] == "saludos") or (entrada[0] == "buenas") or (entrada[0] == "listo") or (entrada[0] == "llamaré") or (entrada[0] == "genial") or (entrada[0] == "ok") or (entrada[0] == "buenísimo") or (entrada[0] == "perfecto") or (entrada[0] == "super") or (entrada[0] == "entiendo") or (entrada[0] == "bien") or (entrada[0] == "entendido") or (entrada[0] == "mmm") or (entrada[0] == "emm")  or (entrada[0] == "eh") or (entrada[0] == "aja") or (entrada[0] == "exacto") or (entrada[0] == "jumm") or (entrada[0] == "umm") or (entrada[0] == "jeje") or (entrada[0] == "jajaja") or (entrada[0] == "claro") or (entrada[0] == "bueno") or (entrada[0] == "gracias") or (entrada[0] == "correcto"):
                pregunta = vectorizer_preguntas.transform([pregunta])
                pred=model.predict(pregunta.toarray())
                aux_pos=(int(pred.item()))
                respuesta = respuestas[aux_pos]
            elif c == 1:
                respuesta="No comprendo su pregunta, por favor sea más claro"
            else:
                respuesta="No puedo responder a este tipo de inquietudes, pero puedo ayudarle con todo lo relacionado con el examen de traductor e intérprete oficial, ¿Hay algo en lo que pueda ayudarle?"
            
        else:
            if (entrada[0] == "de acuerdo") or (entrada[0] == "por supuesto") or (entrada[0] == "muy bien") or (entrada[0] == "está bien") or (entrada[0] == "es claro") or (entrada[0] == "me comunicaré") or (entrada[0] == "que bien") or (entrada[0] == "le agradezco") or (entrada[0] == "muchas gracias") or (entrada[0] == "muy gentil") or (c > 1):
                pregunta = vectorizer_preguntas.transform([pregunta])
                pred=model.predict(pregunta.toarray())
                aux_pos=(int(pred.item()))
                respuesta = respuestas[aux_pos]
            elif c == 1:
                respuesta="No comprendo su pregunta, por favor sea más claro"
            else:
                respuesta="No puedo responder a este tipo de inquietudes, pero puedo ayudarle con todo lo relacionado con el examen de traductor e intérprete oficial, ¿Hay algo en lo que pueda ayudarle?"
            
    else:
        respuesta="Hasta pronto. Vuelva y cualquier inquietud con gusto será atendida."" Para peticiones, quejas, reclamos y sugerencias por favor comunicarse a la Escuela de Idiomas. Prof. Gabriel Quiroz, teléfono (57)(4) 219 8997 o escribir al correo electrónico: examentraductorinterpreteoficial@udea.edu.co"
        
    print(respuesta)
    return respuesta