“Estadística General” Proceso de Poisson – Modelos de Probabilidad
PROCESO DE POISSON (Simeón Denis Poisson, 1781 – 1840):
Siméon Denis Poisson (Pithiviers, Francia, 1781 – Sceaux, Francia, 1840), fue un
físico y matemático francés al que se le conoce por sus diferentes trabajos en el
campo de la electricidad, también hizo publicaciones sobre la geometría diferencial y
la teoría de probabilidades. En 1837 publicó en Rerecherchés sur la probabilite des
jugements, un trabajo importante en la probabilidad, en el cual describe la
probabilidad como un acontecimiento fortuito ocurrido en un tiempo, entonces el
evento ocurre algunas veces.
Este proceso, también se lo suele llamar, proceso de generación de sucesos o
acontecimientos raros (aquellos sucesos o acontecimientos que se dan con cierta rareza o bien no se
esperan que ellos ocurran). Podemos decir que un proceso de Poisson es una sucesión de fallas o
acontecimientos puntuales que ocupan, individualmente, una porción despreciable en un medio
continuo. En dos intervalos de tiempo disjuntos, el número de acontecimientos puntuales o fallas son
independientes.
Diremos que en el medio continuo se produce una falla si ocurre el acontecimiento puntual.
Un proceso de Poisson queda definido por un solo parámetro fundamental: el número de fallas(o
acontecimientos puntuales) promedio por unidad de continuo, designado universalmente con la
letra griega lambda “”, también a este parámetro se lo denomina tasa del proceso, tasa de fallas
o tasa de acontecimientos puntuales. Por ejemplo, podemos definir que a un negocio llegan en
promedio 0,1 clientes por minuto o bien, siendo lo mismo, 6 clientes en promedio por hora. Lo que no
se puede afirmar, por lo expresado anteriormente, que en 8 horas de atención ingresarán 48 clientes.
La unidad de referencia del continuo es totalmente arbitraria.
Número promedio de fallas o acontecimi entos puntuales
 
Unidad de extensión de continuo
En un proceso de Poisson se cumplen las siguientes características:
 Los sucesos, acontecimientos puntuales o fallas se producen dentro de un continuo (el
tiempo, una longitud, un área, etc.) y no ocupan una porción apreciable del mismo (son
instantáneos o puntuales).
 La probabilidad de que ocurra un número dado de sucesos, acontecimientos puntuales
o fallas en una porción dada del continuo, es independiente de la posición de la porción
dentro del mismo.
 La probabilidad de que ocurra un suceso, acontecimiento puntual o falla en una porción
dada del continuo, es independiente de la ocurrencia de sucesos en otros trozos del
continuo.
Las características anteriores se pueden resumir diciendo que los sucesos, acontecimientos
puntuales o fallas se producen o generan individual, exclusiva y colectivamente al azar dentro
del continuo de observación en un instante impredecible.
Algunos autores definen al proceso de Poisson como un experimento aleatorio dónde se
cumple la siguiente proposición:
Si en un intervalo de números reales en el cual ocurren conteos al azar a lo largo del intervalo,
se puede hacer una partición del intervalo en sub-intervalos con una longitud suficientemente
Ing. Sergio Aníbal Dopazo Página 103 de 120

pequeña en las que se cumple: a) la probabilidad de más de un conteo en un sub-intervalo es cero, b)
la probabilidad de un conteo en un sub-intervalo es la misma para todos los sub-intervalos y
proporcional a la longitud del sub-intervalo, y, el conteo en cada sub-intervalo es independiente de los
demás sub-intervalos.
Son ejemplos del proceso:
 Fallas o roturas accidentales en el tiempo,
 Llegadas de paquetes a un enlace de salida de una red de acceso a Internet (en este
caso, hay que desarrollar un Modelado basado en un Proceso de Markov
Poissoniano).
 Fallas puntuales en medios continuos,
 Llegadas a un puesto o unidad de servicio,
 Llamadas telefónicas recibidas en una línea,
 Llegadas de personas a un comercio,
 Fallas de aislación en un proceso de fabricación de cable plástico,
 Fallas en los rollos de alfombra moqueta,
 Clientes atendidos,
 Arribos a un aeropuerto o estación Terminal,
 Arribos de pedidos,
 Cortes de luz accidentales en una ciudad,
 Accidentes de tránsito en una ciudad,
 Goles en un partido de fútbol no arreglado, etc.
