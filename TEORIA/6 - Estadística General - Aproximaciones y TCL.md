“Estadística General” Teorema Central del Límite (Suma de Variables Aleatorias)
TEOREMA CENTRAL del LÍMITE (SUMA DE VARIABLES ALEATORIAS)
En la realidad que nos rodea, se presentan variables, no siempre en estado puro, o a veces de
difícil análisis respecto de cuál es el modelo a aplicar; por ello, habitualmente las variables son
estudiadas de manera agrupada. He aquí, la importancia de este capítulo.
A veces, al investigador, se le hace dificultoso estudiar la venta diaria de un determinado
producto en una empresa. Pero gracias a los conceptos vertidos en el presente capítulo, se podrá
estudiar con cierta facilidad a esta variable de forma agrupada, por ejemplo: la venta mensual o
anual (que es la suma de ventas diarias). La modelización de una variable aleatoria, o bien
determinar el modelo de comportamiento de una variable aleatoria, es un tema complejo y no es
objetivo del presente curso. Por eso, en la aplicación práctica y rápida del estudio de una determinada
variable aleatoria, es necesario especificar el entorno de variación, aunque no sepamos cuál es el
modelo de referencia de la misma. No obstante, debemos aclarar que la tecnología nos provee de
herramientas para la modelización de dicha variable aleatoria (hecho que, antes de la aparición de
algunos programas de computación, llevaba un tiempo considerable de estudio). Es por ello, que uno
de los temas que se trata en el presente capítulo (aproximaciones y relaciones de los modelos) con el
tiempo caerá en el olvido.
El Teorema Central de Límite no es un único teorema, sino que consiste en un conjunto de
resultados acerca del comportamiento de la distribución de la suma (o promedio) de variables
aleatorias. Con Teorema Central del Límite nos referiremos a todo teorema en el que se afirma, bajo
ciertas hipótesis, que la distribución de la suma de un número muy grande de variables aleatorias se
aproxima a una distribución normal. El término “Central”, debido a Polyá en 1920, significa
fundamental, o de “ìmportancia central”, este término describe el rol que cumple este teorema en la
teoría de probabilidades. Su importancia radica en que este conjunto de teoremas desvelan las
razones por las cuales, en muchos campos de aplicación, se encuentran en todo momento
distribuciones normales, o casi normales.
Un ejemplo típico de este hecho es el caso de los errores de medida. Con respecto a este
tema, Laplace propuso una hipótesis que parece ser plausible. Considera el error total como una
suma de numerosos errores elementales muy pequeños debidos a causas independientes. Es casi
indudable que varias causas independientes o casi independientes contribuyen al error total. Así por
ejemplo, en las observaciones astronómicas, pequeñas variaciones de temperatura, corrientes
irregulares de aire, vibraciones de edificios y hasta el estado de los órganos de los sentidos de un
observador, pueden considerarse como algunas pocas de dichas causas numerosas.
El Teorema Central del Límite es obra de muchos grandes matemáticos. Dentro de la historia
del Teorema Central del Límite Laplace ocupa un lugar fundamental: a pesar de que nunca enunció
formalmente este resultado, ni lo demostró rigurosamente, a él le debemos este importante
descubrimiento. Es por ello que algunos autores lo denominan “Teorema de De Moivre – Laplace”.
Primera definición del teorema:
Sea un conjunto de cualquier número de variables aleatorias independientes (2 o más), las
cuales se modelan, distribuyen o se comportan de manera normal (modelo de Gauss o de
De Moivre), conociendo de cada una de ellas sus parámetros “” y “” (distintos de cero).
Diremos que la sumatoria de este conjunto, también se distribuye normalmente.
Segunda definición del teorema:
Ing. Sergio Aníbal Dopazo Página 111 de 120

Sea “X , X , …, X ” un conjunto de variables aleatorias independientes cualesquiera (es
| 1 2 | n   |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
decir, que no se conoce el modelo o la distribución a la que responden) e idénticamente
distribuidas (o sea que siguen, aunque sea desconocido, el mismo comportamiento o
modelo aleatorio), conociendo de cada una de ellas sus características “” y “” (distintas
de  cero).  La  función “S ” (sumatoria de este conjunto), tiende o se aproxima a  una
n
distribución normal cuando el número de este conjunto “n” tiende a infinito.

