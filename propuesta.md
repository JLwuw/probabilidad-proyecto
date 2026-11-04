

Simulación de estrategias óptimas para obtener 
recompensas en una misión de dificultad creciente 
Introducción 
Este proyecto se basa en una situación que surgió dentro de un videojuego. Gran parte del 
juego consiste en completar misiones que otorgan recompensas aleatorias. Entre los 
diferentes tipos de misiones existen las misiones infinitas (endless), en las que, en lugar de 
salir una vez completado el objetivo, el jugador tiene la opción de repetir el mismo objetivo 
múltiples veces para obtener recompensas adicionales. Sin embargo, cada repetición 
aumenta la dificultad de la misión, por lo que el tiempo necesario para completarla también 
aumenta. Eventualmente, llega un punto en el que continuar con la misión deja de ser 
conveniente debido al tiempo que toma completarla, por lo que es necesario salir y 
comenzar nuevamente. Pero salir de la misión y empezar de nuevo también implica un 
costo de tiempo 
A partir de esta situación surge la siguiente pregunta: si un jugador necesita conseguir una 
cantidad determinada de ciertas recompensas, ¿cuál es la mejor estrategia para obtenerlas 
en el menor tiempo posible? En este proyecto se utilizará una simulación para comparar 
diferentes estrategias y determinar cuál minimiza el tiempo necesario para alcanzar una 
meta de recompensas. 
Pregunta de investigación 
¿Cuántas repeticiones consecutivas de una misión conviene realizar antes de reiniciarla 
para minimizar el tiempo necesario para obtener una cantidad determinada de 
recompensas? 
Hipótesis 
Se espera que exista un número óptimo de repeticiones consecutivas. Realizar muy pocas 
repeticiones aumentaría la frecuencia con la que se debe pagar el tiempo de reinicio, 
mientras que realizar demasiadas aumentaría considerablemente el tiempo necesario para 
completar las repeticiones más difíciles. 
Variables de entrada 
●  Función de tiempo por repetición: dado el número de repetición, determina cuánto 
tiempo toma completar la repetición. 
●  Distribución de recompensas: determina aleatoriamente las recompensas 
obtenidas en cada repetición. 
●  Tiempo de reinicio: tiempo necesario para salir y volver a comenzar la misión. 
●  Estrategia: número máximo de repeticiones consecutivas que se realizarán antes 
de reiniciar la misión. 
●  Recompensas objetivo: cantidad de cada recompensa que el jugador desea 
obtener. 
●  Número de simulaciones: cantidad de veces que se repetirá el experimento para 
cada estrategia. 
Método 
Para cada estrategia se realizarán múltiples simulaciones. En cada simulación, el programa 
ejecutará repetidamente la misión y generará aleatoriamente las recompensas obtenidas. El 
tiempo de cada repetición se acumulará junto con el tiempo necesario para reiniciar la 
misión cuando se alcance el número máximo de repeticiones establecido por la estrategia. 
La simulación continuará hasta que se hayan obtenido todas las recompensas objetivo. El 
tiempo total necesario se registrará como el resultado de esa simulación. 
Después de realizar un número suficientemente grande de simulaciones para cada 
estrategia, se compararán sus resultados. 
Variables de salida 
La principal variable de salida será: 
●  Tiempo total necesario para alcanzar las recompensas objetivo. 
También se analizarán otras variables, como: 
●  Tiempo promedio por estrategia. 
●  Variabilidad del tiempo necesario. 
●  Número promedio de misiones realizadas. 
●  Número total de repeticiones realizadas. 
●  Cantidad de recompensas adicionales obtenidas por encima de la meta. 
Finalmente, se compararán las diferentes estrategias para determinar cuál presenta el 
menor tiempo promedio para alcanzar las recompensas deseadas. 
 