En el proceso de Poisson intervienen, además del parámetro, dos elementos:
 “t” o “x”, que es el continuo de observación o de estudio;
 “r”, que es la cantidad de fallas o acontecimientos puntuales encontrados o a encontrar
(valores enteros r 0).
Dependiendo del elemento que se fija (parametriza), el otro elemento es una variable
aleatoria.
En el proceso de Poisson, podemos reconocer básicamente dos modelos o distribuciones de
probabilidad: “El Modelo de Poisson” y “El Modelo Gamma”, los cuales responden
(recíprocamente) a dos interrogantes:
a) Si se observa un determinado continuo “t”, ¿qué probabilidad hay de que se generen
exactamente “r” fallas o acontecimientos puntuales?
b) Si se observa al continuo a fin de obtener “r” fallas o acontecimientos puntuales, ¿qué
probabilidad hay de que sea necesario un determinado continuo “t” (en este caso “x”) para
obtener dichas fallas o dichos acontecimientos puntuales?
También en el proceso de Poisson, podemos reconocer a otro modelo: “El Modelo
Exponencial”. Este modelo se puede estudiar como un caso particular del modelo Gamma para un
valor de “r = 1”, esto quiere decir que en el continuo observado no hay fallas.
A continuación desarrollaremos los modelos básicos.
Página 104 de 120 Ing. Sergio Aníbal Dopazo

“Estadística General” Proceso de Poisson – Modelos de Probabilidad
A. MODELO de POISSON:
Este modelo fue desarrollado por Siméon Denis Poisson en 1838. Este modelo es una
distribución de probabilidad de variable aleatoria discreta que expresa, a partir de una frecuencia de
ocurrencia media “”, la probabilidad que ocurra un determinado número de eventos durante cierto
período de tiempo. Las variables aleatorias que siguen este comportamiento tienen la propiedad de
ser infinitamente divisibles.
Además del parámetro del proceso “” se fija un continuo determinado “t” de observación o
de estudio, entonces se observa el número de acontecimientos puntuales que se generan en ese
determinado continuo. De manera que este modelo estudia a una variable aleatoria discreta “r” que
representa el número de eventos, fallas o acontecimientos puntuales independientes que ocurren a
una tasa constante sobre el tiempo o sobre el espacio. El valor de “t” se fija antes de realizar la
observación o antes de los experimentos, esto significa que este valor se convierte en un parámetro
para el modelo.
Es un modelo que se ha empleado, por sus características, para estudiar las líneas de espera,
en confiabilidad, en control de calidad, en mercadotecnia, medicina y otras aplicaciones. Sin
embargo, debe aplicarse cuidadosamente a situaciones en las que las condiciones de independencia
y tasa constante de ocurrencia son dudosas. Una alternativa adecuada de aplicación al modelo de
Poisson es el modelo binomial negativo, este se utiliza cuando la ocurrencia no es constante sobre el
tiempo o el espacio.
Algunos ejemplos de uso de este modelo se pueden enunciar:
 Ocurrencia de roturas o fallas accidentales en el tiempo,
 fallas de aislación en cables,
 fallas puntuales en superficies pintadas,
 defectos de fabricación en artículos manufacturados, etc.