|     |     | S   | X  | X X | ...X |     |     |     |
| --- | --- | --- | --- | ----- | ------ | --- | --- | --- |
|     |     | n   | 1   | 2 3   |        | n   |     |     |

Siendo:
|     |     | E  | S   |     |   | ...      |     |     |
| --- | --- | --- | ------ | ------- | --- | ----------- | --- | --- |
|     |     |     | n      | Sn X1   | X2  | X3          | Xn  |     |
|     |     | VS |      | 2  2 | 2 | 2 ...2 |     |     |
|     |     |     | n      | Sn X1   | X2  | X3          | Xn  |     |

Entonces:
|     |     |     | S |            |    |         | S  |      |
| --- | --- | --- | --- | ------------- | --- | ------- | --- | ------- |
|     |     |     |   | n Sn Slím |    | FS |     | n Sn   |
|     |     | lím | P  |               |     |         |     |         |
|     |     |     |    |              |     |         |    |        |
|     |     | n |   |             |    | n     |    |       |
|     |     |     |    | Sn            |    |         |     | Sn      |

|                   | S  |   |      |                                    |     |     |     |     |
| ----------------- | --- | --- | ----- | ---------------------------------- | --- | --- | --- | --- |
| Afirmando que lím |    | n   | Sn  | Z (distribución normal estándar).  |     |     |     |     |
|                   |    |     |      |                                    |     |     |     |     |
n 
|     |    | Sn  |    |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Por ello es un teorema límite, a medida que el número de variables aleatorias crece, esta
agrupación se acercará cada vez más a una distribución normal.

  Quizás, poco importe como se modela o distribuye la venta diaria de un determinado producto
en una empresa, ya que la venta mensual del mismo es aproximadamente normal. Y mucho más
aproximada a la normal, es la venta anual de este producto.

  En la práctica, la tendencia a la distribución normal es veloz, esto quiere decir que no es
necesaria una agrupación de infinitas de variables aleatorias para poder usar este modelo sin ningún
tipo de  remordimientos. Algunos autores hablan  o  mencionan  que el valor de “n”  debe ser  lo
suficientemente grande, pero esto es una cuestión relativa: depende del tipo de distribución o modelo
que sigue la variable aleatoria “x”. Si ésta es parecida a la Normal, será suficiente con un valor de
“n” pequeño, pero si el comportamiento es muy diferente, puede ser necesario un valor de “n”
grande. Por ejemplo si “x” tiene un comportamiento según un modelo Uniforme, alcanza con un valor
de “n = 10” para que la suma “S ” sea de comportamiento Normal. Si “x” tiene un comportamiento
n
según el modelo Exponencial, sería necesario un valor de “n” por lo menos de 25 sumandos para
llegar a la Normalidad. En los casos más desfavorables, puede alcanzar con 30 o 40 sumandos. Más

específicamente, si la variable “x” tiene un dominio positivo, la relación  Sn  deberá ser inferior al

Sn
20% para que la función “S ” sea considerada aproximadamente Normal. Existen casos patológicos,
n
en los cuales no se alcanza la Normalidad ni siquiera con millones de sumandos.

  Las propiedades principales del Teorema son:

  El  teorema  central del límite  garantiza  una  distribución  normal  cuando  “n”  es
suficientemente grande.

Página 112 de 120  Ing. Sergio Aníbal Dopazo

“Estadística General” Teorema Central del Límite (Suma de Variables Aleatorias)
 Existen diferentes versiones del teorema, en función de las condiciones utilizadas
para asegurar la convergencia. Una de las más simples establece que es suficiente
que las variables que se suman sean independientes, idénticamente distribuidas,
con valor esperado y varianza finitas.
 La aproximación entre las dos distribuciones es, en general, mayor en el centro de
las mismas que en sus extremos o colas, motivo por el cual se prefiere el nombre
"teorema central del límite" ("central" califica al límite, más que al teorema).
 Este teorema, perteneciente a la teoría de la probabilidad, encuentra aplicación en
