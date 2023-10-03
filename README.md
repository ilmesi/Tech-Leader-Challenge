# Satellites on Fire Challenge
La idea de este desafío es trabajar con una parte de las tecnologías utilizadas en el stack de Satellites on Fire para resolver algunos problemas relevantes para nuestros clientes. Estos son los pasos para poder comenzar el desafío:

1. Clonar este repositorio y guardarlo de forma **privada**.
2. Realizar los desafíos propuestos a continuación.
3. Compartirnos tu repositorio para poder acceder a las respuestas.
4. ¡Contactanos por correo electrónico para poder revisar el desafío!

Además, estamos abiertos a feedback sobre el desafío. ¡Esperemos que les guste!

# Introducción

Recibir información de incedios en tiempo real es muy importante para nuestros clientes, por lo que estamos constantemente trabajando para poder agregar nuevos satélites a nuestra plataforma. Por ello, se lanzó un nuevo satélite geoestacionario *FIRESAT23*, un nuevo satélite de última generación que nos permitirá obtener incendios de todo el mundo.

Para ello, cuenta con una API muy agradable, a la cual se le pueden solicitar los incendios del último día (y de días previos si se quiere también, pero en este caso no será necesario).

¡Ayudanos a terminar de implementar este nuevo satélite para nuestra plataforma!

## Lenguaje de Programación

Para este desafío, se deberá usar Python 3. Es crucial que se use Python de forma **tipada** (https://docs.python.org/3/library/typing.html), a pesar de que no sea tenido en cuenta en tiempo de ejecución ya que ahorra errores y fomenta las buenas prácticas.

## El Entorno

Para poder resolver el desafío, utilizaremos AWS SAM (Amazon Web Services Serverless Application Model). Este es útil para poder crear, testear y deployar funciones Lambda en la nube de AWS. Esta tecnología es utilizada por nosotros para poder realizar un producto escalable y eficiente, ya que nuestra aplicación tiene una carga de procesamiento de datos elevada. Para más información, está disponible la documentación de AWS SAM en https://docs.aws.amazon.com/serverless-application-model/ y de AWS Lambda en https://docs.aws.amazon.com/lambda/. Además, en el documento [InitializationDetails.md](InitializationDetails.md), se encuentra una breve explicación de como poder usar SAM para testear la aplicación y deployarla (esto último no es necesario para el challenge). Se recomienda testear las funciones con el entorno de Docker recomendado por AWS, pero también se puede realizar de forma estandar invocando las funciones en Python.

# Consignas

## Implementación de Nuevo Satélite

El equipo de desarrolló comenzó a implementar la carga de datos de este nuevo satélite, pero por razones estratégicas se te solicitó que termines de implementarlo. Para ello, deberás terminar de completar el código que obtiene los incendios de la API externa, realizar el procesamiento de los datos para normalizarlos al estilo de nuestra base de datos, y subirlos.

Para esta parte del desafío, es importante notar que la API del *FIRESAT23* devuelve los incendios de un día solicitado, pero pueden cargarse incendios más de una vez por día. Por eso, deberá de realizarse una lógica que evite subir los incendios ya cargados previamente. Para ello, la función recibirá en el evento de ejecución cuáles incendios habían sido cargados hasta ese momento para que solo se agreguen los nuevos.

Además, al momento de cargar los incendios, se debe de clasificarlos según el contienente que ocurrieron, y se deben descartar los eventos que no ocurrieron en la superficie terrestre.

## 