La variable aleatoria es “r” (cantidad de acontecimientos puntuales o fallas generados o bien
a generarse en un medio continuo “t” determinado y fijado arbitrariamente). Se debe aclarar que
primero se observan los acontecimientos en el medio continuo definido.
Parámetros del Modelo: “” y “t” Variable Aleatoria: “r”
Dominio de la Variable Aleatoria: 0r  .
En realidad en el modelo de Poisson los dos parámetros ( y t) se simplifican en uno solo, que
es “m”, el cual representa el número esperado de eventos, sucesos, fallas o acontecimientos
puntuales en un continuo “t” determinado y fijado previamente. Así podríamos definir que si “ = 0,1
personas por minuto promedio”, en un continuo determinado de “t = 10 horas”, esperamos la
generación de “m = 60 personas” en promedio. Por lo cual podemos definir que “m” se denota por
la siguiente expresión: m  t.
El modelo o función de probabilidad, describe (o calcula) la probabilidad de que se produzcan
o se generen, al azar, exactamente “r” eventos, acontecimientos puntuales o fallas en un continuo
“t” prefijado y determinado, con una generación promedio y constante de acontecimientos puntuales
por unidad de continuo “”, o sea en un proceso de tipo Poisson. Su expresión o función de
probabilidad es:
Ing. Sergio Aníbal Dopazo Página 105 de 120

e(m)mr
|     | P(VA r)P | (r / m) |     |     |     |     |
| --- | ---------- | -------- | --- | --- | --- | --- |
|     |            | po       | r!  |     |     |     |

Se cumplen las reglas generales dadas para las variables aleatorias discretas.

  Función de Probabilidad Acumulada Izquierda:

|           |          | r e(m) mx |    |     |     |     |
| --------- | -------- | ------------ | --- | --- | --- | --- |
| P(VAr)F | (r / m) |            |    |     |     |     |
|           | po       |             |    |     |     |     |
|           |          |  x!         |    |     |     |     |
x0

  Función de Probabilidad Acumulada Derecha:

|           |          |  e(m)mx |    |     |     |     |
| --------- | -------- | ----------- | --- | --- | --- | --- |
| P(VAr)G | (r / m) |           |    |     |     |     |
|           |          |            |    |     |     |     |
|           | po       |  x!        |    |     |     |     |
xr

Para ambas funciones de distribución se deben usar tablas, programas apropiados o bien
planillas de cálculo que tengan esta distribución.

|   Moda: Mor | , verifica las siguientes condiciones:  |     |     |     |     |     |
| ------------- | --------------------------------------- | --- | --- | --- | --- | --- |
o

|     |     | m1 | m |     |     |     |
| --- | --- | ----- | --- | --- | --- | --- |
|     |     | Mo  |     |     |     |     |

  Mediana: Mer . No hay una expresión plausible para determinarla, por ello también se
e
deben cumplir las siguientes condiciones:

|     |     |     |      |      |          |     |
| --- | --- | ---- | ---- | ----- | ---------- | --- |
|     |     | F r | 1/m |  0,5 | y F r /m  | 0,5 |
|     |     | po e |      |       | po e       |     |

  Esperanza Matemática: E(r)    m  t (que es el parámetro del modelo).

|   Varianza: V(r) |  2 |  m  t  |     |     |     |     |
| ----------------- | ---- | ---------- | --- | --- | --- | --- |

1
|   Coeficiente de Asimetría: As |     |   |    |     |     |     |
| ------------------------------- | --- | --- | --- | --- | --- | --- |
3
m

1
. Este coeficiente tiende a 3 cuando “” toma
|   Coeficiente de Kurtosis: Ku |     |   |  3 |     |     |     |
| ------------------------------ | --- | --- | ---- | --- | --- | --- |
4 m
valores muy grandes, este resultado (además de su tendencia a la simetría) traduce la
convergencia de la ley de Poisson a la ley Normal, en la ley Normal este coeficiente es
exactamente igual a 3.

|     |     |     |     | r  | e(m) mx |     |
| --- | --- | --- | --- | --- | ---------- | --- |
  Expectativa Parcial Izquierda: H (r/m)  x mF (r1/ m)
|     |     | po  |     |     |     | po  |
| --- | --- | --- | --- | --- | ---- | --- |
|     |     |     |     |    | x!  |     |
x0

Algunos autores han tratado a este modelo como un límite de la binomial, pero este es un
caso  particular,  el  cual  se  da  con  ciertas  restricciones.  También  este  modelo,  para  ciertas
restricciones, puede calcular en forma aproximada al modelo Binomial; y puede ser calculado de
forma aproximada por el modelo Normal (ver las restricciones de aproximación en la página 118).
| Página 106 de 120  |     |     |     |     | Ing. Sergio Aníbal Dopazo  |     |
| ------------------ | --- | --- | --- | --- | -------------------------- | --- |

