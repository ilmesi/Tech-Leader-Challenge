# Satellites on Fire Challenge
La idea de este desafío es trabajar con una parte de las tecnologías utilizadas en el stack de Satellites on Fire para resolver algunos problemas relevantes para nuestros clientes. Estos son los pasos para poder comenzar el desafío:

1. Clonar este repositorio y guardarlo de forma **privada**.
2. Realizar los desafíos propuestos a continuación.
3. Compartirnos tu repositorio para poder acceder a las respuestas.
4. ¡Contactanos por correo electrónico para poder revisar el desafío!

Además, estamos abiertos a feedback sobre el desafío. ¡Esperemos que les guste!

# Introducción

Recibir información de incendios en tiempo real es muy importante para nuestros clientes, por lo que estamos constantemente trabajando para poder agregar nuevos satélites a nuestra plataforma. Por ello, se lanzó un nuevo satélite geoestacionario *FIRESAT23*, un nuevo satélite de última generación que nos permitirá obtener incendios de todo el mundo.

Para ello, cuenta con una API muy agradable, a la cual se le pueden solicitar los incendios del último día (y de días previos si se quiere también, pero en este caso no será necesario).

¡Ayúdanos a terminar de implementar este nuevo satélite para nuestra plataforma!

## Lenguaje de Programación

Para este desafío, se deberá usar Python 3. Es crucial que se use Python de forma **tipada** (https://docs.python.org/3/library/typing.html), a pesar de que no sea tenido en cuenta en tiempo de ejecución ya que ahorra errores y fomenta las buenas prácticas.

## El Entorno

Para poder resolver el desafío, utilizaremos AWS SAM (Amazon Web Services Serverless Application Model). Este es útil para poder crear, testear y deployar funciones Lambda en la nube de AWS. Esta tecnología es utilizada por nosotros para poder realizar un producto escalable y eficiente, ya que nuestra aplicación tiene una carga de procesamiento de datos elevada. Para más información, está disponible la documentación de AWS SAM en https://docs.aws.amazon.com/serverless-application-model/ y de AWS Lambda en https://docs.aws.amazon.com/lambda/. Además, en el documento [InitializationDetails.md](InitializationDetails.md), se encuentra una breve explicación de como poder usar SAM para testear la aplicación y deployarla (esto último no es necesario para el challenge). Se recomienda testear las funciones con el entorno de Docker recomendado por AWS, pero también se puede realizar de forma estándar invocando las funciones en Python.

# Consignas

## Parte A: Implementación de Nuevo Satélite

El equipo de desarrollo comenzó a implementar la carga de datos de este nuevo satélite, pero por razones estratégicas se te solicitó que termines de implementarlo. Para ello, deberás terminar de completar el código que obtiene los incendios de la API externa, realizar el procesamiento de los datos para normalizarlos al estilo de nuestra base de datos, y subirlos.

Para esta parte del desafío, es importante notar que la API del *FIRESAT23* devuelve los incendios de un día solicitado, pero pueden cargarse incendios más de una vez por día. Por eso, deberá de realizarse una lógica que evite subir los incendios ya cargados previamente. Para ello, la función recibirá en el evento de ejecución cuáles incendios habían sido cargados hasta ese momento para que solo se agreguen los nuevos.

Además, al momento de cargar los incendios, se debe de clasificarlos según el continente que ocurrieron, y se deben descartar los eventos que no ocurrieron en la superficie terrestre.

(Luego se completarán los detalles técnicos de como implementar la solución)

## Parte B: Segmentación de Incendios

Actualmente, contamos con varios usuarios que utilizan nuestro sistema de alertas (disponible en https://app.satellitesonfire.com) para poder recibir notificaciones de los fuegos que ocurren en su territorio. Ahora, están interesados en saber la cantidad de incendios (compuestos por uno o más fuegos) que ocurrieron en un período de tiempo determinado en su territorio.

Cada usuario tiene un criterio distinto para considerar que dos fuegos son del mismo incendio. Por ende, luego de hablar con cada uno de ellos, el equipo técnico determinó que en cada solicitud se puedan indicar dos parámetros (elegidos por cada usuario al momento de pedir la información) que ayudarán a determinar esto:

- $d: int$, la distancia máxima (inclusive) la cual dos fuegos deben tener para ser considerados del mismo incendio. Por simplicidad, consideraremos que la distancia entre dos puntos (fuegos) en coordenadas geodésicas puede ser calculado utilizando la siguiente cuenta: $\sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$, siendo ambos puntos $(x_1,y_1)$ y $(x_2, y_2)$.
- $t: int$, el tiempo, en minutos, que deben tener dos incendios a distancia menor o igual a $d$ para ser consideradas del mismo incendio.

Teniendo estos datos, se debe programar una función en Python ``segmentacionDeIncendios(fuegos: list[dict], d: int, t: int) -> tuple[int,dict]`` que, dado un conjunto de fuegos y los valores $d$ y $t$, indique la cantidad de incendios que ocurrieron, y además, se indique a que incendio pertenece cada fuego.

### Input

La cantidad de fuegos va a recibir esta función va a ser siempre menor o igual a $5000$. Cada fuego va a ser un diccionario con los siguientes datos: ``{id: string, x: float, y: float, time: string}``, donde además ``time`` es de la forma ``"YYYY-MM-DDTHH:MM"``. Además, está garantizado que $d$ y $t$ son mayores a $0$.

### Output

Una tupla. Su primer valor debe ser la cantidad de incendios distintos, y su segundo valor un diccionario que contenga como claves a los ``id`` de cada uno de los incendios, y como valor un número ``int`` que debe ser el mismo para cada uno de los fuegos que pertenezcan al mismo incendio.

La solución debe ser lo suficientemente eficiente para que el usuario no se quede esperando más de unos segundos la respuesta del request.

## Parte C: Implementación de API con la función