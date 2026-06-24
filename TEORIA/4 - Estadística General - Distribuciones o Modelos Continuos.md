“Estadística General” Variables Aleatorias Continuas – Modelos de Probabilidad
VARIABLES ALEATORIAS CONTINUAS
Una variable aleatoria “x”, es continua si sus valores consisten en uno o más intervalos de la
recta de los reales. Es continua, si puede tomar cualquier valor numérico en un intervalo o conjuntos
de intervalos. En general, todos los resultados experimentales que se basan en escalas de medición
(tiempo, peso, distancia, temperatura, etc.), son variables aleatorias continuas. Resumiendo, diremos
que una variable aleatoria es continua si su conjunto de posibles valores es todo un intervalo de
 
números, esto es, si para algún intervalo A;B (siendo AB), cualquier número “x” entre “A” y
“B” es posible. La escala de medición de “x” se puede subdividir en cualquier grado deseado.
Si bien el campo de variación real de la variable aleatoria continua puede ser un intervalo
finito, se considera usualmente que el mismo es todo el campo real, es decir  x, debido a
que en realidad no se puede precisar con exactitud los límites del dominio de dicha variable aleatoria.
A diferencia de las variables aleatorias discretas, a las continuas es imposible asignar un valor
de probabilidad a cada valor puntual del dominio de la variable. La probabilidad de que la variable
aleatoria continua tome un valor determinado, solo puede ser distinta de cero para un número finito o
infinito pero numerable de valores, pero no para todos los posibles, pues las probabilidades de los
mismos no podría sumar 1. La mayor parte de las variables continuas que encontramos en la
práctica, son tales que cada valor posible específico tiene probabilidad nula, estando las
probabilidades asociadas realmente a intervalos de valores y no a valores aislados. A este tipo de
variables se denominan variables absolutamente continuas o simplemente continuas.
Dada su característica de que las probabilidades están asociadas a intervalos de valores,
aparece como natural comenzar a definir conceptos relacionados con la función de densidad de
probabilidad.
La función de distribución de probabilidad de una variable aleatoria continua “x” está
caracterizada por una función “f(x)” que recibe el nombre de función de densidad de probabilidad.
Esta función “f(x)”, que no es la misma función de probabilidad de las variables aleatorias discretas,
proporciona un medio para determinar la probabilidad de ocurrencia de un intervalo de la variable
aleatoria (AxB), ya que la probabilidad asociada a cada valor de “x”, que toma la variable
aleatoria, vale cero, cualquiera sea el valor “x”. Desde un punto matemático, esta función de
densidad de probabilidad, se puede interpretar como la derivada de la función de distribución de
probabilidad.
La gráfica de la función de densidad de probabilidad es una curva bajo la cual queda
 
encerrada un área que representa al espacio muestral de ocurrencia. Cada intervalo A;B secciona
una porción de este espacio muestral. Dicho de otro modo esta función modela el comportamiento de
la frecuencia relativa de ocurrencia de los infinitos valores que puede tomar la variable aleatoria.
Ing. Sergio Aníbal Dopazo Página 61 de 120

Resumiendo el concepto, diremos que la función de densidad de probabilidad es una
función “f(x)” tal que se cumplan las siguientes condiciones:
 La función es cero fuera del dominio de definición de la variable aleatoria “x”.
 La función es positiva en el dominio definido: f(x)0, x.
 Como la función encierra al espacio muestral de observación, el área bajo la curva de la

función debe ser igual a 1: f(x)dx 1.

 Como el área total bajo la “f(x)” es igual a 1, la probabilidad del intervalo AxB es el
área acotada por la función de densidad y las rectas xA y xB. Esta área define la
probabilidad de que la variable aleatoria “x” tome valores entre “A” y “B”, o sea que
B
calcula la siguiente probabilidad: P(Ar B) f(x)dx.
A
Así como en el procesamiento de datos, para algunas aplicaciones en general, se utilizan las
Frecuencias Acumuladas; en variables aleatorias se utilizan probabilidades acumuladas, por lo que
es conveniente definir a las Funciones de Distribución de Probabilidad.
x
 Función de Distribución: FxP(VA  x)  f(x)dx, al igual que en el caso de las

variables aleatorias discretas, esta función calcula la probabilidad de que la variable
aleatoria en cuestión tome un valor específico menor o igual que “x”. En muchos casos
Página 62 de 120 Ing. Sergio Aníbal Dopazo

“Estadística General” Variables Aleatorias Continuas – Modelos de Probabilidad

también se utiliza: GxP(VA  x) f(x)dx, la cual calcula la probabilidad de que la
x
variable aleatoria en cuestión tome un valor específico mayor o igual que “x”. Por lo que a
la primera se la denomina función de probabilidades acumuladas izquierda y a la
segunda función de probabilidades acumuladas derecha. La función de distribución de
probabilidad acumulada izquierda “F(x)”, es una función creciente de los valores de la
variable aleatoria con las siguientes propiedades:
 Fx0, para todo el dominio de la variable  x ;
 F  x  F  x , si x x ;
1 2 1 2
 lím  Fx F 0;
x
 lím  Fx F1;
x
dFx dGx
   fx; la derivada de la función de distribución es la función de
dx dx
densidad de probabilidad como consecuencia del teorema fundamental del
cálculo integral.
De manera que podemos definir las siguientes relaciones funcionales:
 Se cumple que: F(x)G(x)1
 F(x)1G(x) y G(x)1F(x)
Por lo tanto se puede deducir que:
B
 P(A  x B) f(x)dx F(B)F(A) G(A)G(B)
A
A partir del concepto de la función de distribución de probabilidad acumulada
izquierda, demostraremos que la probabilidad asociada a un valor específico de la
variable aleatoria continua es cero. Esto se debe a la continuidad de la función “F(x)”.
Si “a” y “b” son valores mayores que cero, entonces es válida la siguiente expresión:
 0PVAx Pxaxxb
, entonces:
Ing. Sergio Aníbal Dopazo Página 63 de 120

0PVAx

 Fxb Fx

 Fx Fxa
, y como la función “F(x)” es continua, se
puede definir que:
 Fxb Fx 0 si b0, y  Fxa Fx 0 si a0.
Entonces queda demostrado que: Px PVAx 0
Salvo puntos de discontinuidad de la función de distribución “F(x)”, carece de sentido
discernir si la misma incluye o no el valor de “x”, ya que se demostró que la probabilidad puntual es
nula, razón por la cual sería lo mismo definirla como:
Fx PVAx PVAx
y
Gx PVAx PVAx
, esto lo podemos expresar en el
siguiente ejemplo:
Supongamos que estamos estudiando a una variable aleatoria continua y quisiéramos calcular
la probabilidad de que la misma tome un valor menor que 10, o sea la
Px10 F10 
; por lo
que hay que ubicar (siguiendo el razonamiento de las variables aleatorias discretas) el valor
 
inmediatamente inferior a 10, que es 10 . Análogamente, si quisiéramos calcular la probabilidad
   
de que la misma tome un valor mayor que 10, o sea la P x10 G10 ; por lo que hay que
ubicar (siguiendo el razonamiento de las variables aleatorias discretas) el valor inmediatamente
mayor a 10, que es 10  , siendo “” un valor incremental que tiende a cero. Tal como lo podemos
visualizar de manera exagerada en el siguiente esquema de una escala numérica:
Para hallar los correspondientes valores de forma matemática debemos resolver las siguientes
ecuaciones:
lím1010 y lím1010, de manera que, para las variables aleatorias continuas,
0 0
tenemos (para el ejemplo) que el valor inmediatamente inferior a 10 es 10; y el valor inmediatamente
superior a 10 es 10.
Para algunos lectores estos conceptos pueden parecer algo chocantes. Pero es importante
tratar de comprender que el continuo, con todas sus propiedades, es sólo un modelo matemático,
esto es, que el continuo no existe en la naturaleza, la cual podríamos definirla como esencialmente
discreta de acuerdo a su observación. El proceso de obtener valores de una variable continua es la
medición de la misma mediante un instrumento. No existe un instrumento de medición que arroje
valores continuos, por ejemplo un instrumento digital, nos arrojará resultados discretos de la variable,
a pesar de la continuidad teórica de la misma.
Página 64 de 120 Ing. Sergio Aníbal Dopazo

“Estadística General” Variables Aleatorias Continuas – Modelos de Probabilidad
PARÁMETROS y CARACTERÍSTICAS de las VARIABLES CONTINUAS
Al igual que en el procesamiento de datos y en el estudio de las variables aleatorias discretas,
se pueden definir los denominados valores característicos. Los cuales serán definidos a partir del
siguiente ejemplo:
Ejemplo: Supongamos una variable aleatoria continua cuya función de densidad de
probabilidad es: fx0,02xe  0,01x2 y su dominio es x0. La gráfica de
dicha función es la siguiente:
Ing. Sergio Aníbal Dopazo Página 65 de 120
8
Valores característicos:
 Moda o Modo: Mo x ; es el valor de la variable aleatoria cuya densidad de probabilidad
o
es máxima. De manera que dicho valor maximiza la función de densidad
 f  x  hay un Máximo local. Para hallar la moda en el ejemplo debemos derivar la
o
función, igualarla a cero y encontrar el valor de variable que satisface dicha condición:
fx df(x)  1 e  0,01x2  1 e  0,01x2 0, entonces el valor que satisface la
dx 50 2.500
igualdad es x Mo7,071068.
o
 Mediana: Me x ; es el valor de la variable aleatoria tal que se cumplan las siguientes
e
condiciones: F  x   G  x   0,5. Para hallar la mediana en el ejemplo, primero hay que
e e
hallar la función de distribución “G(x)”, igualarla a “0,5” y encontrar el valor de variable
que satisface dicha condición:
Gx   0,02xe  0,01x2 dx e  0,01x2 0,5, resolviendo la ecuación tenemos:
x
ln0,5
x   x Me8,325546
e 0,01 e
 Fractiles: x . Son valores que representan a un porcentaje de los valores posibles de

una variable aleatoria. Es el valor de la variable aleatoria cuya probabilidad de estar por

debajo del mismo es igual a “”, o sea que encierra al % de los valores a su izquierda.
Su cálculo es muy parecido al de la mediana (que es el fractil del 50%, ya que la
probabilidad de estar por debajo de ella vale “0,50”). Se calculan teniendo en cuenta la
 
siguiente condición: F x  .


 Esperanza Matemática o Valor Medio: E(x)  xf(x)dx; (suele denominarse

valor esperado de la variable o MEDIA), es el valor que toma el promedio de la variable
aleatoria después de infinitas observaciones. En el estudio de las funciones teóricas de
probabilidad, el valor medio es, generalmente, el parámetro más importante. Si de un
proceso aleatorio se extrae una muestra, el promedio de la misma es una medida
experimental de la esperanza matemática de la variable aleatoria, en la misma forma en
que la frecuencia relativa lo es de la probabilidad. En el ejemplo:
Ex    0,02x2 e  0,01x2 dx8,862269
0
 
 
 Varianza: V(r) 2  x2 f(x)dx 2 ; es el valor esperado del cuadrado de las
 

desviaciones de la variable aleatoria respecto a su esperanza matemática. Mide la
aleatoriedad misma de la variable, porque nos indica cuan dispersa puede ser la
distribución. En el ejemplo:
Vx2      0,02x3 e  0,01x2 dx  8,8622692 21,460184
 
0
Al igual que en las variables aleatorias discretas, se cumplen las propiedades matemáticas
de la Esperanza Matemática y de la Varianza enunciadas.
 Desvío Standard: D(r)  2 ; (Desvío Estándar, Desvío Típico o Dispersión), es el
valor que mide la dispersión de los valores que toma la variable respecto a la esperanza
matemática. En el ejemplo:
D(r)   21,460184  4,632514.

 Coeficiente de Variación: Cv 100; (o Dispersión Relativa) expresado en forma

porcentual, con el mismo concepto visto en las características de las variables aleatorias
discretas. Cabe destacar que esta característica es muy importante en las variables
aleatorias continuas. En el ejemplo:
4,632514
Cv 10052,27%.
8,862269
  x3 f(x)dx
 Coeficiente de Asimetría: As   ; (es una característica de
3 3
forma), con el mismo concepto visto en las características de las variables aleatorias
discretas. En el ejemplo:
Página 66 de 120 Ing. Sergio Aníbal Dopazo