“Estadística General” Proceso de Poisson – Modelos de Probabilidad
B. MODELO GAMMA o de o de MOLINA o de ERLANG (E. Molina, 1915 ; A. Erlang, 1920):
Edward Charles Dixon Molina (Estados Unidos, 1877 – Estados Unidos, 1964) fue
un ingeniero estadounidense, conocido por sus contribuciones a la ingeniería del
tráfico (telecomunicaciones). Fue autodidacta en matemáticas y entró en el
departamento de investigación de la empresa AT&T y luego, en 1901, en el
laboratorio de la Bell Co. Su invención de los traductores de relé, en 1906, dio
resultado en los sistemas del panel de marcado. Molina fue pionero en el uso de los
truenos de impacto, que en esencia eran simulaciones de Monte Carlo del tráfico
telefónico para encontrar las asignaciones de capacidad óptima, de las líneas
troncales, a las oficinas centrales. En 1952 fue galardonado con la Medalla Cresson
Elliott del Instituto Franklin.
Agner Krarup Erlang (Lonborg, Dinamarca, 1878 – Copenhague, Dinamarca, 1929)
fue un matemático, estadista, e ingeniero danés que inventó los campos de
Ingeniería de tráfico (telecomunicaciones) y la Teoría de Colas. Desarrolló su teoría
del tráfico telefónico a través de varios años. En 1909 publica "La teoría de las
probabilidades y las conversaciones telefónicas", esta publicación demostró que la
Distribución de Poisson se aplica para tráfico telefónico aleatorio.
Este modelo se rige por el proceso de Poisson. Permite modelar el lapso entre dos eventos
consecutivos de Poisson que ocurren de manera independiente, o sea que estudia la duración de
elementos que fallan a la Poisson. La variable aleatoria es la extensión de continuo entre fallas
consecutivas de un proceso de Poisson (el mismo se emplea para estudiar, como un caso particular,
al modelo Exponencial que desarrollamos anteriormente).
Este modelo se utiliza con habitualidad para modelar la extensión del continuo necesaria para
que se generen “r” acontecimientos puntuales o fallas. Este modelo también es utilizado en otras
aplicaciones, como la duración total de un stock de “r” elementos cuya falla individual se produce por
fallas aleatorias. Este modelo estudia problemas de tipo Poissonianos, que se representa como la
suma de una serie de variables de comportamiento exponenciales (todas con el mismo “”).
También se lo utiliza para estudiar situaciones, que a simple vista, no parecen Poissonianas
como la demanda de algunos artículos en períodos cortos, lluvia caída en una región (también en un
período corto de tiempo). Es importante aclarar que, en estas situaciones, “r” no tiene que ser un
número entero.
Resumiendo, podemos decir que, si estamos en un proceso, perfecto, de Poisson “r” es
entero, de lo contrario, será un número real positivo. Cuando “r” es un número natural, el modelo se
denomina “Modelo o Distribución de Probabilidad de Erlang – Molina” propiamente dicho; en
cambio si “r” es un número real no negativo, el modelo se denomina “Modelo o Distribución de
Probabilidad Gamma” propiamente dicho.
Los parámetros del modelo son: “”, de escala, que representa la tasa del acontecimiento
puntual o falla (o sea el número medio de acontecimientos puntuales o fallas por unidad de
continuo); y “r”, parámetro de forma, que indica el número de acontecimientos puntuales o fallas
deseados. Cuando el valor de “r” es igual que 1, el modelo Gamma se comporta como el modelo
Exponencial. Este modelo tiene un análisis similar que el modelo de Pascal en el proceso de
Bernoulli. Así como en el modelo de Poisson, la variable aleatoria es el número de acontecimientos
puntuales “r” y sus parámetros son “” y la unidad de continuo “t”, en este modelo el objeto de
Ing. Sergio Aníbal Dopazo Página 107 de 120

