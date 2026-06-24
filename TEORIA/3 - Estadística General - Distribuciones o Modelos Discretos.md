“Estadística General” Variables Aleatorias Discretas – Modelos de Probabilidad
VARIABLES ALEATORIAS y DISTRIBUCIONES O MODELOS DE PROBABILIDAD
El concepto de una variable aleatoria nos permite pasar de los resultados experimentales a
una función numérica de los resultados. Una variable aleatoria es una regla bien definida para asignar
valores numéricos a todos los resultados posibles de un experimento o fenómeno aleatorio (regla
mediante la cual a cada uno de los resultados de un experimento se le asocia un número). También
se la puede definir como una descripción numérica del resultado de un experimento (la variable
aleatoria asocia un valor numérico con cada resultado posible). Por lo tanto se puede resumir que una
variable aleatoria es una regla de asociación. El valor numérico de la variable aleatoria depende del
resultado del experimento.
La variable aleatoria: Primero es variable porque son posibles diferentes valores numéricos.
Segundo es aleatoria porque el valor observado depende de cuál de los posibles resultados
experimentales aparezca, y, además, porque involucra la probabilidad de los resultados del espacio
muestral. La variable aleatoria es una función de valor real definida sobre el espacio muestral, de
manera que transforma todos los posibles resultados del espacio muestral en cantidades numéricas.
Se pueden definir variables aleatorias cuyos números de posibles valores es finito, o variables
aleatorias cuyos valores son infinitos (sean contables o no), ya que una variable aleatoria es una
caracterización cuantitativa de los resultados de un espacio muestral. Dependiendo de los valores
numéricos que asume, las variables aleatorias se pueden clasificar en variables aleatorias discretas
y variables aleatorias continuas. Cabe aclarar que las variables aleatorias son discretas o
continuas por su carácter intrínseco y no por como se las observa. Para ser rigurosos, para el caso
continuo, el conjunto infinito debe ser no numerable; porque si fuera numerable, la variable, desde un
punto de vista matemático estricto, sería discreta. Ello no obstante, cuando un dominio tiene muchos
valores posibles, se le asocia en la práctica un modelo o distribución continua.
VARIABLES ALEATORIAS DISCRETAS
Una variable aleatoria “r”, es discreta si el número de valores que puede tomar es contable
(ya sea finito o infinito), y si éstos pueden arreglarse en una secuencia que corresponde con los
enteros positivos. En general, todo lo que se quiere expresar de manera contable (cantidad de
unidades defectuosas, cantidad de vehículos que arriban o parten, etc.), es una variable aleatoria
discreta.
En resumen, una variable aleatoria es discreta si su conjunto de valores posibles es un
conjunto discreto. Un conjunto es discreto si está formado por un número finito de elementos, o si sus
elementos se pueden enumerar en secuencia de modo que haya un primer elemento, un segundo
elemento, un tercer elemento, y así sucesivamente, en la lista. O sea que cada fenómeno aleatorio
genera su propia variable.
En el capítulo sobre procesamiento de los datos se estudió la forma de condensar la
información contenida en una muestra o población. Para una variable discreta, la forma más simple
de hacerlo era asignar a cada valor posible de la variable la frecuencia absoluta o relativa
correspondiente.
Cabe destacar que toda variable aleatoria discreta “r” tiene un dominio bien definido entre
valores extremos: mínr Máx
Si consideramos ahora un valor particular “r” de la variable aleatoria como un acontecimiento
aleatorio, es indudable que su frecuencia relativa resulta una medida experimental de la probabilidad
de su ocurrencia. Es posible entonces asociar a cada valor de “r” (variable aleatoria discreta) una
Ing. Sergio Aníbal Dopazo Página 39 de 120

probabilidad, obteniéndose entonces la denominada “Función de Probabilidad” (o función
puntual de probabilidad” o función masa de probabilidad”) de la variable aleatoria considerada.
Una función de probabilidad (también llamada probabilidad puntual) P(r)P(VA r), es
una función que indica (o bien calcula) la probabilidad de que la variable aleatoria discreta en cuestión
tome un valor exactamente igual a “r”. Es una función tal que se cumplen dos condiciones:
Primera condición: P(r) P(VA r) 0  para todo "r"
Máx
Segunda condición:   Pr 1
rmín
La segunda condición refleja el hecho que el conjunto de acontecimientos correspondientes a
los distintos valores de la variable aleatoria “r” es una partición de un “Espacio Muestral”.
Los pares ordenados  r;P(r)  dan la distribución de la variable aleatoria. La distribución de
probabilidad para una variable aleatoria discreta es una realización mutuamente excluyente de todos
los resultados numéricos posibles para esa variable aleatoria, de modo tal que la probabilidad de
ocurrencia se relacione en particular con cada resultado. Estos valores de “P(r)”, se pueden asignar
de manera subjetiva y/o arbitraria (aplicando las reglas de cálculo de probabilidades); o bien usando
modelos matemáticos de comportamiento aleatorio (razonamiento analítico).
En el razonamiento analítico, el analista parte de algunas suposiciones y deduce
matemáticamente la expresión de la función “P(r)”. En la asignación subjetiva y/o arbitraria, se utiliza
cuando no es posible aplicar un modelo matemático o bien no se puede realizar la experimentación
correspondiente; es un recurso terminal y los valores de “P(r)”, se especifican de acuerdo a nuestro
sentimiento o con la indicación de la persona que mejor conoce el fenómeno en estudio y puede
darnos una buena información; la utilidad de este procedimiento está dada por la razonable
confiabilidad de la información disponible.
Veamos algunos ejemplos de asignación subjetiva:
Ejemplo 1: Al tirar un dado me interesa saber el número que va a salir. Entonces la Variable
Aleatoria “r” es: r = número que sale al tirar un dado equilibrado. El dominio
de la variable aleatoria es: 1r6. Su distribución de probabilidades se
visualiza en la siguiente tabla:
r 1 2 3 4 5 6
P(r)
1 1 1 1 1 1
6 6 6 6 6 6
En este ejemplo vemos como los pares ordenados  r;P(r)  conforman un espacio
muestral y se cumplen las dos condiciones de la función de probabilidad. Es una
asignación subjetiva porque suponemos que el dado está equilibrado, ya que si el
dado no estaría equilibrado y lo suponemos cargado de manera proporcional a su
cara, la distribución de probabilidades sería:
Página 40 de 120 Ing. Sergio Aníbal Dopazo

“Estadística General” Variables Aleatorias Discretas – Modelos de Probabilidad
r 1 2 3 4 5 6
P(r)
1 2 3 4 5 6
21 21 21 21 21 21
También vemos como los pares ordenados  r;P(r)  conforman un espacio
muestral y se cumplen las dos condiciones de la función de probabilidad.
Ejemplo 2: Al tirar dos dados me interesa saber el número resultante de la suma de las
caras que van a salir. Entonces la variable aleatoria “r” es: r = suma de las
caras de dos dados equilibrados. El dominio de la variable aleatoria es:
2r12. Su distribución de probabilidades se visualiza en la siguiente tabla:
r 2 3 4 5 6 7 8 9 10 11 12
P(r)
1 2 3 4 5 6 5 4 3 2 1
36 36 36 36 36 36 36 36 36 36 36
Los pares ordenados  r;P(r)  conforman un espacio muestral y se cumplen las
dos condiciones de la función de probabilidad. También es una asignación
subjetiva porque suponemos que los dados están equilibrados y además hemos
usado para el resultado de la función de probabilidad, las reglas del cálculo de
probabilidades (que fueron desarrolladas en el capítulo anterior).
A las distribuciones tipo del ejemplo 1 se las denomina distribuciones uniformes discretas o
bien distribuciones rectangulares, y, a las distribuciones tipo del ejemplo 2 se las denomina
distribuciones triangulares. Se ilustrará mejor en el gráfico del polígono de probabilidad.
1
6
Ejemplo 1
Ing. Sergio Aníbal Dopazo Página 41 de 120

6
36
5
36
4
36
3
36
2
36
1
36
Ejemplo 2
Así como en el procesamiento de datos, para algunas aplicaciones en general, se utilizan las
Frecuencias Acumuladas; en variables aleatorias se utilizan probabilidades acumuladas, por lo que
es conveniente definir a las Funciones de Distribución de Probabilidad.
r
 Función de Distribución: F(r)P(VAr) P(r), calcula la probabilidad de que la