“Estadística General” Variables Aleatorias Continuas – Modelos de Probabilidad
0,062742
  0,6311. Con asimetría positiva o derecha, como se puede observar en el
3 0,099415
gráfico correspondiente. Se puede observar que se cumple: Mo  Me  .
Cabe recordar que las variables de comportamiento simétrico, este coeficiente es nulo y
los tres valores de tendencia central coinciden: Mo  Me  ; en cambio en las de
comportamiento asimétrico positivo, este coeficiente es mayor que cero y los tres valores
de tendencia central difieren: Mo Me  , y en las de comportamiento asimétrico
negativo, este coeficiente es menor que cero y los tres valores de tendencia central
difieren:   Me  Mo. Como hemos visto en el desarrollo de las variables aleatorias
discretas, debemos señalar que el hecho que este coeficiente sea nulo, no implica
necesariamente que la distribución sea simétrica y puede no cumplirse la propiedad.
Veremos las gráficas correspondientes a estos comportamientos:
Ing. Sergio Aníbal Dopazo Página 67 de 120

  x4 f(x)dx
 Coeficiente de Kurtosis: Ku   ; (o Coeficiente de Aplastamiento
4 4
o de Agudeza) es una característica de forma, con el mismo concepto visto en las
características de las variables aleatorias discretas. En el ejemplo:
0,149449
  3,2451. Es una variable con distribución leptocúrtica (aguda).
4 0,046054
Generalizando para cualquier variable aleatoria continua, la kurtosis de una variable se
utiliza para comparar agudeza o aplastamiento entre distribuciones. Si es mayor que la de
otra, se dice que la variable primera es más puntiaguda (o aguda) que la otra. Se puede
observar en los siguientes gráficos, que la “variable 1” es más aguda que la “variable 2”;
o bien que la “variable 2” es más aplastada que la “variable 1”.
Si   3, la distribución de probabilidad presenta un pico relativamente alto y recibe el
4
nombre de distribución leptocúrtica; si   3, la distribución es relativamente plana y recibe
4
el nombre de distribución platicúrtica, y si   3, la distribución no presenta un pico muy
4
alto ni muy bajo y recibe el nombre de distribución mesocúrtica. El valor “3” se emplea como
una referencia debido a que en la práctica la kurtosis de una distribución suele compararse
con la kurtosis de una distribución o modelo conocido como normal, cuyo valor es “3”. La
distribución normal se desarrollará más adelante.
Página 68 de 120 Ing. Sergio Aníbal Dopazo

“Estadística General” Variables Aleatorias Continuas – Modelos de Probabilidad
EXPECTATIVA PARCIAL
Tal como vimos en el estudio de las variables aleatorias discretas, este concepto es útil en
muchos problemas prácticos, especialmente aquellos problemas de decisión en que aparecen costos
o ganancias con un número finitos de discontinuidades.
Habíamos definido a la esperanza matemática (que denominaremos TOTAL, porque tiene en
cuenta a todo el dominio de la variable) como:

 Esperanza Matemática Total: E(x)  xf(x)dx.

Al igual que en el estudio de las variables aleatorias discretas, las expectativas parciales se
pueden interpretar como una parte de la esperanza matemática, de modo que a la misma la podemos
dividir en partes. Entonces definimos:
x
 Expectativa Parcial Izquierda: H(x) xf(x)dx. Hacemos el cálculo tomando en cuenta

los valores de la variable aleatoria menores o iguales que el valor “x” en cuestión (o sea a
la izquierda de “x”).

 Expectativa Parcial Derecha: J(x) xf(x)dx. Hacemos el cálculo tomando en cuenta
x
los valores de la variable aleatoria mayores o iguales que el valor “x” en cuestión (o sea a
la derecha de “x”).
Como la integral es un operador matemático lineal tenemos:
x 
xfxdx xfxdx   Ex
 x
Observemos que la primer sumatoria corresponde a la expectativa parcial izquierda de los
valores de la variable aleatoria menores o iguales que “x”; y la segunda sumatoria corresponde a la
expectativa parcial derecha de los valores de la variable aleatoria mayores o iguales que “x”. De
manera que podemos deducir lo siguiente:
 
 E x H(x)J(x), se demuestra que una expectativa se puede obtener a partir de la
otra.
Si quisiéramos obtener la expectativa en un intervalo de la variable, la expresión es:
B
 Expectativa Parcial en un rango: EA  x B xfxdx. Tomando en cuenta los
A
valores de la variable aleatoria comprendidos entre “A” y “B”. Siendo estos
pertenecientes al dominio de la variable aleatoria “x” en cuestión. También se puede
calcular mediante EAxB H(B)H(A)J(A)J(B).
Ing. Sergio Aníbal Dopazo Página 69 de 120

ESPERANZA MATEMÁTICA TRUNCADA (o PROMEDIOS TRUNCADOS)
Una aplicación sencilla, práctica e intuitiva de las expectativas parciales es el cálculo de los
promedios truncados. El procedimiento denominado truncamiento de la variable aleatoria,
consiste en eliminar un intervalo de su dominio; por lo tanto el promedio obtenido solamente refiere a
una parte de los valores observados descartando al resto de los otros valores obtenidos. El cálculo de
estos promedios se denota por medio de las siguientes expresiones:
H(x)
 Promedio Truncado Izquierdo:   ; realizamos un truncamiento a la izquierda
T(VAx) F(x)
(eliminamos valores de la variable aleatoria mayores que el valor “x”). O sea que
tomamos en cuenta solamente los valores de la variable aleatoria menores o iguales que
el valor “x”.
J(x)
 Promedio Truncado Derecho:   ; realizamos un truncamiento a la derecha
T(VAx) G(x)
(eliminamos valores de la variable aleatoria menores que el valor “x”). O sea que
tomamos en cuenta solamente los valores de la variable aleatoria mayores o iguales que el
valor “x”.
H(B)H(A) J(A)J(B)
 Promedio Truncado a dos Colas:    ; realizamos un
T(AxB) F(B)F(A) G(A)G(B)
truncamiento a la izquierda y a la derecha (eliminamos valores de la variable aleatoria
menores que “A” y mayores que “B”). O sea que tomamos en cuenta solamente los
valores de la variable aleatoria comprendidos en un rango del valor “x”. También se puede
EA xB
calcular mediante la siguiente expresión:   .
T(AxB) P(A xB)
Los ejemplos y aplicaciones de estos conceptos, los veremos en el desarrollo de cada uno de
los modelos correspondientes.
Página 70 de 120 Ing. Sergio Aníbal Dopazo

“Estadística General” Variables Aleatorias Continuas – Modelos de Probabilidad
MODELOS (o DISTRIBUCIONES de PROBABILIDAD) de VARIABLES ALEATORIAS CONTINUAS
Para estudiar los modelos correspondientes a las variables aleatorias continuas, primero es
indispensable reconocer a la Variable Aleatoria objeto de estudio, y luego definir el Modelo más
adecuado a usar. Se reconocen en la naturaleza, una cantidad importante de modelos aplicados a
distintos tipos de variables aleatorias continuas, que fueron desarrollados de manera empírica. Es por
ello que para algunas aplicaciones en particular, se encuentren solapamientos en la aplicación de los
mismos. La elección del mejor modelo, se hace difícil en la práctica. Es por eso que la experiencia
profesional ayuda en la selección. No obstante veremos en el desarrollo de los modelos, algunos
aspectos orientativos para su selección, como ser: la historia del desarrollo y uso del modelo, el
coeficiente de variación del modelo, su forma, etc.
Debemos recalcar que en el desarrollo de cada modelo toman relevancia los parámetros del
mismo, los cuales podemos clasificar en tres tipos. En todos los modelos no siempre se encuentran
los tres tipos de parámetros:
 Parámetro de corrimiento, se denomina al parámetro que afecta a los
momentos ordinarios pero no a los momentos centrados. Un cambio de
valor de un parámetro de corrimiento solo afecta la posición de la
distribución respecto del origen, pero no su dispersión ni su forma.
 Parámetro de escala, se denomina al parámetro que afecta a los
momentos centrados pero no a los momentos centrados adimensionales.
Un cambio de valor de un parámetro de escala modifica la dispersión de la
distribución, pero puede o no modificar la posición respecto del origen, y no
altera su forma.
 Parámetro de forma, se denomina al parámetro que afecta a los momentos
centrados adimensionales (o a algunos de ellos), aunque no
necesariamente a la esperanza matemática y/o a la varianza. Un cambio de
valor de un parámetro de forma altera la forma de la distribución, pero no
siempre su posición o dispersión.
No obstante, en la vida profesional, resulta difícil seleccionar el modelo más adecuado. De
manera que existen procedimientos para la adecuada selección. Estos procedimientos están
desarrollados dentro de la inferencia estadística, tema que escapa a nuestro apunte.
De acuerdo a lo anterior, es indispensable conocer el comportamiento las variables que son
de nuestro interés definiendo un modelo, el cual se encuentra representado por una función de
densidad. Estudiaremos algunos modelos que se emplean con mayor frecuencia en el estudio de
fenómenos aleatorios en las ciencias aplicadas o bien en los negocios y en la economía. En resumen,
modelos que se usan en una amplia gama de situaciones experimentales y en diversos problemas
inherentes a la toma de decisiones.
No hay un orden prestablecido en el desarrollo de los modelos, de manera que el
agrupamiento en el presente capítulo es arbitrario y responde a la experiencia en el campo
profesional y en la enseñanza de estos conceptos.
Ing. Sergio Aníbal Dopazo Página 71 de 120

MODELOS RELACIONADOS con la TEORÍA de la FIABILIDAD (VIDA de ELEMENTOS)
Se define como fiabilidad a la probabilidad de que un elemento, bien, ser viviente, proceso,
sistema o dispositivo realice adecuadamente su función prevista a lo largo del tiempo, cuando opera
en el entorno para el que ha sido diseñado. En cambio la confiabilidad es la capacidad que tiene ese
elemento, bien, ser viviente, proceso, sistema o dispositivo para funcionar en el tiempo establecido
cuando opera en el entorno para el que ha sido diseñado. Resumiendo, la fiabilidad nos indica la
duración o resistencia del elemento, bien, ser viviente, proceso, sistema o dispositivo; en cambio la
confiabilidad es la garantía que doy a ese elemento, bien, ser viviente, proceso, sistema o dispositivo.
La variable aleatoria “x” mide la duración hasta la falla del elemento o bien la resistencia
hasta la rotura. Esta variable también se denomina vida del elemento.
Otras características importantes en este tema son: MTBF (Mean Time Between Failures) o
Tiempo Medio Entre Fallas, y MTTF (Mean Time To Failures) o Tiempo Medio Hasta la Falla. El
MTBF es el tiempo promedio de vida entre ciclos de mantenimiento o bien entre dos fallas
consecutivas, esta característica es la más usada en los estudios de fiabilidad. Este nos indica el
tiempo promedio en que se tiene otra falla después de que ya ocurrió una. El MTTF es el tiempo
promedio hasta la falla, esta característica es la esperanza matemática de la variable aleatoria “x”, la
cual estudia la duración de un elemento hasta la falla. Este nos indica el tiempo promedio en el que
se tiene una falla desde que el elemento se puso en funcionamiento.
Una característica fundamental en la teoría de la fiabilidad es la tasa de falla, “”, la cual no
tiene una interpretación física directa pero es muy importante a lo largo de la vida del producto. Esta
característica en realidad es una función que evoluciona a través del tiempo, por ello suele
denominarse función de tasa de fallas o función de riesgo “(t)”. Esta evolución se puede
visualizar gráficamente en una curva llamada curva de Davies o curva de bañera (como
consecuencia de su forma peculiar), la cual es la base conceptual del estudio de la fiabilidad. En la
curva se pueden definir e identificar claramente, tres zonas o períodos a lo largo de la vida de un
elemento, bien, ser viviente, proceso, sistema o dispositivo.
El primer período se da en el nacimiento o al principio de la vida de los elementos, los más
débiles fallan a una tasa alta como consecuencia de un fenómeno llamado mortalidad infantil; las
fallas se producen inmediatamente o al cabo de muy poco tiempo del nacimiento o puesta en
funcionamiento del elemento. En realidad no se conocen las causas de este fenómeno, se cree que
se produce porque el elemento es débil. Las fallas disminuyen hasta llegar al segundo período. En
general los fabricantes, para evitar esta zona, someten a sus componentes a un quemado inicial.
Este quemado inicial se realiza sometiendo a los elementos a determinadas pruebas y seguimiento
riguroso, si el elemento pasa este período se lo garantiza para su segundo período.
El segundo período llamado de madurez, vida funcional o vida útil, las fallas (si ocurren) se
producen a una tasa constante, en este período las fallas ocurren de manera azarosa. Suele ser el
período de mayor duración, en el que se suelen estudiar los sistemas.
El tercer período llamado de envejecimiento, los supervivientes de los períodos anteriores,
fallan como consecuencia del desgaste, de modo que aumenta la tasa. Corresponde al agotamiento
de los elementos los cuales se consumen o deterioran constantemente durante su funcionamiento.
Aún con reparaciones y mantenimiento exhaustivo, la tasa de falla aumenta, hasta que resulta
demasiado costoso el mantenimiento o bien innecesario o contraproducente.
Aunque existen distintos tipos de curva de bañera, dependiendo del tipo de elemento a
estudiar, representaremos en la siguiente figura, la forma típica y convencional:
Página 72 de 120 Ing. Sergio Aníbal Dopazo