muchos campos relacionados, tales como la inferencia estadística y la
aproximación de las distribuciones de probabilidad.
El teorema de Moivre-Laplace es una aproximación normal a la distribución binomial. Se trata
de un caso particular del Teorema central del límite. Establece que la distribución binomial del número
de éxitos en “n” pruebas independientes de Bernoulli con probabilidad de éxito “p” en cada intento
es, aproximadamente, una distribución normal, si “n” es suficientemente grande y se satisfacen
determinadas condiciones. El teorema apareció por primera vez en la segunda edición de The
Doctrine of Chances, de Abraham de Moivre (ver referencia biográfica en el capítulo de cálculo de
probabilidades), publicado en 1738. Los "ensayos de Bernoulli" no se llamaron así en ese libro, pero
De Moivre escribió lo suficiente sobre la distribución de probabilidad del número de veces que
aparecía "cara" cuando se lanzaba una moneda 1800 veces. Luego este teorema fue ampliado y
completado por Laplace (ver referencia biográfica en el capítulo de cálculo de probabilidades).
Markov fue el primero en intentar demostrar la aplicación del “teorema central del límite” en
variables aleatorias dependientes, en este sentido su trabajo dio origen al teorema de las
denominadas “Cadenas de Markov”.
NOTA RECORDATORIA:
Para este tema será importante recordar las propiedades matemáticas de la Esperanza
matemática y de la Varianza de una Variable Aleatoria (tema visto en los capítulos correspondientes
al tratamiento general de las variables aleatorias discretas y continuas respectivamente).
Sean “x” e “y” dos variables aleatorias independientes de las cuales se conocen su
esperanza matemática y su desvío estándar, y, además tenemos, “a” y “b” dos
constantes se demuestran las siguientes propiedades en la combinación algebraica de
dichos elementos. O sea que se puede formar una nueva variable aleatoria “R” como
sigue:
R  ax  yb, entonces se puede demostrar que las expresiones de la esperanza
matemática y de la varianza de esta nueva variable aleatoria son, respectivamente:
ER   a  b y VR 2  a2 2 2
R x y R x y
O bien: R  xy, entonces la esperanza matemática y la varianza son:
ER     y V  R   2  2 2 2 2 2 2
R x y R x y x y x y
Ing. Sergio Aníbal Dopazo Página 113 de 120

Página 114 de 120 Ing. Sergio Aníbal Dopazo

“Estadística General”  Aproximaciones de los Modelos de Probabilidad

RELACIONES EXACTAS ENTRE MODELOS:

A. DEL MODELO BINOMIAL:

|    | P (r | / n;p)P |     | (nr / | n;1p)  |     |     |     |     |     |     |     |
| --- | ---- | -------- | --- | ------ | ------- | --- | --- | --- | --- | --- | --- | --- |
|     | b    |          | b   |        |         |     |     |     |     |     |     |     |

|    | F (r | / n;p)G |     | (nr | / n;1p)  |     |     |     |     |     |     |     |
| --- | ---- | -------- | --- | ---- | --------- | --- | --- | --- | --- | --- | --- | --- |
|     | b    |          | b   |      |           |     |     |     |     |     |     |     |

|    | G (r | / n;p)F |     | (nr | / n;1p)  |     |     |     |     |     |     |     |
| --- | ---- | -------- | --- | ---- | --------- | --- | --- | --- | --- | --- | --- | --- |
|     | b    |          | b   |      |           |     |     |     |     |     |     |     |

CON EL MODELO BETA

|     |      |          |     | xp |         |     | bnrF | x1p |     |         | br1  |     |
| --- | ---- | -------- | --- | ---- | ------- | --- | -------- | ------ | --- | ------- | ------- | --- |
|    | F (r | / n;p)G |     |      | / ar1 |     | ;        |        |     | / anr | ;       |     |
|     | b    |          |    |      |         |     |          |       |     |         |         |     |

F (x / a;b)G r a / nab1 ; p xF r b1 / nab1 ; p1x
|    |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |    |     |     | b   |     |     |     |    |     |     |     |     |

CON EL MODELO F de FISHER – SNEDECOR