rmín
variable aleatoria en cuestión tome un valor específico menor o igual que “r”. En muchos
Máx
casos también se utiliza: G(r)P(VAr)P(r), calcula la probabilidad de que la
r
variable aleatoria en cuestión tome un valor específico mayor o igual que “r”. Por lo que a
la primera se la denomina función de probabilidades acumuladas izquierda y a la
segunda función de probabilidades acumuladas derecha.
 Se cumple: F(r)G(r) 1P(r)
De manera que podemos definir las siguientes relaciones funcionales:
 P(r) F(r)F(r 1)  G(r)G(r 1)
 F(r) 1G(r 1), y G(r) 1F(r 1)
B
 P(Ar B)P(r)F(B)F(A1)G(A)G(B1)
rA
El lector verá como se cumplen las funciones de probabilidad y sus relaciones en los ejemplos
desarrollados anteriormente.
Página 42 de 120 Ing. Sergio Aníbal Dopazo

“Estadística General” Variables Aleatorias Discretas – Modelos de Probabilidad
PARÁMETROS y CARACTERÍSTICAS de las VARIABLES DISCRETAS
Al igual que en el procesamiento de datos se pueden definir los siguientes valores
característicos:
 Moda o Modo: Mo r ; es el valor de la variable aleatoria cuya probabilidad de ocurrencia
o
es máxima. P  r  Máxima.
o
 Mediana: Mer ; es el valor de la variable aleatoria tal que se cumplan las siguientes
e
condiciones: F  r  0,5 y F  r   0,5.
e1 e
Máx
 Esperanza Matemática o Valor Medio: E(r)

rP(r)

; (suele denominarse valor
rmín
esperado de la variable o MEDIA), es el valor que toma el promedio de la variable
aleatoria después de infinitas observaciones. En el estudio de las funciones teóricas de
probabilidad, el valor medio es, generalmente, el parámetro más importante. Si de un
proceso aleatorio se extrae una muestra, el promedio de la misma es una medida
experimental de la esperanza matemática de la variable aleatoria, en la misma forma en
que la frecuencia relativa lo es de la probabilidad. La esperanza no es una función de “r”,
no depende de un valor particular de la variable, sino que es una característica general de
la distribución.
 Varianza: V(r) 2     Máx r2 P(r)      2  ; es el valor esperado del cuadrado de las
 
rmín
desviaciones de la variable aleatoria respecto a su esperanza matemática. Mide la
aleatoriedad misma de la variable, porque nos indica cuan dispersa puede ser la
distribución. Esta característica es utilizada de manera usual para medir la dispersión de la
variable.
 Propiedades matemáticas de la Esperanza Matemática y de la Varianza. Sean “x” e “y”
dos variables aleatorias independientes, y, “a” y “b” dos constantes, se demuestran las
siguientes propiedades en la combinación algebraica de dichos elementos:
R  axyb    a  b ;  2  a2 2  2
R x y R x y
R  xy      ;  2   2 2  2 2  2 2
R x y R x y x y y x
Estas propiedades se cumplen en cualquier tipo de variable aleatoria independiente, ya
sea discreta (como en este caso) o sea continua (como veremos más adelante).
Si las variables aleatorias “x” e “y”, no son independientes, las propiedades de la
varianza (en la combinación algebraica de estas) cambian. Para desarrollar la varianza,
debemos introducir el concepto de covarianza, ésta es una medida de dispersión conjunta
de dos variables aleatorias.
 Desvío Standard: D(r)   2 ; (Desvío Estándar, Desvío Típico o Dispersión), es el
valor que mide la dispersión de los valores que toma la variable respecto a la esperanza
matemática.
Ing. Sergio Aníbal Dopazo Página 43 de 120


 Coeficiente de Variación: Cv 100; (o Dispersión Relativa) expresado en forma

porcentual, con el mismo concepto visto en el procesamiento de datos. Cabe destacar que
esta característica, no es muy importante en las variables aleatorias discretas; pero en el
caso de las variables aleatorias continuas, como veremos más adelante, esta
característica adquiere vital importancia.
Máx 
 P(r)r3
 Coeficiente de Asimetría: As   rmín ; (es una característica de forma),
3 3
con el mismo concepto visto en el procesamiento de datos.
Cabe aclararas que si este coeficiente es mayor que cero, la distribución tiene asimetría
positiva, en cambio, si es menor que cero la distribución tiene asimetría negativa. Si el
coeficiente es nulo, diremos que la distribución es simétrica y, en general, se cumple la
propiedad de este tipo de distribuciones (Modo = Mediana = Esperanza Matemática).
Debemos señalar que el hecho que este coeficiente sea nulo, no implica necesariamente
que la distribución sea simétrica y puede no cumplirse la propiedad.
Máx 
 P(r)r4
 Coeficiente de Kurtosis: Ku  rmín ; (o Coeficiente de Aplastamiento o
4 4
de Agudeza) es una característica de forma, con el mismo concepto visto en el
procesamiento de datos.
EXPECTATIVA PARCIAL
En muchos problemas prácticos, especialmente aquellos problemas de decisión en que
aparecen costos o ganancias con un número finitos de discontinuidades, resulta útil la definición de la
expectativa matemática parcial de la variable aleatoria o de una función de la misma.
La necesidad de la expectativa matemática parcial aparece cuando se requiere calcular la
esperanza matemática de una función de una variable aleatoria tal que, ella misma o su derivada
tiene un número finito de discontinuidades.
Esta se aplica como un poderoso procedimiento de análisis que permite resolver un conjunto
importante de problemas, en general de naturaleza económica. Es una herramienta estadística de
decisión de suma utilidad en el cálculo de valores esperados de variables económicas atípicas. La
idea de esta aplicación de las esperanzas matemáticas parciales fue propuesta por el estadístico
Robert Schlaifer y el economista Howard Raiffa en sus obras (1967).
El uso de estas expectativas matemáticas parciales tiene aplicación en variables con puntos
de corte o bien variables cuya función es lineal a tramos; o bien variables que son funciones
condicionales de una variable aleatoria simple. Permite estudiar o calcular los valores esperados de
este tipo de variables aleatorias y obtener sus valores óptimos, también puedo calcular la famosa
curva “A-B-C” (la cual realiza una clasificación de elementos en un cierto orden de importancia
respecto de un cierto criterio). Otro uso aparece cuando de una variable aleatoria no se quiera
estudiar todo el dominio, de manera que tenemos distribuciones truncadas. Algunos ejemplos:
Página 44 de 120 Ing. Sergio Aníbal Dopazo

“Estadística General” Variables Aleatorias Discretas – Modelos de Probabilidad
 En una obra civil, la empresa constructora tiene un plazo de n días para concluirla. Si se
atrasa, tiene una penalización de b U$s/día y si se adelanta recibe un premio de c U$s/día.
 Se desea estipular el salario promedio de los individuos que ganan menos que el salario
mínimo vital y móvil.
 Los rollos de tela de 100 metros pueden tener cierta cantidad de fallas, si el número de fallas
es menor que a, el rendimiento tiene un costo y si el número de fallas es mayor que a, el
rendimiento tiene otro costo.
 La demanda de camisas en temporada es variable. Si la empresa compra un lote de x
camisas y las vende a todas tiene un determinado beneficio; pero si le sobran, el remanente
se debe vender a otro precio
A la esperanza matemática (que denominaremos TOTAL, porque tiene en cuenta a todo el
dominio de la variable), que es el valor que toma el promedio después de infinitas observaciones al
darse todos los valores posibles de la variable aleatoria en cuestión, la habíamos definido:
Máx
 Esperanza Matemática Total: E(r)   rP(r) 
rmín
Al igual que las funciones de distribución de probabilidad, que se interpretan como una parte
del espacio muestral, las expectativas parciales se pueden interpretar (de manera matemática) como
una parte de la esperanza matemática, de modo que a la misma la podemos dividir en partes.
Entonces definimos:
r
 Expectativa Parcial Izquierda: H(r)  rP(r) . Hacemos el cálculo tomando en cuenta