estudio es el continuo (en este caso “x”) necesario para que se den ciertos acontecimientos
puntuales “r”.
Algunos autores, tratan a este modelo como una sumatoria de exponenciales todas con el
mismo valor de “”, esto se sustenta con el siguiente razonamiento: si se define a un modelo
exponencial como el continuo necesario para la ocurrencia de la primer falla, si a continuación le
adicionamos otra exponencial igual, el resultado será el continuo necesario para la ocurrencia de dos
fallas. Si adicionamos “r” exponenciales tendremos un continuo necesario para la ocurrencia de “r”
fallas o acontecimientos puntuales (o sea una Gamma).
Un caso particular de la Gamma es el modelo o distribución de probabilidad denominado
“Chi–Cuadrado”, el cual escapa al tratamiento de este curso.
Ejemplos de uso de este modelo: tráfico en líneas telefónicas, los metros de tela que
contengan cierto número de fallas, tiempo necesario para la falla de cierto número de elementos,
tiempo necesario para que se produzcan cierto número de arribos, precipitaciones en un determinado
lapso de tiempo, demanda de productos perecederos en un determinado lapso de tiempo, etc.
 Parámetros del Modelo: “” (de escala) y “r” (de forma). Ambos mayores que cero.
 Dominio de la Variable Aleatoria: x0. El continuo “t”, se convierte en la variable
aleatoria “x”.
 Función de densidad de probabilidad: Su expresión es:
 
f(x) xr1 e(X)  xr1 e(X)
r1!

r
 Gráfica de la función de densidad:
Página 108 de 120 Ing. Sergio Aníbal Dopazo

“Estadística General”  Proceso de Poisson – Modelos de Probabilidad