“Estadística General” Variables Aleatorias Continuas – Modelos de Probabilidad
No incurriremos en el estudio de la fiabilidad / confiabilidad, sino que trataremos el problema
desde el punto de vista estadístico. Se desarrollarán los modelos que explican a la variable aleatoria
“x” mencionada y la distribución de probabilidad de dichas fallas. Los modelos más adecuados para
el estudio de este tipo de variable aleatoria son: el “Modelo Exponencial”, el “Modelo de Weibull”,
el “Modelo Gumbel del mínimo”, el “Modelo Gumbel del Máximo” y en algunas aplicaciones
particulares, el “Modelo Log-normal”. También en esta teoría de la fiabilidad / confiabilidad, se
han aplicado (con dudoso éxito) los modelos “Normal” y “Gamma”.
A. MODELO EXPONENCIAL
Este modelo se rige fundamentalmente por el proceso de Poisson, el cual desarrollaremos
particularmente más adelante. Permite modelar el lapso entre dos eventos consecutivos de Poisson
que ocurren de manera independiente, o sea que estudia la duración de elementos que fallan a la
Poisson, es decir que fallan al azar. La variable aleatoria es la extensión de continuo entre fallas
consecutivas de un proceso de Poisson (el mismo se puede estudiar como un caso particular de los
modelos Gamma y de Weibull, que desarrollaremos más adelante).
Es el modelo que se utiliza o bien utilizaba con habitualidad para modelar la fiabilidad, o sea
problemas del tipo tiempo-falla. El mismo es un modelo matemático sencillo de tratar y es adecuado
para modelar el comportamiento de los elementos en el período de vida útil o vida funcional, período
en el cual la tasa de fallas o función de riesgo del elemento, es constante. Si la tasa de falla no es
constante, se debe utilizar al modelo de Weibull, siendo este el modelo más apropiado para estudiar
la duración de los elementos, además recordemos que el modelo Exponencial se puede tratar como
un caso particular del modelo de Weibull.
Debemos aclarar que en el modelo Exponencial, las fallas de los elementos se producen
exclusivamente por el azar, no así, en el modelo de Weibull, donde en las causas de las fallas de los
elementos interviene el desgaste y la fatiga. Resumiendo este modelo es útil para observar el tiempo
de falla de un elemento cuya única causa de falla es el azar como por ejemplo un fusible de luz o de
un chip que no disipa energía.
Tal como ocurre en el proceso de Poisson, que desarrollaremos más adelante, el modelo
Exponencial no tiene memoria. Esta propiedad, carencia de memoria, se explica porque la
probabilidad de ocurrencia de eventos presentes o futuros no depende de los eventos que hayan
ocurrido en el pasado. De esta forma, la probabilidad de que una unidad falle en un lapso específico
Ing. Sergio Aníbal Dopazo Página 73 de 120

depende, nada más, de la duración de este lapso, y no del tiempo en que la unidad ha estado
funcionando o ha estado operando. La probabilidad de que un elemento, que está funcionando, falle
en el próximo instante es independiente de cuánto ha estado funcionando el mismo (se demuestra
que el elemento no presenta síntomas de envejecimiento). Es tan probable que el elemento falle al
principio o al final de su funcionamiento. En cambio, para un elemento que falla por desgaste o fatiga,
la probabilidad de que falle en un lapso específico depende de la cantidad de tiempo en que el
elemento ha estado funcionando u operando.
Se debe aclarar que este modelo también es utilizado en otras aplicaciones, las cuales
desarrollaremos oportunamente. Este modelo estudia problemas de tipo Poissonianos, en donde la
variable aleatoria es el continuo hasta que se produce el primer acontecimiento puntual, y también se
aplica como modelo para el intervalo en problemas de líneas de espera o de atención entre dos
acontecimientos puntuales.
El parámetro del modelo es “” (parámetro de escala), que representa desde el punto de vista
de la fiabilidad la tasa de falla (número medio de fallas por unidad de continuo). Cuando
desarrollemos al proceso de Poisson, explicaremos con más detalle a este parámetro.
 Parámetro del Modelo: “” (de escala).
 Dominio de la Variable Aleatoria: x0.
 Función de densidad de probabilidad: Su expresión es:
f(x)eX
 Gráfica de la función de densidad:
Se cumplen las reglas generales dadas para las variables aleatorias continuas.
 Función de Distribución de Probabilidad: Para este modelo se desarrolla la función de
distribución de probabilidad acumulada derecha.
Página 74 de 120 Ing. Sergio Aníbal Dopazo

“Estadística General” Variables Aleatorias Continuas – Modelos de Probabilidad

P(VAx)G (x/) eX dxeX
EXP
x
 Moda: Mo  0
ln2
 Mediana: Me 

1
 Esperanza Matemática: Ex . Si al modelo lo usamos para la fiabilidad, la

esperanza matemática es “MTTF” y en este modelo por efecto del azar es coincidente con
“MTBF”.
1
 Varianza: Vx 2 
2
1
 
 Coeficiente de Variación: Cv  100  100 100%. En este modelo se puede
 1

observar que el coeficiente de variación es exactamente igual al 100%.
ln1
 Fractiles: x 


  x3 f(x)dx
 Coeficiente de Asimetría: As   2
3 3
  x 4 f(x)dx
 Coeficiente de Kurtosis: Ku   9. Este modelo tiene agudeza
4 4
de tipo leptocúrtica.
1
 Expectativa Parcial Izquierda: H (x/) F (x / 2 ; ), observe el lector que se
EXP  
utiliza, para su cálculo, la función de distribución de probabilidad acumulada izquierda del
modelo Gamma, el cual desarrollaremos más adelante.
Ing. Sergio Aníbal Dopazo Página 75 de 120

B. MODELO de WEIBULL (Wallodi Weibull, 1887 – 1979)
Ernst Hjalmar Waloddi (Wallodi) Weibull (Suecia, 1887 – Annecy, Francia, 1979) fue
un ingeniero mecánico, físico y matemático sueco. Es reconocido por su trabajo en
el área de la fatiga de materiales y en el área de la estadística por sus estudios
sobre la distribución de Weibull. En 1951 publica el tratado sobre la distribución que
lleva su nombre: A statistical distribution function of wide applicability (Una función
de distribución estadística de amplia aplicabilidad).
La distribución de Weibull fue establecida, en 1951, por el físico mencionado quien demostró
que el esfuerzo al que se someten los materiales puede modelarse de manera adecuada mediante el
empleo de esta distribución. Luego se descubrió que este modelo se ajusta mejor a los problemas de
tiempo de vida, sobre todo, si la tasa de falla de los elementos, no permanece constante a causa del
desgaste o fatiga de ellos. Debemos aclarar, que este modelo, no descarta la posibilidad de que la
muerte del elemento en cuestión (que se desgasta con el tiempo) se produzca por el mero azar. Se
tiene en cuenta, en esta distribución, que es más probable que el elemento en cuestión falle a medida
que envejece.
Se trabaja con dos parámetros: “” y “”, el primero se denomina parámetro de escala y el
segundo parámetro de forma. El parámetro “”, en la teoría de la fiabilidad, y, para algunas
aplicaciones, se puede considerar como la inversa de , o sea la inversa de la tasa de falla y se
denomina según la confiabilidad como la vida característica; este parámetro está relacionado con el
MTBF.
El parámetro “”, hace que la función de densidad tome diferentes formas dependiendo del
valor que toma y el modelo tiene diferentes propiedades. Si el parámetro toma el valor “ = 1”, este
es un caso particular donde la distribución de Weibull se resume al modelo Exponencial (donde la
única causa de la falla del elemento es el azar). Si “ < 3,60234943”, tiene una forma con sesgo
positivo o a la derecha (en este caso predominan las causas del azar frente al desgaste o fatiga en la
falla del elemento). Si “ < 1”, la tasa de fallas disminuye con la edad sin llegar a cero, por lo que
podemos suponer que nos encontramos en el nacimiento del elemento, dando lugar a fallas por
tensión de rotura. Si “ > 3,60234943”, la forma es con sesgo negativo o a la izquierda (la causa
predominante es el desgaste o fatiga frente al azar en la falla del elemento). Y, si “ = 3,60234943”,
la distribución tiene una forma simétrica, el coeficiente de asimetría es igual a cero (predominan con
igual intensidad tanto el azar como el desgaste, en la falla del elemento).
Para resumir, este modelo se puede interpretar como una generalización del modelo
Exponencial para contemplar causas más variadas de falla de un elemento. Son ejemplos del uso
habitual de este modelo los problemas relacionados con la fiabilidad de los elementos (cualquiera sea
las causas de sus fallas) y el esfuerzo al que se someten los materiales que causan deformación
irreversible y luego su rotura.
Casos particulares de este modelo son el modelo o distribución de probabilidad de John W.
Rayleigh (el cual no está al alcance de este apunte). Algunos autores consideran que inicialmente el
modelo de Weibull fue descubierto en 1927 por Maurice Fréchet, y otros que Boris Gnedenko llegó a
obtener dicho modelo por otra vía.
Página 76 de 120 Ing. Sergio Aníbal Dopazo

“Estadística General”  Variables Aleatorias Continuas – Modelos de Probabilidad

  Parámetros del Modelo: “” (de escala) y “” (de forma).

  Dominio de la Variable Aleatoria: x0.

  Función de densidad de probabilidad: Su expresión es:

|     |     |     |       |     |            |  x  |     |
| --- | --- | --- | ----- | --- | ----------- | ------ | --- |
|     |     |     |       |     | 1         |   |     |
|     |     |     | f(x) |  |  x1e |     |     |
 


  Gráfica de la función de densidad:

Tal  como  podemos  visualizar  en  la  gráfica:  si  “  <  1”,  la  función  de  densidad  es
decreciente como ocurre en el período de nacimiento de la curva de bañera; si “ > 1”,
nos  encontramos  con  una  función  de  degradación  que  describe  bien  el  período  de
envejecimiento de la curva de bañera.

Se cumplen las reglas generales dadas para las variables aleatorias continuas.

  Función de Distribución de Probabilidad: Para este modelo se desarrolla la función de
distribución de probabilidad acumulada derecha.

|       |      |          |        |         |       |       |       |
| ----- | ---- | -------- | ------ | ------- | ------ | ----- | ------ |
|       |      |          |      | 1     |   x |       |   x |
|       |      |          |        | x1 |    |       |    |
| P(VA | x)G | (x/;) |    |        | e    | dxe |       |
|       |      | W        |     |         |        |       |        |
x

1
 1 
|   Moda: Mo |    | 0(si 1), o Mo |    | 1 |  (si 1).  |     |     |
| ----------- | --- | --------------- | --- | ----- | ------------ | --- | --- |
 

Mediana: Meln21
|    |     |     |    |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |

Ing. Sergio Aníbal Dopazo  Página 77 de 120

 
  Esperanza Matemática:  Ex  . Si se estudia a la variable aleatoria del
 1
  1  
  