rmín
los valores de la variable aleatoria menores o iguales que el valor “r” en cuestión (o sea a
la izquierda de “r”).
Máx
 Expectativa Parcial Derecha: J(r)  rP(r) . Hacemos el cálculo tomando en cuenta los
r
valores de la variable aleatoria mayores o iguales que el valor “r” en cuestión (o sea a la
derecha de “r”).
Como la sumatoria es un operador matemático lineal tenemos:
r Máx Máx


rP(r)



rP(r)



rP(r)

 E(r)
rmín rr1 rmín
Observemos que la primer sumatoria corresponde a la expectativa parcial izquierda de los
valores de la variable aleatoria menores o iguales que “r”; y la segunda sumatoria corresponde a la
expectativa parcial derecha de los valores de la variable aleatoria mayores o iguales que “r+1”. De
manera que podemos deducir lo siguiente:
  H(r)J(r1)  J(r)H(r1), se demuestra que una expectativa se puede obtener a
partir de la otra.
Ing. Sergio Aníbal Dopazo Página 45 de 120

Si quisiéramos obtener la expectativa en un punto o bien en un intervalo de la variable, las
expresiones son:

r
|     |     |     |     |     |   |     |    |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  Expectativa  Puntual:  E (r) rP(r) rP(r).  Para  un  valor  de  la  variable  aleatoria
p
rr
exactamente igual que “r”.

B
Expectativa Parcial en un rango: EAr B  . Tomando en cuenta los valores
|    |     |     |     |     |     |     |     | rP(r) |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- |
rA
de la variable aleatoria comprendidos entre “A” y “B”. Siendo estos pertenecientes al
dominio de la variable aleatoria “r” en cuestión. También se puede calcular mediante
 
|     | E ArB | H(B)H(A1)J(A)J(B1).  |     |     |     |     |     |     |     |     |     |     |
| --- | ------- | -------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Ejemplo: Tomemos en cuenta la variable que surge al tirar un dado y observar el número que sale. La
distribución de la variable aleatoria con sus funciones de probabilidad, se visualizan en la
tabla de la página 41. El dominio de la variable es 1r6. Recordemos el cálculo de la
esperanza matemática de esta variable aleatoria:

6
|     |         |     |      |    | 1   | 1       | 1   | 1   | 51 | 1   | 21 |       |
| --- | ------- | --- | ------ | --- | --- | ------- | --- | --- | ---- | --- | --- | ----- |
|     | E(r) |     | rP(r) | 1 |     | 2 3 |     | 4 |      | 6 |     | 3,5  |
|     |         |     |        |     | 6   | 6       | 6   | 6   |      | 6 6 | 6   |       |
r1

  Calculemos la expectativa parcial izquierda de 3, o sea para r3

3
|     |       |   |       | 1   |     | 1   | 1 6 |     |     |     |     |     |
| --- | ----- | --- | ------ | --- | --- | --- | ---- | --- | --- | --- | --- | --- |
|     | H(3) |     | rP(r) | 1 | 2 | 3 |      | 1  |     |     |     |     |
|     |       |     |        |     | 6   | 6   | 6    | 6   |     |     |     |     |
r1

  Calculemos la expectativa parcial derecha de 4, o sea para r4

6
|     | J(4) |   | rP(r)  |  4 1 | 51 | 61 | 15 | 2,5 |     |     |     |     |
| --- | ----- | --- | -------- | ------ | ---- | ---- | --- | ---- | --- | --- | --- | --- |
|     |       |     |          |        | 6    | 6    | 6   | 6    |     |     |     |     |
|     |       | r4 |          |        |      |      |     |      |     |     |     |     |

  Si realizamos la suma de las dos expectativas anteriores, tenemos comprendido al total del
espacio muestral:

|                    |     |     |   | 3      |   | 6      |   6 |        |  6 | 15 21 |             |     |
| ------------------ | --- | --- | --- | ------ | ----- | ------ | ------ | ------ | --- | ------ | ----------- | --- |
|   H(3)J(4)E(r) |     |     |    | rP(r) |       | rP(r) |       | rP(r) |    |       | 12,53,5  |     |
|                    |     |     |     |        |       |        |        |        | 6   | 6      | 6           |     |
|                    |     |     | r1 |        |       | r4    | r1    |        |     |        |             |     |

  Veamos  de  otra  manera:  calculemos  la  expectativa  parcial  izquierda  de  2;  luego  la
expectativa parcial entre 3 y 5; y luego la expectativa puntual de 6.

| 2   |     |     |     |     |     |     |     | 5   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
H(2)  rP(r)  1 1 2 1 3 0,5;  E3r 5  rP(r)  3 1 4 1 5 1 12 2;
|     |     | 6   | 6   | 6   |     |     |     |     |     | 6   | 6   | 6 6 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r1 |     |     |     |     |     |     |     | r3 |     |     |     |     |
6
E (6)  rP(r)  6 1 6 1. Denotemos que todas son una parte del dominio completo de la
6 6
p
r6
variable aleatoria que si las sumamos nos da la esperanza matemática.

| Página 46 de 120  |     |     |     |     |     |     |     |     |     | Ing. Sergio Aníbal Dopazo  |     |     |
| ----------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------------------------- | --- | --- |

“Estadística General”  Variables Aleatorias Discretas – Modelos de Probabilidad

|     |   H(2)E3r |  5E (6) | 3 12 6 |  21  0,521 | 3,5    |     |
| --- | ------------ | ----------- | -------- | --------------- | -------- | --- |
|     |              |             | 6 6      | 6 6             |          |     |
p

ESPERANZA MATEMÁTICA TRUNCADA (o PROMEDIOS TRUNCADOS)

  Una aplicación sencilla, práctica e intuitiva de las expectativas parciales es el cálculo de los
promedios truncados. Imaginemos, en el ejemplo del dado, que tiramos infinitas veces el dado y
solamente promediamos los valores obtenidos en un rango de la variable aleatoria, sin considerar al
resto de los valores observados. A dicho procedimiento se denomina truncamiento de la variable
aleatoria (el truncamiento de una variable consiste en eliminar un intervalo de su dominio); por lo
tanto el promedio obtenido solamente refiere a una parte de los valores observados descartando al
resto de los otros valores obtenidos. El cálculo de estos promedios se denota por medio de las
siguientes expresiones:

H(r)
  Promedio Truncado Izquierdo:    ; realizamos un truncamiento a la izquierda
|     |     |     | T(VAr) | F(r) |     |     |
| --- | --- | --- | ------- | ---- | --- | --- |
(eliminamos valores de la variable aleatoria mayores que el valor “r”). O sea que tomamos
en cuenta solamente los valores de la variable aleatoria menores o iguales que el valor
“r”.

J(r)
  Promedio Truncado Derecho:    ; realizamos un truncamiento a la derecha
T(VAr)
G(r)
(eliminamos valores de la variable aleatoria menores que el valor “r”). O sea que tomamos
en cuenta solamente los valores de la variable aleatoria mayores o iguales que el valor “r”.

|     |                                    |     |          | H(B)H(A1) | J(A)J(B1) |               |
| --- | ---------------------------------- | --- | -------- | ----------- | ----------- | ------------- |
|     |   Promedio Truncado a dos Colas:  |     |         |            |            | ; realizamos  |
|     |                                    |     | T(ArB) | F(B)F(A1) | G(A)G(B1) |               |
un truncamiento a la izquierda y a la derecha (eliminamos valores de la variable aleatoria
menores que “A” y mayores que “B”). O sea que tomamos en cuenta solamente los
valores de la variable aleatoria comprendidos en un rango del valor “r”. También se puede
|     |                                             |     |     | EAr          | B |     |
| --- | ------------------------------------------- | --- | --- | -------------- | --- | --- |
|     | calcular mediante la siguiente expresión:  |     |     |               | .   |     |
|     |                                             |     |     | T(ArB) P(Ar | B) |     |

Ejemplo: Tomando a la variable aleatoria que surge al observar el número que sale en un dado
equilibrado al tirarlo de marea azarosa.

  Si  solamente  tenemos  en  cuenta  a  los  valores  de  la  variable  r3,  truncamiento  a  la
