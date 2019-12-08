#Funciones necesarias para el modelo de regresión
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

#Limpiar pregunta
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

model=load('C:/Users/ADRIANA/trabajo_grado/chatApp/TF-IDF_R.Log_Model2.joblib')
respuestas=open_text('C:/Users/ADRIANA/trabajo_grado/chatApp/Respuestas2.txt')
stopwords=open_text('C:/Users/ADRIANA/trabajo_grado/chatApp/Stop_List.txt')
text_preguntas=clean_text('C:/Users/ADRIANA/trabajo_grado/chatApp/Preguntas2.txt')
arch_sal_chat=clean_text('C:/Users/ADRIANA/trabajo_grado/chatApp/Salir_Chat.txt')
cv=TfidfVectorizer(stop_words=stopwords)
vector=cv.fit_transform(text_preguntas)
vectorizer_preguntas = TfidfVectorizer(ngram_range=(1,1))
XP = vectorizer_preguntas.fit_transform(text_preguntas)

def chat_bot(pregunta):
    #pregunta=request.POST["pregunta"]
    salida=salida_chat(pregunta,arch_sal_chat)
    if salida != True:
        word_vector=cv.transform([pregunta])
        if np.max(word_vector) != 0:#valida si la pregunta ingresada tiene que ver con el examen, sin tomar stopwords
            entrada=clean(pregunta)
            if len(str(entrada).split()) == 1:#si se ingresa una sola palabra
                #entrada=clean(pregunta)
                if entrada[0] == "si" or entrada[0] == "sí":
                    respuesta="¿En qué puedo ayudarle?"
                    #return HttpResponse("¿En qué puedo ayudarle?")
                elif entrada[0] == "no":
                    respuesta="¿No requiere alguna otra información?"
                    #return HttpResponse("¿No requiere alguna otra información?")
                elif entrada[0] != "excelente" and entrada[0] != "listo" and entrada[0] != "llamaré" and entrada[0] != "genial" and entrada[0] != "ok" and entrada[0] != "buenísimo" and entrada[0] != "perfecto" and entrada[0] != "super" and entrada[0] != "no" and entrada[0] != "si" and entrada[0] != "sí" and entrada[0] != "entiendo" and entrada[0] != "bien" and entrada[0] != "entendido" and entrada[0] != "mmm" and entrada[0] != "emm"  and entrada[0] != "eh" and entrada[0] != "aja" and entrada[0] != "exacto" and entrada[0] != "jumm" and entrada[0] != "umm" and entrada[0] != "jeje" and entrada[0] != "jajaja" and entrada[0] != "claro" and entrada[0] != "bueno" and entrada[0] != "gracias" and entrada[0] != "correcto":
                    respuesta="No comprendo su pregunta, por favor sea más claro"
                    #return HttpResponse("No comprendo su pregunta, por favor sea más claro")
                else:
                    pregunta = vectorizer_preguntas.transform([pregunta])
                    pred=model.predict(pregunta.toarray())
                    aux_pos=(int(pred.item()))
                    respuesta = respuestas[aux_pos]
                    #return HttpResponse(respuesta_p)
            else:#se valida si al aplicar stop words se queda con una sola palabra
                c=np.count_nonzero(word_vector.toarray())
                if c == 1:
                    respuesta="No comprendo su pregunta, por favor sea más claro"
                else:
                    pregunta = vectorizer_preguntas.transform([pregunta])
                    pred=model.predict(pregunta.toarray())
                    aux_pos=(int(pred.item()))
                    respuesta = respuestas[aux_pos]
                    #return HttpResponse(respuesta_p)
                
        else:
            respuesta='No puedo responder a este tipo de inquietudes, pero puedo ayudarle con todo lo relacionado con el examen de traductor e intérprete oficial, ¿Hay algo en lo que pueda ayudarle?'
            #return HttpResponse("No puedo responder a este tipo de inquietudes, pero puedo ayudarle con todo lo relacionado con el examen de traductor"
                 #"e intérprete oficial, ¿Hay algo en lo que pueda ayudarle?")
         
    else:
        respuesta="Hasta pronto. Vuelva y cualquier inquietud con gusto será atendida."" Para peticiones, quejas, reclamos y sugerencias por favor comunicarse a la Escuela de Idiomas. Prof. Gabriel Quiroz, teléfono (57)(4) 219 8997 o escribir al correo electrónico: examentraductorinterpreteoficial@udea.edu.co"
        #return HttpResponse("Hasta pronto. Vuelva y cualquier inquietud con gusto será atendida."" Para peticiones, quejas, reclamos y sugerencias por favor comunicarse a la Escuela de Idiomas. Prof. Gabriel Quiroz, teléfono (57)(4) 219 8997 o escribir al correo electrónico: examentraductorinterpreteoficial@udea.edu.co")
    print(respuesta)
    return respuesta