modelo como la duración de un elemento, la esperanza matemática es “MTTF” y en este
modelo, si “ = 1” por efecto exclusivo del azar, es coincidente con “MTBF”. Debemos
aclarar que “ (t) ” es la función gamma de Euler del valor “t”.

La función gamma de Euler del argumento “t”, permite calcular el factorial de cualquier
número real positivo entero y no entero (siendo t1). Su ecuación es:

|     | t1! | x(t1) | e(x) |     |     |     |
| --- | ------- | ------- | ------ | --- | --- | --- |
|    |        |         | dx    |     |     |     |
t
0
Por ejemplo:

| 0! | x0 e(x)dx | e(x) |          |     |     |     |
| ------ | ------------- | ------ | --------- | --- | --- | --- |
|       |               |       |  011  |     |     |     |
| 1    |               |        | 0         |     |     |     |
0

Toda  calculadora  científica  avanzada  calcula  un  factorial  utilizando  esta  función  (las
científicas convencionales solamente calculan factoriales de números naturales y el de
cero). La calculadora científica del sistema Windows® utiliza la función gamma para el
cálculo de factoriales, pero si se quiere utilizar la planilla tipo Excel®, se debe recurrir a la
EXP(GAMMA.LN(t)), (según versión Microsoft Excel® 2010).
siguiente función: 
t

|    |   |     |     |     |     |     |
| --- | ---- | --- | --- | --- | --- | --- |
Varianza: Vx  2 
  2 2 
|  2     |   1      |     |     |     |     |     |
| -------- | ------------ | --- | --- | --- | --- | --- |
|   1  |   1    |     |     |     |     |     |
|      |          |     |     |     |     |     |


  Coeficiente  de  Variación:  Cv 100.  En este modelo se puede observar que, en

general, el coeficiente de variación es mayor al 20% si “ < 5,7974”, el coeficiente crece;
en cambio si “ > 5,7974”, el coeficiente decrece a valores menores que 20%.

ln11
  Fractiles: x 


|     |        |      |               | 3      |    |     |
| --- | ------- | ---- | ------------- | ------ | --- | --- |
|     |         | 3 | 2          |        |     |     |
|     |       |      |             |        |    |     |
|     |  3    |      |  2  1     |  1   |     |     |
|     |   1 |     |  1   1  |  1  |   |     |
  Coeficiente de Asimetría: As              
3
3 2
|     |     |    | 2  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
 

|     |     |        | 2  1     |     |     |     |
| --- | --- | ------- | ----------- | --- | --- | --- |
|     |     |   1 |   1   |     |     |     |
|     |     |        |        |     |     |     |

|     |    |       |         |     | 2       | 4  |
| --- | --- | ----- | ------- | --- | ------- | --- |
|     |   |  4 |  6 |     |  3 |     |

|     |  4      |    | 3  1     |  2   |  1   |  1      |
| --- | --------- | --- | ----------- | ------ | ------ | --------- |
|     |   1  |    | 1   1  |  1  |  1  |  1   |
  Coeficiente de Kurtosis: Ku                     
4
|     |     |     |    |  2 |     |     |
| --- | --- | --- | --- | --- | --- | --- |
2
|     |     |     |            |               |     |     |
| --- | --- | --- | -------------- | -------------- | --- | --- |
|     |     |     |    1 2  |   1 1   |     |     |
|     |     |     |             |             |     |     |

Página 78 de 120  Ing. Sergio Aníbal Dopazo

“Estadística General” Variables Aleatorias Continuas – Modelos de Probabilidad
  x   1  
 Expectativa Parcial Izquierda: H (x/;) F    / r 1  ; 1,
w  

1

1 

      
observe el lector que se utiliza, para su cálculo, la función de distribución de probabilidad
acumulada izquierda del modelo Gamma, el cual desarrollaremos más adelante.
C. MODELO GUMBEL del MÍNIMO (Emil Gumbel, 1891 – 1966)
Emil Julius Gumbel (Munich, Alemania, 1891 – Nueva York, Estados Unidos, 1966)
fue matemático y escritor político alemán. Su principal aporte fue desarrollar la
teoría estadística de valores extremos. Su tesis para doctorarse en economía
política se refiere a “Cálculo por interpolación del estado de la población”. En 1932
publica un trabajo sobre “La ley estadística sobre la administración de la mortalidad”.
Gumbel encuentra una ley matemática que relaciona la mortalidad con la edad. Se
basó en un estudio de Lexis, quien ajustó las tablas de mortalidad para edades
fuera de lo normal con la distribución Normal; Gumbel extiende su fórmula a toda la
tabla, considerando como variable la edad (y no la muerte), y estudia la expectativa
de vida para cada edad. Enuncia su principio estadístico en sus obras: “Nuestra vida
está en las manos de Dios”, “El destino hace que los que viven sean bolilla negra en
una urna” y “La Ley de los mínimos”. En 1958, publica un tratado dedicado
exclusivamente a las distribuciones de extremos “Statistics of Extremes”.
Gumbel se apoya para el desarrollo del modelo en la distribución de Fréchet. En un principio
este modelo, se originó en el estudio de la vida de seres vivientes de una misma especie. Si se
observan conjuntos de valores y de cada uno de ellos se extraen los valores mínimos, formando un
nuevo conjunto de valores, se forma una distribución de valores aleatorios modelada mediante la
función Gumbel del mínimo. Se puede resumir que, su aplicación está orientada a fenómenos de vida
cuya única causa de falla es el desgaste. Diremos que los seres vivientes mueren, de manera natural,
por desgaste o fatiga.
La variable denominada vida de seres vivientes de una misma especie ha sido objeto de
numerosos estudios, sobre todo en la especie humana. Los objetivos de tales estudios, son de
diversa índole, pero en relación con las Ciencias de la Administración, resultan de utilidad para el
cálculo de las primas de seguros de vida. Hasta no hace mucho tiempo se seguía utilizando la
distribución Normal, despreciándose la clara asimetría negativa de dicha variable; esta aproximación
resulta algunas veces razonable cuando se trata de vida o de duración de objetos inanimados o de
algunas especies animales. Para los humanos, se comenzó a trabajar con el modelo de Weibull, que
permite una exactitud considerablemente mejor; sin embargo, estudios más recientes realizados con
modernas técnicas de tratamiento de datos, permiten concluir que la distribución más exacta para
estas variables es la propuesta por Gumbel en su obra fundamental sobre extremos de una variable
aleatoria.
Se trabaja con dos parámetros: “” y “”, el primero se denomina parámetro de escala y el
segundo parámetro, de corrimiento, es la moda o bien el valor modal de la variable, o sea, aquel
valor que maximiza la función de densidad. En relación al estudio de la expectativa de vida humana,
estos parámetros toman distintos valores según el país y el sexo, siendo en general (en sociedades o
grupos de tipo patriarcales) la mujer más longeva que el varón. Cabe aclarar que expongo el
concepto de sociedad o grupo “tipo” patriarcal, desde el punto de vista que en el varón recae la
responsabilidad de la manutención del hogar o clan familiar, y no como el del varón dominante de la
Ing. Sergio Aníbal Dopazo Página 79 de 120

mujer. En cambio en sociedades o grupo de “tipo” matriarcales (la responsabilidad de la manutención
recae en la mujer), en general es el varón más longevo que la mujer.
El parámetro “”, en la teoría de la fiabilidad, y, para algunas aplicaciones, se denomina como
la vida característica o valor característico.
Se puede demostrar que el modelo Gumbel del mínimo, se puede obtener aplicando el
logaritmo natural a la variable Weibull. Son ejemplos de su uso habitual: primas de los seguros de
vida, vida de animales de una misma especie, etc.
Debemos destacar que, si bien Gumbel estudió el problema de la expectativa de vida humana,
este modelo no limita su utilización a la vida de seres vivientes. Otra de sus aplicaciones es en el
estudio del extremo mínimo de un conjunto de “n” elementos, de los cuales no conocemos el
comportamiento estadístico. Por ello, también se lo denomina Distribución de Extremo Mínimo de una
variable. También se lo utiliza para predecir desastres naturales por extremidad mínima, por ejemplo:
caudal mínimo de un río, precipitaciones mínimas (sequía), caudal de viento mínimo, etc. En
hidrología, hoy en día, la Gumbel del mínimo y la del Máximo, son los modelos aplicados por
excelencia. Los modelos de Gumbel son adecuados para estudiar estos fenómenos, porque se basa
en estudiar los extremos de una variable, y el objetivo fundamental de este tipo de variables reside
justamente en este concepto (los desastres meteorológicos se dan en los extremos), y además se
estudia para grandes períodos de retorno.
El modelo Gumbel del mínimo también se utiliza, en general por ejemplo, cuando en ciertos
sistemas complejos deja de funcionar un elemento vital, pues el sistema falla cuando falla el primero
de sus elementos importantes (o sea el que tiene mínima duración con respecto a los otros). No es,
acaso, un ser viviente un sistema complejo. Usos menos frecuentes, pero no menos importantes, son
para el estudio de emisiones de ondas extremas (en este caso ondas mínimas).
Cuando la variable aleatoria en cuestión es una magnitud relacionada con algún fenómeno
natural, es conveniente referirse a períodos de retorno (o bien recurrencia) en lugar de referirse a
probabilidades de ocurrencia. Si el valor “” es la probabilidad de que la variable supere un valor de
“x” específico en un cierto lapso de tiempo (por lo general se estipula un año), el período de retorno
“T” representará el número de unidades de tiempo que transcurrirán en promedio entre dos
oportunidades en que la variable supere dicho valor, es decir:
1
Gx  
T
Por ejemplo, si esta probabilidad “” es igual a “0,01”, esto es equivalente a especificar un
período de retorno o recurrencia de “100 años” (si el lapso de tiempo estipulado es un año).
 Parámetros del Modelo: “” (de escala) y “” (de corrimiento).
 Dominio de la Variable Aleatoria:   x  .
 Función de densidad de probabilidad: Su expresión es:
f(x)
1
e


x

 


e


 

 e   x     

 



Página 80 de 120 Ing. Sergio Aníbal Dopazo

“Estadística General” Variables Aleatorias Continuas – Modelos de Probabilidad
 Gráfica de la función de densidad:
Tal como podemos visualizar en la gráfica, la asimetría es negativa tal como si fuera una
Weibull donde predominan las causas del desgaste. El modo se encuentra alejado de los
valores mínimos de la variable.
Se cumplen las reglas generales dadas para las variables aleatorias continuas.
 Función de Distribución de Probabilidad: Para este modelo se desarrolla la función de
distribución de probabilidad acumulada derecha.
 x  x
 1   x    e         e      
P(VA x)G (x/;)  e   e   dxe  
Gm 
x
 Moda: Mo  . Es el parámetro de la función.
 Mediana: Me   lnln2
 Esperanza Matemática: Ex   C. Debemos aclarar que “C” es la constante
de Euler – Mascheroni, esta constante es un número especial en el análisis matemático.
Este número también es conocido como constante de Euler, es una constante
matemática que aparece principalmente en teoría de números, y, habitualmente se denota
con la letra griega “”, pero como esta letra también se utiliza en estadística para denotar
un modelo, nosotros vamos a denominar a esta constante como “C”. Esta constante no
debe confundirse con el número “e” que también es llamado número de Euler. La
constante, se define como el límite de la diferencia entre la serie armónica y el logaritmo
natural de la siguiente expresión:
Ing. Sergio Aníbal Dopazo Página 81 de 120

|     |        | n 1    |    | lnx |      |                                             |     |     |     |
| --- | -------- | ------- | --- | ------- | ---- | ------------------------------------------- | --- | --- | --- |
|     | Clím | lnn |     |         |     |                                             |     |     |     |
|     |          |         |   |       | dx | 0,577215664901532860606512090082402431...  |     |     |     |
ex
|     | n | k  |    |    |    |     |     |     |     |
| --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | k1   |     |     | 0   |     |     |     |     |     |

Las calculadoras científicas no traen esta constante, pero en una científica avanzada se
puede escribir la función correspondiente y la misma es calculada.

2
|     | Varianza: Vx |    | 2  | 2  |     |     |     |     |     |
| --- | -------------- | --- | ---- | ---- | --- | --- | --- | --- | --- |

6


  Coeficiente  de  Variación:  Cv 100.  En este modelo se puede observar que, en