izquierda, y eliminamos los valores r4; intuitivamente podemos deducir que el promedio de los
valores 1; 2 y 3 es igual que 2. Confirmemos mediante el uso de la ecuación correspondiente:

6
|     |       |     |     | H(3)     | 6 6 |     |
| --- | ----- | --- | --- | -------- | ---- | --- |
|     |       |     |    |        | 2   |     |
|     |       |     |     | T(r3) 3 | 3    |     |
F(3)
6

  Si solamente tenemos en cuenta a los valores de la variable r4, truncamiento a la derecha,
y eliminamos los valores r3; intuitivamente podemos deducir que el promedio de los valores 4; 5 y
6 es igual que 5. Confirmemos mediante el uso de la ecuación correspondiente:

| Ing. Sergio Aníbal Dopazo  |     |     |     |     | Página 47 de 120  |     |
| -------------------------- | --- | --- | --- | --- | ----------------- | --- |

15
|     |     |     |     |     |     |     | J(4) | 6   |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- |
|     |     |     |     |     |    |    |     | 15 | 5  |     |
3
|     |     |     |     |     |     | T(r4) | G(4) | 3   |     |     |
| --- | --- | --- | --- | --- | --- | ------ | ---- | --- | --- | --- |
6

Si solamente tenemos en cuenta a los valores de la variable  3r 5, truncamiento a dos
colas, y eliminamos los valores  r2 y los valores  r6; intuitivamente podemos deducir que el
promedio de los valores 3; 4 y 5 es igual que 4. Confirmemos mediante el uso de la ecuación
correspondiente:

|     |          |           |           |     | 15  | 3    | 18  | 6   | 12  |      |
| --- | -------- | --------- | --------- | --- | --- | ---- | --- | --- | --- | ---- |
|     |          | H(5)H(2) | J(3)J(6) |     |     |     |     |    |     | 12   |
|     |          |           |           |     |     | 6    | 6 6 | 6   | 6   |      |
|     |         |          |          |     |    |      |    |     |   |  4  |
|     | T(3r5) | F(5)F(2) | G(3)G(6) |     |     | 5 2 | 4   | 1   | 3   | 3    |

|     |     |     |     |     |     | 6 6 | 6   | 6   | 6   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

  Las  aplicaciones  mencionadas  al  principio  (variables  atípicas,  variables  condicionalmente
lineales a tramos, etc.), las veremos en el desarrollo de cada uno de los modelos correspondientes.

|                   |     |     |     |     |     |     |     |     |                            |     |
| ----------------- | --- | --- | --- | --- | --- | --- | --- | --- | -------------------------- | --- |
| Página 48 de 120  |     |     |     |     |     |     |     |     | Ing. Sergio Aníbal Dopazo  |     |

“Estadística General” Variables Aleatorias Discretas – Modelos de Probabilidad
MODELOS (o DISTRIBUCIONES de PROBABILIDAD) de VARIABLES ALEATORIAS DISCRETAS
Para estudiar los modelos correspondientes a las variables aleatorias discretas, primero
debemos introducirnos en los Procesos Físicos de Observación. Se reconocen en la naturaleza, en
forma general, tres procesos bien diferenciados entre si: “El proceso de Bernoulli”, “El proceso
Hipergeométrico” y “El proceso de Poisson”.
En la definición de los procesos como también en el estudio de las variables aleatorias
discretas, los parámetros del proceso o de la variable aleatoria correspondiente son un elemento
importante. Se define como parámetro al dato o característica que se considera como imprescindible
y orientativo para lograr evaluar o valorar una determinada situación. A partir de un parámetro, una
cierta circunstancia puede comprenderse. Un parámetro estadístico es aquel formado por una función
establecida sobre los valores numéricos de una variable aleatoria; es un valor que permite modelizar
una situación real o una población específica.
PROCESO DE BERNOULLI (Jacques Bernoulli, 1654 – 1705):
La referencia bibliográfica fue desarrollada en el capítulo de probabilidades.
El proceso de Bernoulli es un proceso físico de repeticiones de un determinado experimento
en el cual observamos la ocurrencia o no de un determinado evento. Estos experimentos dan lugar a
ensayos independientes repetidos, cada uno de los cuales tiene sólo dos resultados posibles: éxito
(ocurre el evento deseado) o fracaso (no ocurre el evento deseado). Las condiciones en las que se
realizan todas las pruebas deben ser iguales. A cada ensayo se llama experimento de Bernoulli.
Los términos “éxito” y “fracaso” son meras etiquetas o convencionalismos; desafortunadamente,
las etiquetas pueden ser engañosas en ocasiones (la búsqueda de la aparición de una pieza
defectuosa, en un proceso productivo de fabricación, puede resultar en algunas aplicaciones, un
éxito). Las pruebas podrían consistir, por ejemplo, en la tirada de una moneda o de un dado, o en la
fabricación de una pieza por una máquina o un proceso productivo.
Diremos que el resultado de una prueba ha sido un éxito si se ha dado el atributo; en caso
contrario hablaremos de un fracaso.
En un proceso de este tipo se cumplen las siguientes condiciones:
I) Independencia de las Pruebas: la probabilidad de un éxito en una prueba, es
independiente de que en la prueba anterior el resultado haya sido un éxito o un fracaso.
II) Estabilidad: En una serie de ensayos, la probabilidad de un éxito y por ende la
probabilidad de un fracaso, permanece constante a lo largo de la misma.
Un Proceso de Bernoulli queda definido por un solo parámetro: La probabilidad de éxito
(p), que es la probabilidad (constante e independiente de las circunstancias) de la ocurrencia de un
éxito. Denotemos que, si la probabilidad de la ocurrencia de un éxito es “p”, la probabilidad de que se
de un fracaso (en cada experimento realizado) es el complemento de “p” (1p), algunos autores a
la probabilidad de fracaso la denominan “q” de manera convencional. Son ejemplos del proceso:
 Tirar un dado equilibrado o viciado (cargado),
 Tirar una moneda,
 Sacar elementos con reposición de una caja,
Ing. Sergio Aníbal Dopazo Página 49 de 120

 Sacar muestras de elementos finitos de un proceso productivo o un proceso de la
naturaleza (muestreo para el control de procesos), o sea la obtención de una pieza
defectuosa o buena de una máquina o de un proceso productivo que fabrica piezas en
serie. En este ejemplo el proceso de Bernoulli se cumple en un período razonable,
 Sacar una muestra de un lote de tamaño infinito,
 Todo proceso de experimentación dónde la probabilidad del éxito buscado sea
constante e independiente de las circunstancias.
En el proceso de Bernoulli intervienen, además del parámetro, dos elementos:
 “n”, que es la cantidad de pruebas o experimentos realizados o bien a realizar (son
valores enteros n1);
 “r”, que es la cantidad de éxitos encontrados o a encontrar (también valores enteros
r 0, y nunca superiores a n).
Dependiendo del elemento que se fija (parametriza), el otro elemento es una variable
aleatoria.
En el caso del proceso productivo o la máquina, la condición de estabilidad, no se cumpliría si
por desgaste o cambio de la herramienta, variara la frecuencia de los defectuosos o bien de los
buenos. En este caso diremos que el proceso es condicionalmente estable, dado que dicha
estabilidad se cumplirá en un determinado intervalo de fabricación.
En el proceso de Bernoulli, podemos reconocer básicamente dos modelos o distribuciones de
probabilidad: “El Modelo Binomial” y “El Modelo de Pascal”, los cuales responden
(recíprocamente) a dos interrogantes:
a) Si se realiza una serie de “n” pruebas, ¿qué probabilidad hay de que ocurran exactamente
“r” éxitos?
b) Si se realiza una serie de pruebas a fin de obtener “r” éxitos, ¿qué probabilidad hay de que
sea necesario llegar a efectuar exactamente “n” pruebas para obtener dichos éxitos?
También en el proceso de Bernoulli, podemos reconocer otros modelos: “El Modelo de
Bernoulli”; “El Modelo Geométrico”, “El Modelo Binomial Negativo” y “El Modelo Multinomial”.
A continuación desarrollaremos los modelos básicos.
A. MODELO o DISTRIBUCIÓN de PROBABILIDAD “BINOMIAL”:
Además del parámetro del proceso de Bernoulli “p” (probabilidad de éxito constante en cada
experimento), se fija el valor de “n” (cantidad de pruebas o experimentos a realizar o bien
realizados), o sea que el valor de “n” se convierte en parámetro. El valor de “n” se fija antes de los
experimentos. Es uno de los modelos (o distribución de probabilidad) discretos más útiles. Sus áreas
de aplicación incluyen inspección de calidad, ventas, mercadotecnia, medicina y otras aplicaciones.
La variable aleatoria es “r” (cantidad de éxitos encontrados o bien a encontrar en “n”
experimentos realizados o bien a realizar).
Parámetros del Modelo: “n” y “p” Variable Aleatoria: “r”
Página 50 de 120 Ing. Sergio Aníbal Dopazo