Tal como podemos visualizar en la gráfica: si “0 < r < 1”, la función tiene una forma de J
transpuesta; si “r > 1”, la función presenta una asimetría positiva, y, si “r = 1”, la función
toma la forma del modelo exponencial (siendo un caso particular del modelo Gamma.

Se cumplen las reglas generales dadas para las variables aleatorias continuas.

  Función de Distribución de Probabilidad: Para este modelo se desarrolla la función de
distribución de probabilidad acumulada izquierda.

x
 xr1
| P(VA | x)F | (x/r ;) |    |     | e(X) | dx.  |     |
| ----- | ---- | --------- | --- | --- | ------- | ----- | --- |


0 r

Además se puede desarrollar esta expresión de la siguiente manera:

r1
|     |     |     |     |  x | ex |     |     |
| --- | --- | --- | --- | ----- | -------- | --- | --- |
x r1;
| F (x/r | ;)F | /   |     |     |     |     |     |
| ------ | ----- | --- | --- | --- | --- | --- | --- |
|       |       |    |     |    |     |     |     |
r

Esta  expresión  no  se  puede  resolver  con  procedimientos  elementales  del  análisis
matemático, pero dependiendo de los valores que puede tomar el parámetro “r”, este
cálculo se lo puede simplificar o bien reducir, utilizando las siguientes relaciones:

Si “r” es un número natural mayor que uno, esta expresión es posible calcularla con la
distribución de Poisson, esta relación fue desarrollada por Edwards C. D. Molina en 1915.
Por eso a la siguiente relación se la conoce como relación de Molina, el cual desarrolló la
relación existente entre este modelo y los procesos de Poisson.

|       |      |           |     | r/m x  |     |     |     |
| ----- | ---- | --------- | --- | ----------- | --- | --- | --- |
| P(VA | x)F | (x/r ;) | G   |             |     |     |     |
|       |      |          | po  |             |     |     |     |

r1/mx
| P(VAx)G |     | (x/r ;)F |     |     |     |     |     |
| --------- | --- | ---------- | --- | --- | --- | --- | --- |
|           |     |           | po  |     |     |     |     |

Cuando “r” es distinto que uno y mayor a cero (siendo un número no natural), la relación
de molina no puede usarse. En estos casos hay que usar software que contengan a este
modelo.  Suele  usarse,  en  forma  habitual,  la  aproximación  desarrollada  por  Edwin  B.
Wilson y Margaret M. Hilferty en 1931, la misma se basa en el principio que como este
modelo es el resultado  de  una suma  de  exponenciales,  esta suma tiende  al modelo
normal. Entonces para resolver esta función se usa la distribución normal estándar.

|       |      |                |     |     |      | 1   |     |
| ----- | ---- | -------------- | --- | ---- | ----- | --- | ----- |
|       |      |                |     |     | x | 3 1 |      |
| P(VA | x)F | (x/r ;)Z |     | 3 | r  |    | 1  |

|     |     |    |     |     |   r |  9r |    |
| --- | --- | --- | --- | --- | ----- | ----- | --- |
|     |     |     |     |    |      |       |   |
|     |     |     |     |    |       |       |    |

PVA xF x r;F  2 2x  2r  , relación exacta usando la distribución
|     |     |    | 2  |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
Chi – Cuadrado.

r 1
|   Moda: Mo |    | , si r | 1, caso contrario Mo0  |     |     |     |     |
| ----------- | --- | ------ | ------------------------ | --- | --- | --- | --- |


Ing. Sergio Aníbal Dopazo  Página 109 de 120

  Mediana: No hay una expresión a partir de la función Gamma para determinarla, se puede
calcular  en forma exacta con la distribución Chi – Cuadrado o en forma aproximada con la
expresión de Wilson – Hilferty. También se puede usar software que tengan la inversa de
la distribución Gamma.

2
Me  0,5;2r , relación exacta usando el fractil de la distribución Chi – Cuadrado.
2

3
r  1 
Me  1  , utilizando la aproximación de Wilson – Hilferty.
  9r

r
Esperanza Matemática: Ex
|    |     |     |     |     |     |     |
| --- | --- | --- | ----- | --- | --- | --- |


r
|   Varianza: Vx |  2  |     |     |     |     |     |
| ----------------- | ------ | --- | --- | --- | --- | --- |
2


  Coeficiente de Variación:  Cv 100. En este modelo el coeficiente de variación es,

generalmente, mayor al 30% y va disminuyendo a medida que el parámetro “r” aumenta
considerablemente manteniendo el valor de “” o no.

  Fractiles: No hay una expresión a partir de la función Gamma para determinarla, se puede
calcular  en forma exacta con la distribución Chi – Cuadrado o en forma aproximada con la
expresión de Wilson – Hilferty. También se puede usar software que tengan la inversa de
la distribución Gamma.

2
x  ;2r , relación exacta usando el fractil de la distribución Chi – Cuadrado.

2

3
|  r |   Z | 1   |    |     |     |     |
| --- | ----- | --- | --- | --- | --- | --- |

x      1 , utilizando la aproximación de Wilson – Hilferty.
|   |  9r |     |    |     |     |     |
| ------- | ----- | --- | --- | --- | --- | --- |
|         | 3 r |     |    |     |     |     |

|                                 |     |     |         | x 3       |     |     |
| ------------------------------- | --- | --- | -------- | ----------- | --- | --- |
|                                 |     |     |         |  f(x)dx |     | 2   |
|   Coeficiente de Asimetría: As |     |     |     |             |    |     |
|                                 |     |     | 3        | 3          |     |     |
r


|     |     |     |    | x  4 f(x)dx |     |     |
| --- | --- | --- | --- | ----------------- | --- | --- |
6
|                              |     | Ku  |     |     |    | 3                   |
| ---------------------------- | --- | --- | -------- | --- | --- | -------------------- |
|   Coeficiente de Kurtosis:  |     |     |          |     |     | . Este modelo tiene  |
|                              |     |     | 4        | 4  |     | r                    |
agudeza de tipo leptocúrtica.

r
|   Expectativa Parcial Izquierda: H |     |     | (x/r;) | F (x / r1;).  |     |     |
| ----------------------------------- | --- | --- | -------- | ---------------- | --- | --- |
|                                     |     |     |         |                |     |     |

| Página 110 de 120  |     |     |     |     | Ing. Sergio Aníbal Dopazo  |     |
| ------------------ | --- | --- | --- | --- | -------------------------- | --- |

“Estadística General” Proceso de Poisson – Modelos de Probabilidad
Ing. Sergio Aníbal Dopazo Página 111 de 120