general, el coeficiente de variación es mayor al 20%.

|    | Fractiles: x |  lnln1  |     |     |     |     |     |     |     |
| --- | ------------ | ------------------- | --- | --- | --- | --- | --- | --- | --- |


 x3f(x)dx

|    | Coeficiente de Asimetría: As |     |     |     |    |   |     | 1,139547099...  |     |
| --- | ------------------------------ | --- | --- | --- | --- | --- | --- | ----------------- | --- |
|     |                                |     |     |     | 3   |     | 3  |                   |     |

|     |     |     |     |     |     |  x4 |          |     |     |
| --- | --- | --- | --- | --- | --- | -------- | -------- | --- | --- |
|     |     |     |     |     |     |         | f(x)dx |     |     |
  Coeficiente  de  Kurtosis:  Ku   5,4.  La  distribución  es
|     |     |     |     |     | 4   |     | 4  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
leptocúrtica.

  Expectativa Parcial Izquierda:
|     |              |            |     |      | t                   |     |     |     | x    |
| --- | ------------ | ---------- | --- | ---- | ------------------- | --- | --- | --- | -------- |
|     |              |  1e(t) |     |      | lntdt; donde: t |     |     |     |      |
|     | H (x/;) |            |     |  | e(t)               |     |     |  e |    .  |
Gm
0
|     | t                  |           |     |            |   1ntn |     |     |     |     |
| --- | ------------------ | --------- | --- | ---------- | ----------- | --- | --- | --- | --- |
|     |  e(t) lntdt |  1e(t) |     |  lnt |             |     |     |     |     |
; esta integral tiene una fórmula aproximada:
nn!
n1
0

|     |                 |     |        |     |           | 2         |               |     |     |
| --- | --------------- | --- | ------ | --- | ----------- | ---------- | --------------- | --- | --- |
|     | t               |     | 1 t13 | 5   |    1  | 3t 13 8  |                |     |     |
|     | e(t)lntdt |     |        |     |   2      | 3         |              |     |    |
|     |                |     |      |    |    e    |            |   C 1e(t) |     |     |
|     |                 |     |       |     |            |            |                 |     |     |
|     |                 |     | 2  2 | 3  |            |            |                |     |     |
|     | 0               |     |        |     |            |            |                |     |     |

Observe  el  lector  que  para  calcular  la  expectativa  parcial,  se  utiliza  una  fórmula
aproximada, la cual es:

|     |                    |     |     |            |     |      |      |           | 2        |
| --- | ------------------ | --- | --- | ---------- | --- | ---- | ---- | ----------- | ---------- |
|     |                    |     |     |            |     |  t1 | 5   |   1  3t | 1 3 8   |
|     |                    |     |     |  1e(t) |    |      | 3    |  2       | 3       |
|     | H x/;C |     |     |            |    |    |   | e        |         |
Gm
|     |     |     |     |     | 2  |  2 | 3  |    |    |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |     |     |    |    |

| Página 82 de 120  |     |     |     |     |     |     |     |     | Ing. Sergio Aníbal Dopazo  |
| ----------------- | --- | --- | --- | --- | --- | --- | --- | --- | -------------------------- |

“Estadística General” Variables Aleatorias Continuas – Modelos de Probabilidad
D. MODELO GUMBEL del MÁXIMO (Emil Gumbel, 1891 – 1966)
Si se observan conjuntos de valores y de cada uno de ellos se extraen los valores máximos,
formando un nuevo conjunto de valores, se forma una distribución de valores aleatorios modelada
mediante la función Gumbel del Máximo. Se puede resumir que, su aplicación está orientada a
fenómenos donde interesa estudiar los límites de los valores máximos.
Se trabaja con dos parámetros: “” y “”, el primero se denomina parámetro de escala y el
segundo parámetro, de corrimiento, es la moda o bien el valor modal de la variable, o sea, aquel
valor que maximiza la función de densidad. Estos parámetros toman distintos valores.
Debemos destacar el uso de la distribución Gumbel del Máximo. Una de sus aplicaciones es
en el estudio del extremo máximo de un conjunto de “n” elementos, de los cuales no conocemos el
comportamiento estadístico, en contraposición del modelo Gumbel del mínimo. Por ello, también se lo
denomina Distribución de Extremo Máximo de una variable. También se lo utiliza para predecir
desastres naturales por extremidad máxima, por ejemplo: caudal máximo de un río, precipitaciones
máximas (inundaciones), caudal de viento máximo, caudal máximo en las vías de circulación, etc. En
hidrología, hoy en día, la Gumbel del mínimo y la del Máximo, son los modelos aplicados por
excelencia. Los modelos de Gumbel son adecuados para estudiar estos fenómenos, porque se basa
en estudiar los extremos de una variable, y el objetivo fundamental de este tipo de variables reside
justamente en este concepto (los desastres meteorológicos se dan en los extremos), y además se
estudia para grandes períodos de retorno. Este modelo resulta muy útil para predecir terremotos,
inundaciones o cualquier otro desastre natural que pueda ocurrir. También se utiliza para el
dimensionamiento y diseño de aliviaderos o bien de represas hidráulicas o bien se utilizan en el
diseño de construcciones civiles que puedan estar sometidas a condiciones climatológicas extremas.
El modelo Gumbel del Máximo también se utiliza, en general, para el estudio de la elongación
de los materiales hasta la rotura, sin llegar estos, por lo general, a romperse. En particular se lo ha
utilizado para estudiar el alargamiento porcentual de ciertos tipos de hilo (pues el hilo se estira tanto
como la fibra que más cede, la que tiene máxima elongación), y el alargamiento porcentual de ciertos
materiales. Usos menos frecuentes, pero no menos importantes, son para el estudio de emisiones de
ondas extremas (en este caso ondas máximas).
Debemos recordar lo desarrollado en el modelo Gumbel del mínimo, cuando la variable
aleatoria en cuestión es una magnitud relacionada con algún fenómeno natural. Es conveniente, en
estos casos, referirse a períodos de retorno (o bien recurrencia) en lugar de referirse a probabilidades
de ocurrencia, tal como lo desarrollamos oportunamente.
 Parámetros del Modelo: “” (de escala) y “” (de corrimiento).
 Dominio de la Variable Aleatoria:   x  .
 Función de densidad de probabilidad: Su expresión es:
f(x)
1
e


x

 


ee


x

 



Observe el lector que la función de densidad de este modelo es sutilmente diferente al
modelo Gumbel del mínimo.
Ing. Sergio Aníbal Dopazo Página 83 de 120

  Gráfica de la función de densidad:

Tal como podemos visualizar en la gráfica, la asimetría es positiva tal como si fuera una
Weibull donde predominan las causas del azar. El modo se encuentra cercano de los
valores mínimos de la variable.

Se cumplen las reglas generales dadas para las variables aleatorias continuas.

  Función de Distribución de Probabilidad: Para este modelo se desarrolla la función de
distribución de probabilidad acumulada izquierda.

|            |          |              |   x    |   x    |
| ---------- | -------- | ------------ | ------------- | ------------- |
|            |          |              |        |        |
|            |          | x 1   x |   e        |   e        |
|            |          |            |          |           |
| P(VA x)F | (x/;) |  e        |  e dx      | e            |
|            | GM       |             |               |               |


|   Moda: Mo  | . Es el parámetro de la función.  |     |     |     |
| ------------- | ---------------------------------- | --- | --- | --- |

|   Mediana: Me |    lnln2  |     |     |     |
| -------------- | ------------------ | --- | --- | --- |

Esperanza Matemática: Ex
|    |     |   C  |     |     |
| --- | --- | ---------- | --- | --- |

2
Varianza: Vx
  2  2. Observe el lector que la varianza en este modelo se calcula
6
igual que en el modelo Gumbel del mínimo.


  Coeficiente  de  Variación:  Cv 100.  En este modelo se puede observar que, en

general, el coeficiente de variación es mayor al 20%.

|   Fractiles: x |  lnln  |     |     |     |
| --------------- | ----------------- | --- | --- | --- |


Página 84 de 120  Ing. Sergio Aníbal Dopazo

“Estadística General”  Variables Aleatorias Continuas – Modelos de Probabilidad

 x3f(x)dx

|    | Coeficiente de Asimetría: As |     |     |    |   |     | 1,139547099...  |     |
| --- | ------------------------------ | --- | --- | --- | --- | --- | ---------------- | --- |
|     |                                |     |     | 3   | 3  |     |                  |     |

|     |     |     |     |     |   x4 | f(x)dx |     |     |
| --- | --- | --- | --- | --- | ---------- | -------- | --- | --- |

  Coeficiente  de  Kurtosis:  Ku  5,4.  La  distribución  es
|     |     |     |     |     | 4   | 4  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
leptocúrtica igual que la distribución correspondiente al modelo Gumbel del mínimo.

  Expectativa Parcial Izquierda:
|     |                 |          |     | t     |                     |     |     |  x    |
| --- | --------------- | -------- | --- | ----- | ------------------- | --- | --- | -------------- |
|     | (x/;)e(t) |          |     | e(t) | lntdt; donde: t |     |     |               |
|     | H               | C |     |       |                     |     |    | e   .        |
GM
0
 1ntn
|     | t   |   |     |    |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
 e(t) lntdt 1e(t) lnt ; esta integral tiene una fórmula aproximada:
nn!
|     | 0   |     |     | n1 |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

|     |                 |        |       |         | 8 2         |             |     |     |
| --- | --------------- | ------ | ----- | --------- | -------------- | ----------- | --- | --- |
|     | t               | 1 t13 | 5    |    1 |  3t 13    |             |     |     |
|     | e(t)lntdt |        |       |  2       |  3          |            |    |     |
|     |                |      |    |  e      |              | C 1e(t) |     |     |
|     |                 |  2    | 3   |           |                |             |     |     |
|     |                 | 2    |       |          |               |             |     |     |
|     | 0               |        |       |          |               |             |     |     |

Observe  el  lector  que  para  calcular  la  expectativa  parcial,  se  utiliza  una  fórmula
aproximada, la cual es:

|     |                       |     |     |      |       |           | 1 8 2   |    |
| --- | --------------------- | --- | --- | ---- | ----- | ----------- | -------- | --- |
|     |                       |     |     |    | t1 5 |   1  3t | 3     |     |
|     | x/;Ce(t) |     |     |      | 3     |   2    | 3    |    |
|     | H                     |     |    |    |    | e          |          |    |
|     | GM                    |     |     |      | 2 3   |             |          |     |
|     |                       |     |     | 2  |      |            |          |    |
|     |                       |     |     |      |       |            |          |    |

MODELO LOG–NORMAL

  Este modelo requiere, por su importancia un tratamiento especial, por eso lo desarrollaremos
más adelante. Este modelo rige para una variedad de fenómenos de naturaleza económica, y hoy en
día es utilizado, con habitualidad, para tal fin.

  Solamente en esta sección, a modo introductorio, diremos que una variable aleatoria continua
se comporta como el modelo log–normal, si el logaritmo (en cualquier base) se comporta como el
modelo normal (el cual desarrollaremos más adelante).

Su mención en esta sección se fundamenta en que su función de riesgo es creciente, y suele
utilizarse para modelar la fiabilidad de componentes estructurales y procesos de fallas físicos. Como
por ejemplo: situaciones de colapse estructural como la compresión dinámica del hormigón armado
(aunque muchos autores usan al modelo de Weibull y las normas requieren, en forma errónea, el uso
de la distribución normal), las fallas de materiales que soporten cargas dinámicas como ciertos
hormigones  plásticos  usados  en  prótesis  ortopédicas,  para  evaluar  los  efectos  de  fatiga  sobre
materiales (en este caso, cuando un material está fatigado, su falla se da por colapse estructural), etc.
Podríamos decir, que este modelo, estudia el comportamiento de los materiales exclusivamente en el
período de envejecimiento.

Ing. Sergio Aníbal Dopazo  Página 85 de 120

DISTRIBUCIONES DE EXTREMOS

  Estas distribuciones y sus modelos particulares fueron propuestos por Gumbel, en 1958, para