“Estadística General”  Variables Aleatorias Discretas – Modelos de Probabilidad

| Dominio de la Variable Aleatoria: 0 |     |     |     |     |  r  | n.  |     |     |     |     |
| ----------------------------------- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |

El  modelo  o  función  de  probabilidad,  describe  (o  calcula)  la  probabilidad  de  obtener
exactamente “r” éxitos en “n” experimentos o pruebas realizadas con una probabilidad de éxito
constante “p”, o sea en experimentos de tipo Bernoulli. Su expresión es:

n
|     |      |       |     | n;p) |     | pr 1p(nr) |     | nCrpr | 1p(nr)  |     |
| --- | ---- | ----- | --- | ------ | --- | ---------------- | --- | ------- | ------------ | --- |
|     | P(VA | r)P |     | (r /   |    |                 |     |         |              |     |
|     |      |       |     | b      | r  |                  |     |         |              |     |


Veamos  la  demostración  de  esta  expresión  en  el  siguiente  ejemplo:  Se  arroja  un  dado
equilibrado  buscando  que  salga  un  “As”;  se  quiere  averiguar  la  probabilidad  de  que  salgan
exactamente  2 ases, en  3 tiradas  consecutivas. Observemos que  estamos en presencia de un
proceso de Bernoulli, donde el éxito es la obtención de un as en cada tirada; “p” es la probabilidad de
que salga un as en cada tirada, esta probabilidad es constante en cada tirada y vale p  1 , se
6
deduce  que  la  probabilidad  de  fracaso  (de  que  no  salga  As)  es  q1p  5 ;  el  número  de
6
experimentos  a  realizar  es  n3 y  la  cantidad  de éxitos  deseados  es  r  2.  Si  resolvemos  el

problema con los conceptos desarrollados en el capítulo anterior, deberíamos observar todas las
combinaciones posibles en tres tiradas consecutivas de un dado equilibrado. La cantidad de posibles
resultados es 8 y surge de realizar la siguiente cuenta  23 8, son 2 resultados posibles en cada
tirada y se realizan un total de 3 tiradas, visualicemos en una tabla los posibles resultados:

Primer Tirada  Segunda Tirada  Tercer Tirada  De los 8 posibles resultados, sólo 3 de ellos son
favorables a las condiciones estipuladas
| Éxito    | Éxito    |     |     | Éxito    |     |     |     |     |     |     |
| -------- | -------- | --- | --- | -------- | --- | --- | --- | --- | --- | --- |
| Fracaso  | Fracaso  |     |     | Fracaso  |     |     |     |     |     |     |
Los parámetros son: n3 (cantidad de tiradas) y
| Éxito    | Fracaso  |     |     | Fracaso  |     |                              |     |     |     |     |
| -------- | -------- | --- | --- | -------- | --- | ---------------------------- | --- | --- | --- | --- |
| Fracaso  | Éxito    |     |     | Fracaso  |     | 1  (probabilidad de éxito).  |     |     |     |     |
p 
6
| Fracaso  | Fracaso  |     |     | Éxito  |     |     |     |     |     |     |
| -------- | -------- | --- | --- | ------ | --- | --- | --- | --- | --- | --- |

| Éxito  | Éxito  |     |     | Fracaso  |     |     |     |     |     |     |
| ------ | ------ | --- | --- | -------- | --- | --- | --- | --- | --- | --- |
La variable aleatoria es “r” (cantidad de ases a
| Éxito  | Fracaso  |     |     | Éxito  |     |     |     |     |     |     |
| ------ | -------- | --- | --- | ------ | --- | --- | --- | --- | --- | --- |
obtener en las 3 tiradas), con dominio 0r  3.
| Fracaso  | Éxito  |     |     | Éxito  |     |     |     |     |     |     |
| -------- | ------ | --- | --- | ------ | --- | --- | --- | --- | --- | --- |

De manera que la probabilidad de obtener 2 ases en 3 tiradas se puede calcular con la
siguiente expresión:

|     |                                     |       |       |             |    |             |        |        |         |      |
| --- | ----------------------------------- | ----- | ------- | ----------- | --- | ------------ | ------- | ------- | ------- | ------ |
|     | P(r                                 | 2)P | E       | E F       |    | E F         | E      |  F E  | E      |       |
|     |                                     |       |         | 1 2         | 3   | 1 2          | 3       | 1       | 2       | 3      |
|     | P                                  |  E  | PE   | PF   PE |   | P  F  PE |   PF |   PE |   PE |     |
|     |                                     | 1     | 2       | 3           | 1   | 2            | 3       | 1       | 2       | 3      |
|     | pp(1p)p(1p)p(1p)pp3p2 |       |         |             |     |              |         | (1p)  |         |        |

Analicemos el resultado de la expresión: “p” (la probabilidad de que salga un as en cada
tirada) está elevado a la cantidad de ases deseados  p2; el complemento de esta probabilidad
q1p (la probabilidad de que no salga un as en cada tirada) está elevado a la cantidad de no
ases deseados  1p1  1p y el número 3 (representa el número de combinaciones favorables
dentro de las 8 combinaciones posibles), este número se calcula con la siguiente expresión:

|     |     |     |     |     |   3  C3 | 3 !       | 6    |     |     |     |
| --- | --- | --- | --- | --- | ---------- | --------- | ---- | --- | --- | --- |
|     |     |     |     |     |   2      |  3 C 2  |  3 |     |     |     |
|     |     |     |     |     |  2       | 2 !      | 1! 2 |     |     |     |

| Ing. Sergio Aníbal Dopazo  |     |     |     |     |     |     |     |     |     | Página 51 de 120  |
| -------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------------- |

Ahora demostremos que el modelo es una función de probabilidad, para ello se debe
cumplir con las 2 condiciones: la primera condición se demuestra calculando las P(r), siendo todas
|     |     |     | Máx       |      | n   | n        |    |
| --- | --- | --- | --------- | ---- | --- | ----------- | --- |
|     |     |     |   Pr | 1 |     | 1p(nr) |     |
mayores que cero; la segunda condición    pr , se demuestra de la
|     |     |     |     |     | r0r |    |     |
| --- | --- | --- | --- | --- | ------- | --- | --- |

rmín
siguiente manera:

Partiendo del conocimiento (por el Binomio de Newton) de que:

|     |     |     | n         | n |     |    |     |
| --- | --- | --- | --------- | ---- | --- | --- | --- |
|     |     |     | ABn  |      |     |     |     |
  AiB(ni)
i 

i0

|     |     |     | n   | n |     |    |     |
| --- | --- | --- | --- | ---- | --- | --- | --- |
Llamando Ap y B1p, tenemos:   pr 1p(nr)   p1pn 1n 1
|     |     |     |     |   |     |    |     |
| --- | --- | --- | --- | ---- | --- | --- | --- |
r0r


Quedando demostrado que el modelo Binomial es una Función de probabilidad.

Se cumplen las reglas generales dadas para las variables aleatorias discretas.

  Función de Probabilidad Acumulada Izquierda:

|     |     |     | r n |     |    |     |     |
| --- | --- | --- | ------ | --- | --- | --- | --- |
n;p)
| P(VAr)F | (r  | /   |    px | (1p)(nx) |    |     |     |
| --------- | --- | --- | --------- | ----------- | --- | --- | --- |
|           | b   |     |         |             |     |     |     |
|           |     |     |  x     |             |    |     |     |
x0

  Función de Probabilidad Acumulada Derecha:

|           |     |        | n n  |              |     |    |     |
| --------- | --- | ------ | ------- | ------------ | --- | --- | --- |
|           |     | n;p) |   px | (1p)(nx) |     |     |     |
| P(VAr)G | (r  | /      |      |              |     |     |     |
|           | b   |        | x      |              |     |     |     |
|           |     |        | xr   |              |     |    |     |

|   Moda: Mo | r ; verifica las siguientes condiciones:  |     |     |     |     |     |     |
| ----------- | ------------------------------------------ | --- | --- | --- | --- | --- | --- |
o
|     |     |     |  np1p | Mo | npp  |     |     |
| --- | --- | --- | ------------ | ---- | -------- | --- | --- |

. Para la mayoría de los casos la mediana es la parte entera de np, y
  Mediana: Mer
e
P.E.np
está dada por la siguiente expresión: Me

Para otros casos no hay una expresión plausible para determinarla, por ello también se
deben cumplir las siguientes condiciones:

|     |     |     |            |     |     |          |     |
| --- | --- | --- | ----------- | ---- | --- | ---------- | --- |
|     |     |     | F r 1/n;p | 0,5 | y   | F r /n;p  | 0,5 |
|     |     |     | b e         |      |     | b e        |     |

  Esperanza Matemática: E(r)np

1p
|   Varianza: V(r)2 |     | np |     |     |     |     |     |
| -------------------- | --- | ----- | --- | --- | --- | --- | --- |

12p
|   Coeficiente de Asimetría: As |     |     |    |           |     |     |     |
| ------------------------------- | --- | --- | ----- | --------- | --- | --- | --- |
|                                 |     |     | 3     | np1p |     |     |     |

| Página 52 de 120  |     |     |     |     |     |     | Ing. Sergio Aníbal Dopazo  |
| ----------------- | --- | --- | --- | --- | --- | --- | -------------------------- |

“Estadística General” Variables Aleatorias Discretas – Modelos de Probabilidad
1
 6p1p
 Coeficiente de Kurtosis: Ku  3 . Este coeficiente tiende a 3
4 np1p
cuando “n” tiende a infinito, este resultado traduce la convergencia de la ley Binomial a
la ley Normal. Cabe aclarar que en la ley normal, como veremos en el siguiente capítulo,
este coeficiente es exactamente igual a 3.
 Expectativa Parcial Izquierda:
r  n 
H b (r/n;p)  x0   x   x    px  1p(nx)   npF b (r1/ n1;p)
Este modelo, para ciertas restricciones, puede calcular en forma aproximada al modelo
Hipergeométrico; y puede ser calculado de forma aproximada por el modelo de Poisson o por el
modelo Normal. (Ver las restricciones de aproximación en el capítulo correspondiente, página 118).
B. MODELO o DISTRIBUCIÓN de PROBABILIDAD de “PASCAL”:
Blaise Pascal (Clermont, Francia, 1623 – París, Francia 1662) fue un matemático,
físico, filósofo católico y escritor. Sus contribuciones a las matemáticas y las
ciencias naturales incluyen el diseño y construcción de calculadoras mecánicas,
aportes a la teoría de la probabilidad, investigaciones sobre los fluidos y la
aclaración de conceptos tales como la presión y el vacío. Después de una
experiencia religiosa profunda en 1654, Pascal abandonó las matemáticas y la física
para dedicarse a la filosofía y a la teología.
Además del parámetro del proceso de Bernoulli “p” (probabilidad de éxito constante en cada
experimento), se fija el valor de “r” (cantidad deseada de éxitos a obtener), o sea que el valor de “r”
se convierte en parámetro. El valor de “r” se fija antes de los experimentos.
La variable aleatoria es “n” (cantidad de pruebas o experimentos necesarios para obtener “r”
éxitos deseados). Se debe observar que se van realizando los experimentos hasta obtener los éxitos
deseados (los experimentos paran cuando se encuentra el “r -ésimo” éxito).
Parámetros del Modelo: “r” y “p” (siendo r 1) Variable Aleatoria: “n”
Dominio de la Variable Aleatoria: r n .
El modelo o función de probabilidad, describe (o calcula) la probabilidad de necesitar
exactamente “n” experimentos o pruebas para obtener “r” éxitos deseados con una probabilidad de
éxito constante “p”, o sea en experimentos de tipo Bernoulli. Su expresión es:
n1
P(VA n)P (n / r ;p) pr 1p(nr)
pa  r1  
Por las propiedades del modelo, se puede afirmar la siguiente igualdad:
r
P (n / r ;p) P (r / n;p)
pa n b
Ing. Sergio Aníbal Dopazo Página 53 de 120

Se puede observar, en las siguientes expresiones, la relación matemática con el modelo
Binomial.

Se cumplen las reglas generales dadas para las variables aleatorias discretas.

  Función de Probabilidad Acumulada Izquierda:

|     |     |     |     | n x1 |     |     |    |     |     |     |
| --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- |
;p)
| P(VAn)F | (n  | / r |     |      |  pr | (1p)(xr) |     | G (r / | n;p)  |     |
| --------- | --- | --- | --- | ------ | ----- | ------------ | --- | ------- | ----- | --- |
|           | pa  |     |     |  r1 |      |              |     | b       |       |     |
|           |     |     |     |       |      |              |    |         |       |     |
xr

  Función de Probabilidad Acumulada Derecha:

|           |     |        |       |  x1 |       |              |    |          |         |     |
| --------- | --- | ------ | ----- | -------- | ----- | ------------ | --- | -------- | ------- | --- |
| P(VAn)G |     | (n / r | ;p) |         |  pr | (1p)(xr) |     | F (r1/ | n1;p)  |     |
|           |     |        |       |        |      |              |     |          |         |     |
|           | pa  |        |       | r1     |       |              |     | b        |         |     |
|           |     |        |       | xn     |      |              |    |          |         |     |

Para ambas funciones de distribución se deben usar programas apropiados o bien planillas de
cálculo que tengan esta distribución. Si se quiere usar tablas notemos que las tres funciones tienen
una relación con el modelo Binomial.

  Moda: Mon ; no hay una expresión plausible para determinarla.
o

  Mediana: Men ; no hay una expresión plausible para determinarla, por ello también se
e
deben cumplir las siguientes condiciones:

|     |     |     | F  |  n 1/r;p |     |   0,5 | y F |  n /r;p |   0,5 |     |
| --- | --- | --- | --- | ---------- | --- | ------- | --- | -------- | ------- | --- |

|     |     |     |     | pa e |     |     | pa  | e   |     |     |
| --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- |

r
|   Esperanza Matemática: E(n) |     |     |     |    |     |     |     |     |     |     |
| ------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
p

|                      |     |     | r 1p |     |     |     |     |     |     |     |
| -------------------- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
|   Varianza: V(n)2 |     |    |          |     |     |     |     |     |     |     |
p2

2p
|   Coeficiente de Asimetría: As |     |     |     |   |    |     |     |     |     |     |
| ------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
3 r1p

|     |     |     |     |     |    |     |    |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
p2 6p6
|   Coeficiente de Kurtosis: Ku |     |     |     |     | 3 |     |     |     |     |     |
| ------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

|     |     |     |     | 4   |     | r1p |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- |

  Expectativa Parcial Izquierda:
|     |     |     |     |          | n   |  x1 |       |             |  r        |         |
| --- | --- | --- | --- | -------- | --- | ------- | ----- | ----------- | ---------- | ------- |
|     |     |     | H   | (n/r;p) |    | x     |  pr | 1p(xr) |  F (n1/ | r1;p)  |
|     |     |     |     |          |     |       |      |             |           |         |
|     |     |     |     | pa       |     | r1    |      |             | p pa       |         |
|     |     |     |     |          | xr |        |       |             |           |         |

| Página 54 de 120  |     |     |     |     |     |     |     |     | Ing. Sergio Aníbal Dopazo  |     |
| ----------------- | --- | --- | --- | --- | --- | --- | --- | --- | -------------------------- | --- |

“Estadística General” Variables Aleatorias Discretas – Modelos de Probabilidad
PROCESO HIPERGEOMÉTRICO
El proceso Hipergeométrico es un proceso físico de repeticiones de un determinado experimento
en el cual observamos la ocurrencia o no de un determinado evento. Estos experimentos dan lugar a
ensayos repetidos, los cuales no son independientes entre sí, y, también, al igual que en el proceso
de Bernoulli, tienen cada uno sólo dos resultados posibles: éxito (ocurre el evento deseado) o
fracaso (no ocurre el evento deseado). Las condiciones en las que se realizan todas las pruebas no
son iguales, porque a medida que ocurre un resultado de una prueba, éste condiciona el resultado de
la siguiente prueba.
En un proceso de este tipo se cumplen las siguientes condiciones:
I) Las Pruebas no son independientes: la probabilidad de un éxito en una prueba, está
condicionada por el resultado de la prueba anterior (si fue un éxito o un fracaso, entonces
habrá un éxito o un fracaso menos respectivamente).
II) No Estabilidad: En una serie de ensayos, la probabilidad de un éxito no permanece
constante a lo largo de la misma.
III) Población, Lote o Universo Finito: A diferencia del proceso de Bernoulli (que se da en
una población infinita), este proceso se da en una población acotada o finita.
Un proceso Hipergeométrico queda definido por dos parámetros: total de elementos,
posibles, que intervienen en el experimento a realizar, o tamaño del lote a examinar “N”; y la
cantidad total de éxitos en el total de elementos posibles o en el lote a examinar “R”. Pese a ser
dos parámetros, que para el desarrollo de este capítulo supondremos conocidos, muchas veces los
mismos son desconocidos a los ojos del profesional que trata una problemática basada en este
proceso. Cabe aclarar que en la mayoría de las aplicaciones se suele conocer el tamaño del lote a
examinar “N” pero “R” casi siempre es desconocido.
Son ejemplos del proceso:
 Números salidos en una lotería,
 Sacar elementos sin reposición de una caja,
 Sacar una muestra de un lote de tamaño finito (muestreo para aceptación de un lote),
 Todo proceso de experimentación dónde la probabilidad del éxito buscado en cada
