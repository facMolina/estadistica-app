**Estadística General / Probabilidad y Estadística**

**MODELO NO VALIDO COMO EVALUACION**

*Segundo parcial- 2025*

**Trabaje en todos los ejercicios con 4 cifras significativas después de la coma,** y considere siempre redondear hacia arriba (de esta forma, por ejemplo: 4,11115 se aproxima como 4,1112). Considere representativo un **Coeficiente de Variación menor a 10%.** Escriba todos los procedimientos de forma clara y ordenada, indicando correctamente a que ejercicios e inciso corresponden.

**El tiempo para realizar el examen es de 2:30 hs.** **La aprobación de este requiere de alcanzar 4 puntos o más y contar con puntaje total en por lo menos 6 incisos.** El siguiente examen se corrige con curva bajo el criterio de “mejor alumno posible”, para acceder a ella se deben alcanzar los 7 puntos o más, de caso contrario las notas se calculan sobre el puntaje total. Los incisos que contengan un resultado erróneo, pero cuenten con un desarrollo parcialmente correcto serán calificados según el profesor lo considere. **Mucha suerte.**

**Nombre y Apellido: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_**

**Legajo: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_**

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| **Ejercicio** | **1** | **2** | **3** | **4** | **5** | **Totales** |
| Puntaje |  |  |  |  |  |  |
| Incisos |  |  |  |  |  |  |

Usted acaba de ser seleccionado/a como consultor de ingeniería de software para la creación de una nueva app financiera en una startup. Por esto se le asignaron una serie de trabajos a resolver:

1. Ejercicio teórico. **REPASO DE MANUALES Y NOTAS A CARGO DEL ALUMNO** **(1p)**
2. Para que el ingreso a la aplicación sea más rápido, una vez el usuario ingresa su nombre de usuario en la página principal del servidor comienza a cargar (de manera remota) la primera página visible una vez ingresado. De esta forma, los usuarios sienten que el tiempo de espera es menor y están más satisfechos. Sin embargo, hay algunos usuarios que ingresan su clave sumamente rápido, y ellos aun así deben esperar.
3. Sabiendo que la carga en el servidor tarda 0,8 segundos y si suponemos que el tiempo que se toma un usuario para ingresar su clave sigue una distribución Normal, con un promedio de 0,92 segundos y a su vez conocemos que el 17% de los mismos tarda menos de 0,82458 segundos. ¿Qué porcentaje de usuarios deben esperar, aunque sea algo de tiempo de más una vez ya colocada su clave?
4. Los líderes técnicos están muy interesados en poder bajar la cantidad de usuarios que deben esperar. ¿A qué tiempo debería bajar el nivel de carga para asegurar que el 95% de los usuarios no esperara nada?
5. ¿Qué porcentaje de los usuarios espera entre 0,1 y 0,2 segundos? ¿Cuánto seria la variación en puntos porcentuales de su respuesta si el tiempo de espera aumentase un 5%? Justifique teóricamente porque no es igual. *Recomendación: puede usar un gráfico*
6. Aunque muchos usuarios están muy satisfechos con el rápido ingreso a la app, el depto. De ciberseguridad está preocupado que esto puede poner en riesgo los usuarios frente a ataques de fuerza bruta (donde una máquina ingresa infinitas claves en milésimas de segundos tratando de vulnerar a las cuentas). Para aumentar la seguridad, se decide que, cuando se realicen muchos pedidos de ingreso (con diferentes claves) en poco tiempo se pedirá una validación en dos pasos enviando un código de 3 dígitos vía mail. Una vez se recibe el código los usuarios tendrán un tiempo delimitado para cargarlo antes de que la cuenta se bloquee por un día. Un PM del proyecto propuso que el tiempo máximo sea sesteado en 35 segundos.

A su vez se sabe, que un 15% de los usuarios reciben el código en otro dispositivo, lo que hace que tarden aún más tiempo en ingresar el código.

1. Si usted asume que el tiempo agregado por recibir código en otro dispositivo suma 5 segundos si es un celular o Tablet y 15 segundos se es una PC y que desde que se visualiza el código el tiempo de carga del mismo sigue una distribución Gamma con media de 20 segundos y una varianza de 5 segundos. ¿Qué porcentaje de usuarios se les bloquearía la cuenta antes de llegar a colocar el código?
2. Si considera solo a los usuarios que reciben en el mismo dispositivo, desde que ven el código ¿cuánto tiempo debería asignarse para que el 90% de los usuarios logren colocar el código antes que se bloque la cuenta?
3. Para realizar las transacciones financieras, usualmente la aplicación es inmediata una vez que se aprueba la verificación de fondos (que se puede asumir tarda siempre 1 minuto) y que es el tiempo más común. Sin embargo, algunas transacciones (por temas aleatorios) tardan más. Si se sabe que en promedio se tarda 1,4 minutos y asumiendo que se podría utilizar la distribución Pareto para explicar este proceso.
4. ¿Cuantas transacciones tardan más de 1,44 minutos?
5. ¿Del 50% de las transacciones que más tardan, cuantas tardan más que la media?
6. ¿Cuánto tardan en promedio aquellas que tardan más que la media?
7. Existen otro tipo de transacciones (internacionales) que tienen un tiempo de aprobación más largo de 1,2 minutos (que es su moda) y una media de 1,5. Si se sabe que una transacción tardo más de 1,5 minutos en realizarse, ¿cuál es la probabilidad de que sea una transacción internacional? Asuma que el 20% de las transacciones son internacionales.
8. El financiamiento de la app tiene 2 fuentes. La primera es un fijo por mantener cuentas abiertas, la cual se fija en 24 USD anuales. Por otra parte, se cobra una comisión por operaciones (3%). Se estima que las operaciones de un cliente se distribuyen normalmente donde los montos superan los 584,5824 USD solo un 10% de las veces y la probabilidad de estar por debajo de 400 USD solo un 6,487%.
9. Los jefes del sector de presupuesto quieren saber cuál es el promedio del monto operado por cliente en 12 meses.
10. Si la empresa ahora tiene 350 clientes, ¿cuánto se espera sea la ganancia promedio en 12 meses si no se suman ni restan clientes?
11. Un director de la empresa propone sumar una tercera fuente de ingreso mostrando publicidades. Estas publicidades pagan 3 USD segundo que se muestran. Si para simplificar el modelo, se estima que el tiempo que pasan los usuarios en la app sigue una distribución uniforme de entre 1 y 5 minutos. ¿Cuánto se podría ganar en promedio cada vez que un cliente usa la app? ¿Cómo cambia su respuesta si se sabe que el usuario es del 20% que más tiempo usa la app?