tratar de describir estadísticamente las denominadas variables aleatorias extremas, es decir, el
máximo o el mínimo de una muestra (o bien de un conjunto) de “n” observaciones. Si tenemos: “x 1 ;
x ; …; x ” una muestra (o bien un conjunto) de observaciones de una variable aleatoria “x”, que
| 2   | n   |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
responde  a  un  determinado  modelo  o  sigue  una  determinada  distribución  de  probabilidad.
Llamaremos al valor mínimo y al valor máximo del conjunto, “x ” y “x ” respectivamente.
mín Máx

  Se demuestra que la probabilidad de que el valor mínimo de “x” (“x ”), tome un valor mayor
mín
o igual que un cierto valor “A” determinado es igual a la probabilidad de que todos los valores en
forma simultánea sean mayores o iguales que ese cierto valor “A”, es decir:

|     |    |    |   |    |    |    |    |   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  Px  A P x  A  x  A ... x  A , y como todos los “x” son independientes,
|     |     | mín |     | 1   | 2   |     |     | n   | i   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
tenemos:
|     |    |    |    |        |    |            |    |      |     |
| --- | --- | --- | --- | ------- | --- | ----------- | --- | ----- | --- |
|     | P x |  A | Px |  A Px |     |  A ...Px |     |  A   |     |
|     |     | mín | 1   |         | 2   |             |     | n     |     |

Si todos los “x” provienen de la misma distribución (o modelo), con función de distribución de
i
probabilidad acumulada derecha “G(x)”, la expresión que queda, se define como distribución de
probabilidad de extremo mínimo:
|     |     |     |     |     | G   | A  |  G | An  |     |
| --- | --- | --- | --- | --- | --- | ----- | --- | ------ | --- |
|     |     |     |     |     |     | x mín | x   |        |     |

  Con un razonamiento similar se puede demostrar que la probabilidad de que el valor máximo
de “x” (“x Máx ”), tome un valor menor o igual que un cierto valor “A” determinado es igual a la
probabilidad de que todos los valores en forma simultánea sean menores o iguales que ese cierto
valor “A”, es decir:

|     |    |    |    |        |    |            |    |      |     |
| --- | --- | --- | --- | ------- | --- | ----------- | --- | ----- | --- |
|     | Px  |  A | Px |  A Px |     |  A ...Px |     |  A   |     |
|     |     | Máx |     | 1       | 2   |             |     | n     |     |

Si todos los “x” provienen de la misma distribución (o modelo), con función de distribución de
i
probabilidad acumulada izquierda “F(x)”, la expresión que queda, se define como distribución de
probabilidad de extremo máximo:
|     |     |     |     |     | F   | A |  F An  |     |     |
| --- | --- | --- | --- | --- | --- | ---- | ---------- | --- | --- |
|     |     |     |     |     |     | xMáx | x          |     |     |

  Gumbel demostró que, para conjuntos de tamaño “n” grandes, o bien, cuando no se conoce
el modelo de comportamiento de “x”, y, en condiciones bastantes generales, las distribuciones de
i
extremo mínimo y máximo se modelan con la Gumbel del mínimo y la del Máximo respectivamente.

|                   |     |     |     |     |     |     |     |                            |     |
| ----------------- | --- | --- | --- | --- | --- | --- | --- | -------------------------- | --- |
| Página 86 de 120  |     |     |     |     |     |     |     | Ing. Sergio Aníbal Dopazo  |     |

“Estadística General” Variables Aleatorias Continuas – Modelos de Probabilidad
OTROS MODELOS DE USO MENOS FRECUENTE
A. MODELO de PARETO (Vilfredo Pareto, 1848 – 1923)
Vilfredo Federico Damaso Pareto (París, Francia, 1848 – Céligny, Suiza, 1923) fue
un sociólogo, economista y filósofo italiano. Nacido en Francia a causa del exilio de
su padre que era marqués de Italia. Pareto realizó importantes contribuciones al
estudio de la economía y de la sociología, especialmente en el campo de la
distribución de la riqueza y el análisis de las elecciones individuales. Fue el creador
del concepto eficiencia de Pareto, y contribuyó, con ideas como la de las curvas de
indiferencia, al desarrollo de la microeconomía. En 1906 hizo la famosa observación
de que el 20% de la población poseía el 80% de la propiedad en Italia,
posteriormente generalizada por Joseph M. Juran en el principio de Pareto (también
conocida como la regla del 80-20 o principio de Pareto). En 1909 Pareto introdujo el
índice de Pareto (la medida de la desigualdad de la distribución del ingreso) y
mostró el cómo se distribuye la riqueza: "a través de cualquier sociedad humana, en
cualquier época o país". Desde esa perspectiva Pareto desechó algunos postulados
económicos, sugiriendo que los individuos actúan basados en elementos instintivos
residuales, no lógicos ni racionales.
Este modelo tuvo su origen en la descripción de unidades económicas según su extensión
(salarios, rentas, empresas según ventas o números de empleados, etc.). Debemos destacar que en
el caso de distribuciones de rentas de personas, el modelo de Pareto se ajusta de manera
satisfactoria; en cambio los salarios de personas, con frecuencia, se ajustan mejor por el modelo Log-
normal (que desarrollaremos más adelante). Históricamente se encontraba en una empresa o bien en
un país, un salario (llamado mínimo vital) que es el percibido por la mayoría de los individuos. Para
los sistemas económicos actuales, quizás este modelo se encuentre pasado de moda, siendo más
realista la aplicación del modelo Log-normal, que es válido para grandes grupos urbanos y
seguramente para muchas empresas.
Esta distribución permite modelar variables en donde se tiene un valor mínimo de frecuencia
máxima (que es el modo o moda de la distribución), por ejemplo: además de las mencionadas, los
reclamos en una compañía de seguros, la distribución de recursos naturales en zonas geográficas, el
tamaño de las ciudades, las fluctuaciones de los precios en los mercados de valores, etc. Esta
variable aleatoria no admite valores por debajo del valor modal. Se observará, luego, que la
distribución log-normal, que admite valores por debajo de su modo o moda, suele modelar mejor a
este tipo de variables.
El modelo de Pareto trabaja con dos parámetros: la moda “”, o parámetro de corrimiento,
que es el valor mínimo que puede tomar la variable aleatoria, y “b”, que es un parámetro de forma
que se deduce a partir del conocimiento de la esperanza matemática. Cuando este modelo es usado
para estudiar el comportamiento de la distribución de riqueza, el parámetro “b” es conocido como
índice de Pareto.
Hoy en día este modelo nos permite realizar una clasificación en función de un criterio, por
ejemplo: clasificar países o empresas en función de la distribución salarial, PBI o ventas, número de
habitantes o empleados, etc. También se ha utilizado este modelo para otro tipo de clasificaciones de
tipo económico-comercial (o también llamadas clasificaciones A-B-C), por ejemplo: tipo de
consumidor, inventarios, sistema de transporte, etc.
Ing. Sergio Aníbal Dopazo Página 87 de 120

  Parámetros del Modelo: “” (de corrimiento) y “b” (de forma).

|   Dominio de la Variable Aleatoria: x |     |  .  |     |
| -------------------------------------- | --- | ----- | --- |

  Función de densidad de probabilidad: Su expresión es:

b
b 
|     |     | f(x) |   |
| --- | --- | ----- | --- |

x x

  Gráfica de la función de densidad:

b


Tal como podemos visualizar en la gráfica, la asimetría es positiva y su forma parecida al
modelo Exponencial. El modo es el valor mínimo de la variable.

Se cumplen las reglas generales dadas para las variables aleatorias continuas.

  Función de Distribución de Probabilidad: Para este modelo se desarrolla la función de
distribución de probabilidad acumulada derecha.

|           |           | b b     | b   |
| --------- | --------- | -------- | --- |
|           |           |       |  |
| P(VAx)G | (x/;b) |  dx |     |
|           | P         |         |    |
|           |           | x x    | x |
x

|   Moda: Mo |  . Es el parámetro de la función.  |     |     |
| ----------- | ------------------------------------ | --- | --- |

|   Mediana: Me | 21 b  |     |     |
| --------------- | --------- | --- | --- |

b
|   Esperanza Matemática: Ex |     |   |     |
| ------------------------------ | --- | --- | --- |
b1

Página 88 de 120  Ing. Sergio Aníbal Dopazo

“Estadística General”  Variables Aleatorias Continuas – Modelos de Probabilidad

b2
| Varianza: Vx | 2  |        |        |     |     |     |
| -------------- | --- | ------ | ------ | --- | --- | --- |
|               |   |        |        |     |     |     |
|                |     | b12 | b2 |     |     |     |


  Coeficiente  de  Variación:  Cv 100.  En este modelo se puede observar que, en

general, el coeficiente de variación es mayor al 20% para valores “b < 6,099”.


|   Fractiles: x |    |     |     |     |     |     |
| --------------- | --- | --- | --- | --- | --- | --- |

|     | 11 | b   |     |     |     |     |
| --- | ------ | --- | --- | --- | --- | --- |

|                                |     |     | 2b1 |      | 2   |     |
| ------------------------------ | --- | --- | ------- | ---- | --- | --- |
|   Coeficiente de Asimetría:  |     |     |        |  1 |     |     |
|                                |     | 3   | b3     |      | b   |     |

|     |     |     |       |  b2 |     |     |
| --- | --- | --- | ------ | -------- | --- | --- |
|     |     |     | 3 3b2 | b2     |     |     |
  Coeficiente de Kurtosis:   . La distribución es leptocúrtica.
|     |     | 4   | bb3b4 |     |     |     |
| --- | --- | --- | ------------- | --- | --- | --- |

|                                     |     |     |          |     |      | b1 |
| ----------------------------------- | --- | --- | -------- | --- | ----- | ------ |
|                                     |     |     |          | b |    |        |
|   Expectativa Parcial Izquierda: H |     |     | (x/;b) |     | 1 |       |

|     |     |     | p   | b1 |  x |   |
| --- | --- | --- | --- | ----- | ------ | --- |

B. MODELO UNIFORME:

El modelo uniforme continuo es una familia de distribuciones de probabilidad para variables
aleatorias continuas, tales que cada miembro de la familia y todos los intervalos de igual longitud en
la  distribución  en  su  rango,  son  igualmente  probables.  Este  modelo  puede  ser  generalizado  a
conjuntos de intervalos más complicados. El dominio de la variable está definido por dos parámetros
de  escala:  “a”  y “b”  los  cuales,  son  a  la  vez,  sus  valores  mínimo  y  máximo. En  el  intervalo
comprendido entre “a” y “b” todos los valores posibles son igualmente probables. Un caso muy
particular de este modelo, denominado modelo uniforme standard, es cuando los parámetros toman
los valores “0” y “1” respectivamente, este caso se lo suele asociar con el modelo beta (0; 1).

Este modelo, extremadamente simple, presenta escasa aplicaciones naturales. No se conocen
variables de la naturaleza que respondan a este modelo. Algunos autores atribuyen su aplicación a
variables que se pueden imaginar distribuidas uniformemente, por ejemplo, si se mide el diámetro de
piezas de un determinado lote producidas por la misma máquina, siempre y cuando la herramienta
sufrió un desgaste progresivo constante durante el lapso de fabricación. Pero su principal motivo de
interés es en el uso de los denominados experimentos de simulación. En el estudio de simulación,
este modelo se utiliza, para la aplicación de la transformada inversa de la función de densidad de
probabilidad correspondiente al modelo en cuestión. Muchos lenguajes de programación poseen la
capacidad  de  generar  números  pseudo-aleatorios  que  están  distribuidos  de  acuerdo  a  una
distribución uniforme standard.

La simulación de una variable aleatoria merece una mención. Simular una variable aleatoria es
obtener valores de ella mediante un procedimiento generalmente matemático-computacional, pocas
veces físico, diferente del proceso natural que la genera. Para una variable aleatoria continua con un
modelo específico se generan valores “y” con una distribución uniforme en el intervalo (0; 1) que
representa la probabilidad de ocurrencia de la variable en cuestión. Dichos valores se pueden generar
con una calculadora (número random) o bien con el Excel (función “=ALEATORIO()”). El problema
Ing. Sergio Aníbal Dopazo  Página 89 de 120

se reduce en resolver la siguiente ecuación: F(x)  y.Donde “y” es el número generado
aleatoriamente, el cual se demuestra que se comporta uniformemente en el intervalo (0; 1), y, “F(x)”
es la función de distribución izquierda de la variable x.
 Parámetros del Modelo: “a” y “b”.
 Dominio de la Variable Aleatoria: a  x b.
 Función de densidad de probabilidad: Su expresión es:
1
f(x)
ba
 Gráfica de la función de densidad:
1
(ba)
Se cumplen las reglas generales dadas para las variables aleatorias continuas.
 Función de Distribución de Probabilidad: Para este modelo se desarrolla la función de
distribución de probabilidad acumulada izquierda.
x 1 xa
P(VA x)F (x/a;b)  dx
UNI ba ba
a
 Moda: Mo   . todos los valores posibles son modales, puesto que todos tienen la
misma probabilidad de ocurrencia. Esta variable aleatoria es amodal.
ab
 Mediana: Me 
2
ab
 Esperanza Matemática: Ex  
2
Página 90 de 120 Ing. Sergio Aníbal Dopazo

“Estadística General” Variables Aleatorias Continuas – Modelos de Probabilidad
ba2
 Varianza: Vx 2 
12

 Coeficiente de Variación: Cv 100.

 Fractiles: x  a ba

 Coeficiente de Asimetría: As 0
3
 Coeficiente de Kurtosis: Ku 1,8. La distribución es platicúrtica.
4
(xa)(xa)
 Expectativa Parcial Izquierda: H (x/a;b) .
UNI 2ba
Ing. Sergio Aníbal Dopazo Página 91 de 120

MODELOS RELACIONADOS CON LA FUNCIÓN DE “DE MOIVRE” – “GAUSS”
A. MODELO NORMAL (Abraham De Moivre, 1667 – 1754 ; Karl Friedrich Gauss, 1777
– 1855):
Johann Karl Friedrich Gauss (Brunswick, Alemania, 1777 – Göttingen, Alemania
1855), fue un matemático, astrónomo y físico que contribuyó significativamente en
muchos campos, incluida la teoría de números. En 1809 Gauss inició el estudio de
la teoría de errores y en 1810 Laplace, que había considerado anteriormente el
tema, completó el desarrollo de esta teoría.
Este modelo es indudablemente el más importante, de los modelos continuos, y el de mayor
uso en la ciencia estadística. El hecho que haya sido tratado a esta altura se justifica en que muchos
autores han abusado de este modelo, sin prueba previa, llevando a conclusiones catastróficas. Éste
fue presentado en 1733, en el libro The Doctrine of Chances (la doctrina de las posibilidades), por
Abraham De Moivre, luego fue ampliado en 1812, en el libro Teoría analítica de las probabilidades,
por Pierre Simon, Marqués de Laplace, dando origen al Teorema de De Moivre-Laplace.
De Moivre en su obra Approximatio ad summam terminorum binomii (a + b)n in seriem
expansi (Aproximación a la suma de los términos del binomio (a + b)n desarrollado como una serie),
explica este modelo como ley de los errores, luego en el libro mencionado en el párrafo anterior
investigó este modelo para hallar aproximaciones para la distribución binomial. Laplace usó el modelo
en el análisis de errores de experimentos, dando origen al importante método de mínimos
cuadrados el cual fue introducido por Legendre en 1805. Johann Karl Friedrich Gauss entabla una
polémica afirmando que el usaba el modelo y el método desde 1794, pero en realidad lo justificó
rigurosamente recién en 1809 asumiendo que los “errores” se modelaban de acuerdo a esta
distribución, estudiando datos astronómicos; es por ello que algunos autores atribuyen a Gauss su
descubrimiento independiente del de De Moivre. Por lo cual a este modelo se lo suele nombrar como
modelo de Gauss o Gaussiano, o simplemente campana normal de Gauss. A pesar de esta
terminología, “normal”, otros modelos de probabilidad podrían ser más apropiados en determinados
contextos, tal como hemos visto en este capítulo.
Este modelo es la piedra angular en la aplicación de la inferencia estadística para el análisis
de los datos, puesto que las distribuciones de muchas estadísticas muestrales tienden hacia la
distribución normal conforme crece el tamaño de la muestra. Muchos estudios indican que el modelo
normal proporciona una adecuada representación, por lo menos en una primera aproximación, de las
distribuciones de una gran cantidad de variables físicas. Muchas variables aleatorias responden a
este modelo, tales como variables tecnológicas, antropométricas y muchas que provienen de
procesos controlados, datos meteorológicos como la temperatura y la precipitación pluvial,
mediciones efectuadas en organismos vivos, calificaciones en pruebas de aptitud, mediciones físicas
de partes de manufactura, errores de instrumentación y otras desviaciones de las normas
establecidas, etc.. Podemos resumir, en general, que cualquier variable aleatoria que presente una
distribución simétrica en forma de campana, se ajusta a este modelo. Sin embargo, cabe aclarar que,
por este motivo, muchas variables aleatorias que no siguen un comportamiento normal, han sido
tratadas, erróneamente, como normales. Debe tenerse mucho cuidado al suponer para una situación
dada un modelo de probabilidad normal sin previa comprobación. El uso abusivo de este modelo, sin
previa comprobación, puede llevar a conclusiones erróneas graves sobre un hecho. Es por este
abuso que a veces la ciencia estadística tiene mala reputación, pero no debe culparse a la ciencia
sino a los que mal usan y abusan de ella.
Página 92 de 120 Ing. Sergio Aníbal Dopazo

“Estadística General” Variables Aleatorias Continuas – Modelos de Probabilidad
Todo el mundo cree y afirma que los errores siguen una la ley normal: los matemáticos,
porque piensan que es un hecho experimental; y los experimentadores, porque suponen que es un
teorema matemático; pero a veces estos errores pueden no comportarse de acuerdo con este
modelo. Por ejemplo: si todas las fuentes principales de errores se han tomado en cuenta, se asume
que el error que queda debe ser el resultado de un gran número de muy pequeños y aditivos efectos
y, por consiguiente, de comportamiento normal; pero no siempre es verdad; si los datos originales no
están normalmente distribuidos, entonces los residuos o errores residuales tampoco estarán
normalmente distribuidos. Este hecho es ignorado habitualmente en la práctica.
La importancia de este modelo radica en que permite modelar numerosos fenómenos
naturales, sociales y psicológicos. Mientras que los mecanismos que subyacen a gran parte de este
tipo de fenómenos son desconocidos, por la enorme cantidad de variables incontrolables que en ellos
intervienen, el uso del modelo normal puede justificarse asumiendo que cada observación se obtiene
como la suma de unas pocas causas independientes.
Otros usos: la intensidad de la luz láser, la luz térmica en escalas de tiempo grandes, la
longitud de apéndices inertes (pelo, garras, rabos, dientes) de especímenes biológicos en la dirección
del crecimiento, aproximación de varios modelos de probabilidad discretos y continuos, caracteres
morfológicos de individuos como la estatura, caracteres fisiológicos como el efecto de un fármaco,
caracteres sociológicos como el consumo de cierto producto por un mismo grupo de individuos,
caracteres psicológicos como el cociente intelectual, nivel de ruido en telecomunicaciones, errores
cometidos al medir ciertas magnitudes, etc.
Podemos resumir, entonces, que esta distribución es de vital importancia por cuatro razones
principales:
 Numerosos fenómenos continuos parecen seguirla o se pueden aproximar mediante
ella.
 Se puede utilizar como aproximación de otras distribuciones, tanto discretas como
continuas.
 Las distribuciones de comportamiento normal son estrictamente estables y
homogéneas.
 Proporciona la base para la inferencia estadística clásica por su relación con el
Teorema Central del Límite dónde se afirma que la suma de variables aleatorias de
conjuntos cuantiosos tiende a comportarse de acuerdo a este modelo (este teorema,
que estudiaremos más adelante, merece un capítulo aparte).
Como consecuencia de lo anteriormente mencionado, es importante realizar la validación del
modelo antes de aplicarlo a un fenómeno determinado. La validación del modelo se realiza mediante
los denominados “test o pruebas de normalidad”, los cuales se aplican a conjuntos de datos para
determinar su similitud con una distribución normal, o si bien el comportamiento los datos se ajusta a
este modelo. Debemos aclarar que la validación de un modelo determinado es esencial antes de la
aplicación de ese modelo, por lo cual se deberán realizar pruebas de validación para todos los
modelos que uno quiera aplicar. Las pruebas o test de normalidad actualmente conocidos son:
“Prueba de Kolmogórov-Smirnov”, “Test de Lilliefors”, “Test de Anderson–Darling”, “Test de Ryan–
Joiner”, “Test de Shapiro–Wilk”, “Normal probability plot (rankit plot)” (gráfico de la probabilidad
normal), “Test de Jarque–Bera” y “Test omnibús de Spiegelhalter”.
Escapan al tratado del apunte modelos o distribuciones de probabilidad las cuales son
extensiones del modelo Normal General. Son ellos: el modelo o distribución de probabilidad
Multinormal y el modelo o distribución de probabilidad Bi–Normal.
Ing. Sergio Aníbal Dopazo Página 93 de 120

Las características interesantes del modelo Normal son: que la función de densidad es
simétrica, y, que los parámetros del mismo son su propia esperanza matemática “”, de escala, que
marca el eje central de simetría de la distribución, y su propio desvío estándar “”, parámetro de
escala, el cual marca la distancia que existe desde el eje central de simetría hasta los puntos de
inflexión de la curva.
 Parámetros del Modelo: “” y “” (ambos de escala).
 Dominio de la Variable Aleatoria:   x  .
 Función de densidad de probabilidad: Su expresión es:
1x2
1    
f(x)  e 2   
 2
 Gráfica de la función de densidad:
Algunas propiedades importantes de este modelo, tal como podemos visualizar en la
gráfica de la función de densidad:
a) El modelo presenta un eje de simetría respecto de su esperanza matemática, la
cual coincide con la moda y la mediana de la variable aleatoria. O sea que es una
curva simétrica con forma de campana, que se extiende sin límite tanto en la
dirección positiva como en la negativa.
b) Los puntos de inflexión de la curva se encuentran a una distancia igual al desvío
estándar del eje de simetría, o sea en los puntos: x   y x  .
c) El conjunto de los valores se encuentra distribuido de la siguiente forma: el 68,27%
de los valores se encuentra en el intervalo    x     ; el 95,45% se
encuentra en el intervalo  2 x    2; el 99,73% se encuentra en el
intervalo  3 x    3, y, el 99,99% se encuentra en el intervalo
  4 x    4, o sea que fuera de este intervalo se encuentra el 0,01%
de los valores. Esto se puede visualizar en el gráfico siguiente.
Página 94 de 120 Ing. Sergio Aníbal Dopazo

“Estadística General” Variables Aleatorias Continuas – Modelos de Probabilidad
Se cumplen las reglas generales dadas para las variables aleatorias continuas.
 Función de Distribución de Probabilidad: Para este modelo se desarrolla la función de
distribución de probabilidad acumulada izquierda.
x 1    1    x  2 
P(VA x)F (x/;)  e 2    dx. Esta integral no se puede resolver
N  2

con procedimientos elementales, se requieren métodos especiales del análisis
matemático; pero gracias a Pierre Simón, Marqués de Laplace, la función normal general
se la puede simplificar o bien reducir a una expresión más simple empleando una
transformación con un cambio de variable (llamada sustitución de Laplace o función
normal estándar o reducida) que veremos más adelante.
 Moda: Mo   Me
 Mediana: Me    Mo
 Esperanza Matemática: Es uno de los parámetros del modelo:
Ex
.
 Varianza: Es uno de los parámetros del modelo: Vx 2; teniendo la misma
interpretación que en la generalidad de las variables aleatorias continuas.

 Coeficiente de Variación: Cv 100. En este modelo se puede afirmar, en general,

que el coeficiente de variación no supera el 20%. Podemos deducir que las variables de
comportamiento normal tienden a ser de característica homogénea. En la gran mayoría de
las aplicaciones este coeficiente será inferior al 10%.
Ing. Sergio Aníbal Dopazo Página 95 de 120

 Fractiles: x Z , siendo “Z ” el fractil de una variable normal estandarizada.
  
 Coeficiente de Asimetría: As 0
3
 Coeficiente de Kurtosis: Ku 3. Es una distribución mesocúrtica.
4
 1x2
     
 Expectativa Parcial Izquierda: H (x/;)F x/;  e 2   .
N N 2  
 