experimento condicione a la probabilidad del éxito del siguiente experimento (o sea
que la probabilidad del éxito no es constante).
Este proceso surgió a partir de la necesidad del control de calidad de lotes acotados. La tendencia
actual es el control de los procesos a los cuales les cabe perfectamente el proceso de Bernoulli. Por
lo tanto este proceso se usa para verificar los supuestos declarados por los fabricantes y/o
proveedores.
En el proceso Hipergeométrico intervienen, además de los dos parámetros, dos elementos:
 “n”, que es la cantidad de pruebas o experimentos realizados o bien a realizar, o mejor
dicho la muestra extraída (son valores enteros n1, y nunca superiores a “N”);
 “r”, que es la cantidad de éxitos encontrados o a encontrar (también valores enteros
r 0, y nunca superiores a “n” ni a “R”).
Ing. Sergio Aníbal Dopazo Página 55 de 120

Dependiendo del elemento que se fija (parametriza), el otro elemento es una variable
aleatoria.
En el proceso Hipergeométrico, podemos reconocer dos modelos o distribuciones de
probabilidad básicos: “El Modelo Hipergeométrico” y “El Modelo de Pascal Hipergeométrico o
Hiper–Pascal”, los cuales responden (recíprocamente) a dos interrogantes:
a) Si se extrae una muestra de “n” elementos de un lote de tamaño “N” conteniendo un total de
éxitos “R”, ¿qué probabilidad hay de encontrar exactamente “r” éxitos en esa muestra?
b) Si se extrae una serie de elementos de un lote de tamaño “N” (conteniendo un total de éxitos
“R”), a fin de encontrar “r” éxitos, ¿qué probabilidad hay de que sea necesario llegar a
extraer exactamente una muestra de “n” elementos para obtener dichos éxitos?
También en el proceso Hipergeométrico, podemos reconocer a otro modelo: “El Modelo
Hipergeométrico Multivariado o Multipergeométrico”.
A continuación desarrollaremos los básicos.
A. MODELO o DISTRIBUCIÓN de PROBABILIDAD “HIPERGEOMÉTRICO/A”
Además de los dos parámetros del proceso Hiergeométrico “N” (tamaño del lote o total de
elementos a experimentar) y “R” (cantidad total de éxitos en el lote o en los elementos a
experimentar), se fija el valor de “n” (cantidad de pruebas o experimentos a realizar o bien
realizados, o sea el tamaño de la muestra a extraer del lote en cuestión), o sea que el valor de “n” se
convierte en parámetro. El valor de “n” se fija antes de las extracciones.
La variable aleatoria es “r” (cantidad de éxitos encontrados o bien a encontrar en “n”
extracciones realizadas o bien a realizar, o sea en la muestra extraída).
Parámetros del Modelo: “n”, “N” y “R” Variable Aleatoria: “r”, siendo rR
Dominio de la Variable Aleatoria: Máx  0;nNR r Mín  n; R .
El modelo o función de probabilidad, describe (o calcula) la probabilidad de obtener
exactamente “r” éxitos en “n” extracciones realizadas o bien en una muestra de un lote de tamaño
“N” que contiene “R” éxitos. Su expresión es:
R NR
  
   
r   nr 
P(VA r)P (r / n;N;R) 
h N
 
 
n
Se cumplen las reglas generales dadas para las variables aleatorias discretas.
 Función de Probabilidad Acumulada Izquierda:
Página 56 de 120 Ing. Sergio Aníbal Dopazo

“Estadística General”  Variables Aleatorias Discretas – Modelos de Probabilidad

|     |           |              |     | R    | NR |     |     |     |     |     |     |
| --- | --------- | ------------ | --- | ------- | ------ | --- | --- | --- | --- | --- | --- |
|     |           |              |     |    |       |   |     |     |     |     |     |
|     |           |              |     |        |       |    |     |     |     |     |     |
|     |           |              |     | r x  | nx |     |     |     |     |     |     |
|     | P(VAr)F | (r / n;N;R) |     |        |        |     |     |     |     |     |     |
|     |           | h            |     |        |        |    |     |     |     |     |     |
N
|     |     |     |     | xmín |   |    |     |     |     |     |     |
| --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
 
|     |     |     |     |   | n |   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

|     |   Función de Probabilidad Acumulada Derecha:  |     |     |     |     |     |     |     |     |     |     |
| --- | ---------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

|     |           |              |     | R     | NR |     |     |     |     |     |     |
| --- | --------- | ------------ | --- | -------- | ------ | --- | --- | --- | --- | --- | --- |
|     |           |              |     |       |       |   |     |     |     |     |     |
|     |           |              |     |       |       |    |     |     |     |     |     |
|     |           |              |     | Máx x | nx |     |     |     |     |     |     |
|     | P(VAr)G | (r / n;N;R) |     |         |        |     |     |     |     |     |     |
|     |           | h            |     |         | N    |    |     |     |     |     |     |
|     |           |              |     | xr      |      |     |     |     |     |     |     |
|     |           |              |     |         |      |    |     |     |     |     |     |
n
|     |     |     |     |   |     |   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Para ambas funciones de distribución se deben usar tablas, programas apropiados o bien
planillas de cálculo que tengan esta distribución.

|     |   Moda: Mo | r :   |     |     |     |     |     |     |     |     |     |
| --- | ----------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
o
|     |     |     | nRNRn1 |       |     |        | nRRn1 |       |     |     |     |
| --- | --- | --- | -------------- | ----- | --- | ------ | ------------ | ----- | --- | --- | --- |
|     |     |     |               |       |     |  Mo |             |       |    |     |     |
|     |     |     |                | N2 |     |        |              | N2 |     |     |     |
|     |     |     |               |       |     |       |             |       |    |     |     |

  Mediana: Mer . No hay una expresión plausible para determinarla, por ello también se
e
deben cumplir las siguientes condiciones:

|     |     |     |     |           |    |       |    |        |      |     |     |
| --- | --- | --- | --- | ---------- | --- | ----- | --- | ------ | ----- | --- | --- |
|     |     |     | F  | r 1/n;N;R |    | 0,5 y | F r | /n;N;R |  0,5 |     |     |
|     |     |     |     | h e        |     |       | h e |        |       |     |     |

R
Esperanza Matemática: Er
|     |    |     |     | n |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
N

|     |     |     | R   |  R Nn |     |     |     |     |     |     |     |
| --- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
  Varianza:  Vr 2 n 1  .  Si  observamos  las  ecuaciones  de  la