|     |      |          |     |  r1 | 1   |     |            |     |        |    |     |     |
| --- | ---- | -------- | --- | ----- | ---- | ---- | ---------- | --- | ------ | --- | --- | --- |
|    | F (r | / n;p)F |     |  F  |    | 1  |  2n2r; |     | 2r2 |     |     |     |
|     | b    |          | F   | nr   |  p |     | 1          | 2   |        |     |     |     |
|     |      |          |     |      |      |     |            |     |        |    |     |     |

B. DEL MODELO HIPERGEOMÉTRICO

P (r / n;N;R)P (r / R ;N;n)P (Rr / Nn;N;R)P (nr / n;N;NR)
|    |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | h   |     |     | h   |     |     | h   |     |     | h   |     |     |

|     | P (r | / n;N;R)P |     | (rNRn |     | /   | Nn;N;NR) |     |     |     |     |     |
| --- | ---- | ---------- | --- | -------- | --- | --- | ---------- | --- | --- | --- | --- | --- |
|    | h    |            |     | h        |     |     |            |     |     |     |     |     |

F (r / n;N;R)F (r / R ;N;n)G (Rr / Nn;N;R)G (nr / n;N;NR)
|    | h   |     |     | h   |     |     | h   |     |     | h   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

|     | F (r | / n;N;R)F |     | (rNRn |     | /   | Nn;N;NR) |     |     |     |     |     |
| --- | ---- | ---------- | --- | -------- | --- | --- | ---------- | --- | --- | --- | --- | --- |
|    |      |            |     |          |     |     |            |     |     |     |     |     |
|     | h    |            |     | h        |     |     |            |     |     |     |     |     |

C. DEL MODELO de POISSON

CON EL MODELO GAMMA Y EL MODELO CHI – CUADRADO

|     |     |               |     | x | t/r;F |     |  2    |     |      |     |     |     |
| --- | --- | ------------- | --- | --- | -------- | --- | ------- | --- | ----- | --- | --- | --- |
|    | G   | (r / mt)F |     |     |          |     | 2t/ |     | 2r   |     |     |     |
|     | po  |               |     |    |          |     | 2      |     |       |     |     |     |

|     |      |            |     | xt/r1;G |     |     |    |              |     |    |     |     |
| --- | ---- | ---------- | --- | ------------- | --- | --- | --- | ------------ | --- | --- | --- | --- |
|    | F (r | / mt)G |     |               |     |     | 2  | 2t/2r2 |     |     |     |     |
|     | po   |            |     |              |     |     | 2  |              |     |     |     |     |

| Ing. Sergio Aníbal Dopazo  |     |     |     |     |     |     |     |     |     |     | Página 115 de 120  |     |
| -------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------------ | --- |

D. DEL MODELO NORMAL

CON EL MODELO GAMMA Y EL MODELO CHI – CUADRADO

|     |     | 1 1 |    |     |     |  1 1 |    |    |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- |
  (Z)  F x  Z2 r 0,5; 0,5   F 2  Z2  1 , para Z0 (positivo)
|     |     |     |    |     |     |     | 2  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     | 2 2 |     |     |     | 2 2 |     |     |

|     |     | 1 1 |    |     |     |  1 | 1  |    |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
  (Z)   F x  Z2 r  0,5;  0,5   F 2  Z2  1 , para Z0 (negativo)
|     |     | 2 2 |    |     |     | 2   | 2 2 |     |
| --- | --- | --- | --- | --- | --- | --- | ---- | --- |

|     |      |               |     |      |    |     |     |     |
| --- | ---- | ------------- | --- | ----- | --- | --- | --- | --- |
|    | F x | r 0,5;2 |     | 2x | 1  |     |     |     |


E.  DEL MODELO GAMMA

CON EL MODELO NORMAL

|     |      |           |        |      |    |     |     |     |
| --- | ---- | --------- | ------ | ----- | --- | --- | --- | --- |
|    | F x | r0,5 ;  |  2 | 2x | 1  |     |     |     |


APROXIMACIONES DE LOS MODELOS:

A. DEL MODELO HIPERGEOMÉTRICO POR EL MODELO BINOMIAL:

Condiciones: Para tamaños de lote “N” tendiendo a infinito (N) o bien, el tamaño de la
muestra “n” es despreciable respecto del tamaño del lote “N”. Por pruebas experimentales, se
puede  considerar  que  la  muestra  es  despreciable  frente  al  lote cuando  se  cumple  la  siguiente
|     | n   |     |     |     |     | n   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
relación:   0,01, en algunos casos, y, en otros:  0,005. Se tienen las siguientes expresiones de
|     | N   |     |     |     |     | N   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
aproximación:

|     |     |     |    |     |    |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
n;pR
|    | P (r | / n;N;R)P |     | r / |     |     |     |     |
| --- | ---- | ---------- | --- | --- | --- | --- | --- | --- |
|     | h    |            | b   |     | N   |     |     |     |

|     |     |     |    |     |    |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
n;pR
|    | F (r | / n;N;R)F | r   | /   |     |     |     |     |
| --- | ---- | ---------- | --- | --- | --- | --- | --- | --- |
|     | h    |            | b   |     | N   |     |     |     |

|     |     |     |     |    |     |    |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
n;pR
|    | G (r | / n;N;R)G |     | r / |     |     |     |     |
| --- | ---- | ---------- | --- | --- | --- | --- | --- | --- |
|     | h    |            | b   |     | N   |     |     |     |

| Página 116 de 120  |     |     |     |     |     |     |     | Ing. Sergio Aníbal Dopazo  |
| ------------------ | --- | --- | --- | --- | --- | --- | --- | -------------------------- |

“Estadística General”  Aproximaciones de los Modelos de Probabilidad

|      |               |    | 2Rr    |                         |     |
| ---- | ------------- | --- | -------- | ------------------------ | --- |
|   F | (r / n;N;R)F | r  | / n;p   | , aproximación de Wise  |     |
| h    |               | b  | 2Nn1 |                          |     |

B. DEL MODELO BINOMIAL POR EL MODELO NORMAL:

|     | np |     |   |     |     |
| --- | ------ | --- | --- | --- | --- |
Condición:  10  y  n(1p) 10, se debe cumplir simultáneamente. Se tienen las
siguientes expresiones:

|      |         | r0,5np | r0,5np  |     |     |
| ---- | ------- | ---------- | ----------- | --- | --- |
|      | n;p) |            |         |    |     |
|   P | (r /    |            |             |     |     |
| b    |         |           |           |    |     |
|      |         |  np(1p)  |   np(1p) |    |     |

r0,5np
|      | n;p) |           |    |     |     |
| ---- | ------- | --------- | --- | --- | --- |
|   F | (r /    |           |     |     |     |
| b    |         |          |    |     |     |
|      |         |  np(1p) |    |     |     |

r0,5np
|      | n;p)1 |     |          |     |     |
| ---- | --------- | --- | --------- | --- | --- |
|   G | (r /      |     |           |     |     |
| b    |           |    |          |     |     |
|      |           |    | np(1p)  |     |     |

C. DEL MODELO BINOMIAL POR EL MODELO DE POISSON:

Condición p0,005. Se tienen las siguientes expresiones:

|   P | (r / n;p)P | (r / mnp)  |     |     |     |
| ---- | ----------- | ----------- | --- | --- | --- |
| b    |             | po          |     |     |     |

|   F | (r / n;p)F | (r / mnp)  |     |     |     |
| ---- | ----------- | ----------- | --- | --- | --- |
| b    |             | po          |     |     |     |

|    |             |      | mnp)  |     |     |
| --- | ----------- | ---- | ------ | --- | --- |
| G   | (r / n;p)G | (r / |        |     |     |
| b   |             | po   |        |     |     |

D. DEL MODELO BINOMIAL POR EL CRITERIO DE MERMOZ:

Este criterio se aplica cuando se cumplen, simultáneamente, las condiciones de aproximación
por el modelo normal y por el modelo de Poisson, o bien, cuando no se cumplen ninguna de las
condiciones de aproximación anteriores. Hay que tener en cuenta que cuando el valor de “n” y de
“p” son de un valor considerable, a veces el criterio indica que hay que usar la aproximación por el
modelo de Poisson cuando esto no es correcto. Se tiene la siguiente expresión:

| 0,23(1p)2 |     |          |               | 0,23p2  |        |
| ----------- | --- | -------- | ------------- | -------- | ------ |
| n          |     | , para p |  0,5, y, n  | , para p |  0,5  |
| o           | p3  |          | o             | 1p3   |        |

  Si se cumple que: n n se utiliza el modelo de Poisson como aproximación.
o
  Si se cumple que: n n se utiliza el modelo Normal como aproximación.
o
Ing. Sergio Aníbal Dopazo  Página 117 de 120

E. DEL MODELO BINOMIAL POR FISHER
   
 F (r / n;p) (1p)(4r3)  p(4n4r1) , para 0,1p0,9
b
F. DEL MODELO BINOMIAL POR PAULSON
 1 
r1 1  3  1   1 
    1    3  3 
nr p   3(r1)  3(nr)
 F (r / n;p) 
b
 1  1  r11  2 3 
   

 1

 
  nr r1 nrp   
G. DEL MODELO BINOMIAL POR WISE
 
 F (r /n;p) Z , donde “Z” se calcula según:
b
 Para n 2r 1, tenemos:
 1   r1   3r2 4r   1 3
Z3 r1 

1 9r9

3
 

6
  ln1p 

6n3r 6n3r
 

 Para n 2r1, tenemos:
1
  nr    nr1    3n3r1  3  1 
Z3   lnp   3nr1    3 nr  1  
  6  3 nr1    9 nr 
H. DEL MODELO DE POISSON POR EL MODELO NORMAL:
Condición: m 15. Se tienen las siguientes expresiones:
r0,5m r0,5m
 P (r / m)  
po   m     m  
r0,5m
 F (r / m) 
po   m  
Página 118 de 120 Ing. Sergio Aníbal Dopazo

“Estadística General”  Aproximaciones de los Modelos de Probabilidad

r0,5m
|   G | (r / m)1 |    |     |    |     |     |
| ---- | ------------ | --- | --- | ---- | --- | --- |
po
|     |     |    | m   |    |     |     |
| --- | --- | --- | --- | --- | --- | --- |

r1m
|   F | (r / m) |       |    |     |     |     |
| ---- | ---------- | ----- | --- | --- | --- | --- |
| po   |            |      |    |     |     |     |
|      |            |  r1 |    |     |     |     |

|     |     |   |   |   |     |     |
| --- | --- | --- | --- | --- | --- | --- |
  F (r / m) 4r3  2 m , para r 10, aproximación de Fisher
po

|     |     |    |    |     |     | 1     |
| --- | --- | --- | --- | --- | --- | ------- |
|     |     |    |     | 1   |    | m  3  |
  F (r / m)3 r11   , aproximación de Wilson–Hilferty
po
|     |     |    |    | 9(r1) | r1 |   |
| --- | --- | --- | --- | ------- | ----- | ---- |
|     |     |    |    |         |       |     |

I.  DEL MODELO GAMMA POR EL MODELO NORMAL:

|     |     |    |      | 1   |   |     |
| --- | --- | --- | ----- | --- | --- | --- |
|     |     |    | x | 3   | 1   |    |
  F (x / r ;)3 r    1, aproximación de Wilson–Hilferty

|     |     |    |   | r  | 9r   |     |
| --- | --- | --- | --- | --- | ------- | --- |
|     |     |    |    |     |         |    |

x0,5r
|   F (x | / r ;) |     |     | , para x15  |     |     |
| ------- | ---------- | --- | --- | ----------------- | --- | --- |
|         |            |    |     |                  |     |     |
|        |            |    | x |                  |     |     |

xr
|   F (x | / r ;) |     | , para r | 25  |     |     |
| ------- | ---------- | --- | --------- | ---- | --- | --- |
|         |            |    |          |      |     |     |
|        |            |     | r         |      |     |     |
|         |            |    |          |      |     |     |

|     |     |   |    |    |   |     |
| --- | --- | --- | --- | --- | --- | --- |
  F (x / r;) 2 x  4r1 , para r 10, aproximación de Fisher


|     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
Ing. Sergio Aníbal Dopazo  Página 119 de 120

Página 120 de 120 Ing. Sergio Aníbal Dopazo