B. MODELO NORMAL ESTÁNDAR (Pierre Simon Laplace, 1749 – 1827):
Este modelo fue desarrollado por Laplace (ver referencia biográfica en el capítulo de Cálculo
de Probabilidades) como simplificación del modelo normal general. Es por eso que a este modelo
también se lo denomina Normal centrada reducida o bien Normal reducida o bien Normal
estandarizada o tipificada. Este modelo sirve para facilitar el cálculo de probabilidades de la
distribución normal general. La variable aleatoria de este modelo “Z”, es una transformación de la
variable “x” normal general. De modo que podemos asegurar que una variable aleatoria “x” que
tiene una media “” y un desvío estándar “”, se puede transformar a una variable normal estándar
con la siguiente expresión:
x
Z 

Con esta fórmula se pueden transformar una variable aleatoria normal en una variable
aleatoria normal estandarizada, por eso al emplear esta transformación se dice que se está
estandarizando a una variable aleatoria normal general. Por lo tanto se puede convertir cualquier
variable de comportamiento normal a una variable de comportamiento normal estándar.
Este modelo, al ser de comportamiento normal, tiene las mismas propiedades y características
del modelo normal general.
 Parámetros del Modelo: “= 0” y “ = 1” (ambos de escala).
 Dominio de la Variable Aleatoria:    Z   .
 Función de densidad de probabilidad: Su expresión es:
Z2
fz 1 e    2   
2
 Gráfica de la función de densidad:
Página 96 de 120 Ing. Sergio Aníbal Dopazo

“Estadística General” Variables Aleatorias Continuas – Modelos de Probabilidad
Al igual que el modelo normal general, el modelo normal estándar presenta una función
simétrica con las mismas propiedades que la función normal general. Una característica
particular de este modelo es que la distancia al eje de simetría se mide en función de
cuantas veces el desvío estándar se aleja. La función prácticamente se anula a una
distancia del eje de simetría (la esperanza matemática) “  0”, igual a 4 veces el valor
del desvío estándar (como   1), o sea  4. Tal es así que el 99,74% de los valores se
encuentra en el intervalo 3  Z  3.
Se cumplen las reglas generales dadas para las variables aleatorias continuas.
 Función de Distribución de Probabilidad: Para este modelo se desarrolla la función de
distribución de probabilidad acumulada izquierda.
P(VA Z)F Z   Z 1 e    Z 2 2     dZ. Esta integral es sencilla de resolver con
NS 2

procedimientos elementales, pero la misma está tabulada para valores de “Z”
comprendidos entre “-4 y 4” o bien, de manera simplificada, entre “0 y 4”. Por convención
se denomina a la función de distribución de probabilidad acumulada izquierda con la letra
griega “”. Entonces tenemos:
x
P(VA Z)F (Z)Z F (x/;), la cual coincide con la función de
NS    N
distribución de probabilidad acumulada izquierda de una variable “x” normal general.
También se desarrolla la función de distribución de probabilidad acumulada derecha:
x
P(VA Z)G (Z)1(Z)1 G (x/;), la cual coincide con la función
NS    N
de distribución de probabilidad acumulada derecha de una variable “x” normal general.
Por ser una distribución simétrica con eje en cero, se puede demostrar que:
  Z 1 Z y  Z 1  Z
 Moda: Mo   Me  0
Ing. Sergio Aníbal Dopazo Página 97 de 120

 Mediana: Me   Mo  0
 
 Esperanza Matemática: Es uno de los parámetros del modelo: E Z 0.
 Varianza: Es uno de los parámetros del modelo: VZ 2 1

 Coeficiente de Variación: Cv 100. En este modelo se puede afirmar, en general,

que el coeficiente de variación no supera el 20%. Podemos deducir que las variables de
comportamiento normal tienden a ser de característica homogénea. En la gran mayoría de
las aplicaciones este coeficiente será inferior al 10%.
 Fractiles: Se demuestra que la expresión general para las variables aleatorias continuas
se simplifica mediante el uso de tablas o software para fractiles de la normal estandarizada
“Z ”. Tener en cuenta que al ser un modelo simétrico cuyo eje de simetría está en “0”, se

tiene que: Z  Z
 1
 Coeficiente de Asimetría: As 0
3
 Coeficiente de Kurtosis: Ku 3. Es una distribución mesocúrtica.
4
 Z2
 Expectativa Parcial Izquierda: H (Z)  1   e    2     
NS
2  
 
C. MODELO LOG–NORMAL:
Este modelo fue propuesto por Sir Francis Galton en 1879 y luego usado por Charles Cobb y
Paul Douglas, por eso se lo conoce, también como modelo de Cobb–Douglas o modelo de Galton.
Este modelo fue usado como primera aproximación del modelo de Landau que dio origen al modelo
de Moyal.
Se define que una variable aleatoria sigue un comportamiento log–normal, si su logaritmo
sigue el modelo normal. Esto quiere decir que una variable que se comporta normalmente, entonces
la exponencial de esta variable se comporta según el modelo log–normal. Esta distribución rige
cuando las variaciones de la variable se observan entre distintos individuos o unidades
experimentales en un momento fijo del tiempo, y no sobre un individuo a través del tiempo. Por eso,
se la define como variable trasversal o de sección trasversal.
Cuando, en el presente capítulo, mencionamos los modelos asociados a fenómenos de vida,
hemos hecho una mención sobre este modelo. A las características mencionadas se agregan las que
expresamos en este apartado.
Cuando las causas pueden actuar en forma multiplicativa, se puede afirmar que la productoria
de un número “suficiente” de variables aleatorias positivas (ciertas magnitudes) sigue un
comportamiento log–normal. Podemos enumerar algunas situaciones dónde se presentan este tipo
de problemas: variables financieras (tasas de cambio, índices de precios, índices de existencias de
mercado, efectos multiplicativos en el desgaste de materiales (falla por colapso estructural).
Página 98 de 120 Ing. Sergio Aníbal Dopazo

“Estadística General” Variables Aleatorias Continuas – Modelos de Probabilidad
Ejemplos de uso: los ingresos de grandes grupos de individuos, en general cualquier variable
económica o financiera de corte trasversal, consumos, salarios (donde se admite valores por debajo
del modo), saldos de cuenta corriente, la evolución de los precios de un determinado producto, el
retorno a largo plazo de una inversión, el tamaño de partículas que resultan de un proceso de
molienda, la concentración de distintas impurezas en el agua proveniente de perforaciones
practicadas en una determinada zona, etc. Otro uso de este modelo se da en el comportamiento de la
disolución de gases en gases. Durante muchos años se creyó, de la mano de Gauss, que la
disolución tenía un comportamiento normal (tal como fue probado por el autor). El error conceptual de
esta afirmación es que Gauss para modelar dicho comportamiento, transforma a la variable aplicando
el logaritmo, y tal como definimos al principio: el logaritmo de una variable log–normal, tiene
comportamiento normal. Con esta simple definición de la variable, demostramos lo dicho.
Este modelo presenta una fuerte asimetría y sus parámetros son “m”, de escala, que es la
esperanza matemática de los logaritmos de la variable, y “D”, parámetro de forma, que es el desvío
estándar de los logaritmos de la variable. Esto quiere decir que si tenemos el conjunto de valores
(variable aleatoria) que se modelan según un comportamiento log–normal, y a todos los valores le
averiguamos su logaritmo, la esperanza matemática y el desvío estándar que surgen de estos nuevos
valores son “m” y “D” respectivamente.
 Parámetros del Modelo: “m” (de escala) y “D” (de forma).
 Dominio de la Variable Aleatoria: x  0.
 Función de densidad de probabilidad: Su expresión es:
1lnXm2
1    
f(x) e 2 D  
XD 2
 Gráfica de la función de densidad:
Algunas propiedades importantes de este modelo, tal como se puede visualizar en la
gráfica de la función de densidad siguiente, es que al aplicar el logaritmo natural de la
variable obtenemos una gráfica de comportamiento normal.
Ing. Sergio Aníbal Dopazo Página 99 de 120

Se cumplen las reglas generales dadas para las variables aleatorias continuas.

  Función de Distribución de Probabilidad: Para este modelo se desarrolla la función de
distribución de probabilidad acumulada izquierda.

|       |     |      |          |     |     |                 | 2          |         |                         |
| ----- | --- | ---- | -------- | --- | --- | ---------------- | ----------- | ------- | ----------------------- |
|       |     |      |          |     | x   |   1   lnxm |            |         |                         |
|       |     |      |          |     | 1   | 2            | D          | lnxm |                         |
| P(VA |     | x)F | (x/m;D) |     |    | e               |   dx |         | . Esta integral no se  |
LN
|     |     |     |     |     | xD | 2  |     |  D |    |
| --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- |
0
puede resolver con  procedimientos elementales, se  requieren métodos especiales del
análisis matemático; pero gracias a Laplace y a lo demostrado anteriormente, este cálculo
se  lo  puede  simplificar  o  bien  reducir  a  una  expresión  más  simple  empleando  una
transformación con un cambio de variable utilizando la distribución normal estándar.

|   Moda: Mo |     |     |  mD2  |     |     |     |     |     |     |
| ----------- | --- | --- | -------- | --- | --- | --- | --- | --- | --- |
 e

em
|   Mediana: Me |     |     |    |     |     |     |     |     |     |
| -------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

|                                |     |     |     |     |     |  D2      |     |     |     |
| ------------------------------ | --- | --- | --- | --- | --- | ---------- | --- | --- | --- |
|                                |     |     |     |     |     |   m   |     |     |     |
|   Esperanza Matemática: Ex |     |     |     |     |   | e  2 .   |     |     |     |

|                |     |    |    |   2mD2 |    D2 |    |     |     |     |
| -------------- | --- | --- | --- | ---------- | --------- | --- | --- | --- | --- |
|   Varianza: V |     | x   | 2 |  e        |  e       | 1  |     |     |     |

Si se tiene una variable aleatoria de comportamiento log–normal, en una situación real, y se
pueden obtener su esperanza matemática “” y su desvío estándar “”, los parámetros del modelo
“m” y “D” respectivamente se pueden obtener mediante las siguientes expresiones:

|      |    |     |     |       |            |               |     |      |     |
| ---- | --- | --- | --- | ------ | ---------- | ------------- | --- | ---- | --- |
|      |    |     |     |       |            |               |     |      |     |
|      |     |    |     |        |           | 2            |     |      |     |
|      |    |     |     |  y D2 | ln 1  |  , siendo D |     | D2   |     |
| mln |     |     |     |        |           |            |     |      |     |
|      |    |     | 2   |       |           |              |     |      |     |
|      |     |   |    |        |           |              |     |      |     |
|      |    | 1 |    |       |            |               |     |      |     |
|      |     |    |   |        |            |               |     |      |     |
|      |    |     |     |       |            |               |     |      |     |


  Coeficiente de Variación: Cv 100. Al ser una variable de comportamiento con fuerte

asimetría positiva, en este modelo se puede afirmar, en general, que el coeficiente de
variación  supera  el  60%.  Podemos  deducir  que  las  variables  que  tienen  un
| Página 100 de 120  |     |     |     |     |     |     |     | Ing. Sergio Aníbal Dopazo  |     |
| ------------------ | --- | --- | --- | --- | --- | --- | --- | -------------------------- | --- |

“Estadística General” Variables Aleatorias Continuas – Modelos de Probabilidad
comportamiento log–normal tienden a ser de característica heterogénea. En algunas
aplicaciones este coeficiente será muy superior al 100%.
 
 Fractiles: x  emZD , siendo “Z ” el fractil de una variable normal estandarizada.
 
 Coeficiente de Asimetría: As   

2 e
 D2
 e
 D2
1. Este modelo tiene una fuerte
3
asimetría positiva, tal como se visualiza en la gráfica.
 Coeficiente de Kurtosis: Ku e
 4D2
2e
 3D2
3e
 2D2
3. Es una distribución
4
leptocúrtica.
lnxm 
 Expectativa Parcial Izquierda: H (x/m;D) D , observe el lector que se
LN  D 
utiliza, para su cálculo, la función de distribución de probabilidad acumulada izquierda del
modelo Normal estándar.
Ing. Sergio Aníbal Dopazo Página 101 de 120

Página 102 de 120 Ing. Sergio Aníbal Dopazo