|     |     |     | N   |  N N1 |     |     |     |     |     |     |     |
| --- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
esperanza matemática y de la varianza, vemos una similitud con el modelo binomial; salvo
Nn
que en la varianza se agrega un factor de corrección por finitud de la población  ,
N1
este factor tiende a 1 cuando el tamaño del lote “N” tiende a infinito. Cabe aclarar que
cuando los experimentos se realizan con poblaciones de tamaño acotado o finito, siempre
la varianza se ve afectada por este factor. A este factor también se lo llama coeficiente de
exhaustividad.

|     |                                   |     |     |          | N2RN2n |                    |     | N1 |     |     |     |
| --- | --------------------------------- | --- | --- | -------- | ---------------- | ------------------ | --- | ----- | --- | --- | --- |
|     |   Coeficiente de Asimetría: As |     |     |         |                  |                    |     |       |     |     |     |
|     |                                   |     |     | 3 N2 |                  |  nRNRNn |     |       |     |     |     |

|     |   Coeficiente de Kurtosis: Ku |     |     |    |     |     |     |     |     |     |     |
| --- | ------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
4

 N2N1
|     |                            |     |    |                 |     |     | R NR |             |     | 6nNn |    |
| --- | --------------------------- | --- | --- | ---------------- | --- | --- | -------- | ----------- | --- | --------- | --- |
|    |                            |     |     | NN16nNn3 |     |     |          | N2n2Nn2 |     |           |     |
|     |   nRN2N3NRNn |     |    |                 |     |     |          |             |     |           |    |
| 4   |                             |     |   |                  |     | N2  |          |             |     |           |    |


| Ing. Sergio Aníbal Dopazo  |     |     |     |     |     |     |     |     |     | Página 57 de 120  |     |
| -------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------------- | --- |

  Expectativa Parcial Izquierda:
R
|     | H (r/n;N;R)n | F (r1/ | n1;N1;R1)  |     |
| --- | -------------- | -------- | ------------- | --- |
|     | h              | N h      |               |     |

Este modelo, para ciertas condiciones y restricciones, se puede calcular en forma aproximada
por el modelo Binomial. (Ver las restricciones de la aproximación en página 118)

B. MODELO
o  DISTRIBUCIÓN  de  PROBABILIDAD  “PASCAL  HIPERGEOMÉTRICO”  o
“HIPER-PASCAL”

Además de los dos parámetros del proceso Hipergeométrico “N” (tamaño del lote o total de
elementos  a  experimentar)  y  “R”  (cantidad  total  de  éxitos  en  el  lote  o  en  los  elementos  a
experimentar), se fija el valor de “r” (cantidad deseada de éxitos a obtener), o sea que el valor de “r”
se convierte en parámetro. El valor de “r” se fija antes de las extracciones a realizar.

La variable aleatoria es “n” (cantidad de extracciones necesarias o muestra necesaria para
obtener “r” éxitos deseados). Se debe observar que se van realizando las extracciones hasta obtener
los éxitos deseados (las extracciones paran cuando se encuentra el “r -ésimo” éxito).

Parámetros del Modelo: “r”, “N” y “R”, siendo 1rRN

Variable Aleatoria: “n”

Dominio de la Variable Aleatoria: r n NRr.

El  modelo  o  función  de  probabilidad,  describe  (o  calcula)  la  probabilidad  de  necesitar
exactamente “n” extracciones o muestra para obtener “r” éxitos determinada de un lote de tamaño
“N” que contiene “R” éxitos, o sea en experimentos de tipo Hipergeométrico. Su expresión es:

|           |               | R NR   | Nn   | n1       |
| --------- | ------------- | ----------- | ------- | ----------- |
|           |               |      |     |      |
|           |               | r r nr    | Rr   | r1       |
|           |               |           |        |             |
| P(VAn)P | (n / r ;N;R) |            |        |             |
|           | pah           | n N       |         | N         |
|           |               |           |         |           |
|           |               |           |         |           |
|           |               | n         |         | R         |

Se puede afirmar que se cumple la siguiente igualdad:

r
|     | P (n / r ;N;R) | P (r / n;N;R)  |     |     |
| --- | --------------- | --------------- | --- | --- |
|     | pah             | n h             |     |     |

Desarrollemos a continuación las funciones de distribución de probabilidad de este modelo y
sus características (se puede observar, en las siguientes expresiones, la relación matemática con el
modelo Hipergeométrico).

Se cumplen las reglas generales dadas para las variables aleatorias discretas.

  Función de Probabilidad Acumulada Izquierda:
Página 58 de 120  Ing. Sergio Aníbal Dopazo

“Estadística General”  Variables Aleatorias Discretas – Modelos de Probabilidad

|           |     |               |     |    | R NR |     |      |         |     |
| --------- | --- | ------------- | --- | --- | ---------- | --- | ---- | ------- | --- |
|           |     |               |     |     |        |   |      |         |     |
|           |     |               |     |    |         |    |      |         |     |
|           |     |               |     | n r | r xr     |     |      |         |     |
|           |     |               |     |   |          |   |      |         |     |
| P(VAn)F |     | (n / r ;N;R) |     |     |           | G  | (r / | n;N;R)  |     |
|           | pah |               |     | x  | N        |    | h    |         |     |
xr
|     |     |     |     |    |   |    |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
 x 
|     |     |     |     |   |     |   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

  Función de Probabilidad Acumulada Derecha:

|           |     |         |     |       | R NR |     |          |           |     |
| --------- | --- | ------- | --- | ------ | ---------- | --- | -------- | --------- | --- |
|           |     |         |     |        |        |   |          |           |     |
|           |     |         |     |       |         |    |          |           |     |
|           |     |         |     | Máx r | r         | xr |          |           |     |
|           |     | ;N;R) |     |        |          |   |          |           |     |
| P(VAn)G |     | (n / r  |     |        |           |     | F (r1/ | n1;N;R)  |     |
|           | pah |         |     | x     | N        |    | h        |           |     |
|           |     |         |     | xn   |           |   |          |           |     |
 
|     |     |     |     |   | x |   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Para ambas funciones de distribución se deben usar programas apropiados o bien planillas de
cálculo que tengan esta distribución. Si se quiere usar tablas notemos que las tres funciones tienen
una relación con el modelo hipergeométrico.

  Moda: Mon . No hay una expresión plausible para determinarla.
o

  Mediana: Men . No hay una expresión plausible para determinarla, por ello también se
e
deben cumplir las siguientes condiciones:

|     |     |     |     |           |    |       |      |         |     |
| --- | --- | --- | --- | ---------- | --- | ----- | ----- | -------- | --- |
|     |     |     | F  | n 1/r;N;R |    | 0,5 y | F n   | /r;N;R  | 0,5 |
|     |     |     | pah | e          |     |       | pah e |          |     |

r(N1)
|   Esperanza Matemática: En |     |     |     |    |     |     |     |     |     |
| ------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(R1)

|                      |     |      | (r1)(N2) |     |         |     |     |     |     |
| -------------------- | --- | ----- | ------------ | --- | --------- | --- | --- | --- | --- |
|   Varianza: Vn2 |     |   |              |     | 1 2  |     |     |     |     |

|     |     |     |    | (R2) |   |     |     |     |     |
| --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |


  Coeficiente de Asimetría: No hay una expresión plausible para determinarlo.

  Coeficiente de Kurtosis: No hay una expresión plausible para determinarlo.

  Expectativa Parcial Izquierda:

r(N1)
|     |     |     | H (n/r;N;R) |     |       | F  | (n1/ | r1;N1;R1)  |     |
| --- | --- | --- | ------------ | --- | ----- | --- | ----- | ------------- | --- |
|     |     |     | pah          |     | (R1) | pah |       |               |     |

El Proceso de Poisson con sus modelos relacionados será desarrollado más adelante en el
correspondiente capítulo 5 (página 103).

|                            |     |     |     |     |     |     |     |     |                   |
| -------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | ----------------- |
| Ing. Sergio Aníbal Dopazo  |     |     |     |     |     |     |     |     | Página 59 de 120  |

Página 60 de 120 Ing. Sergio Aníbal Dopazo