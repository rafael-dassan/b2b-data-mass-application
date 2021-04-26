# B2B Data Mass Script
Este repositorio contiene el B2B Data Mass Script, dirigido a aquellos que quieran crear toda la información necesaria para ejecutar pruebas, desarrollar nuevas funcionalidades e incluso explorar aplicaciones.

## Requisitos del Sistema
* Sistema operativo basado en UNIX.

## Herramientas Necesarias
*  [Git][GitDoc]
*  [Python 3.7 o superior][Python]

## Ejecutando la Aplicación
Para iniciar el menú de la aplicación, siga los pasos a continuación después de abrir la Terminal::
```sh
cd <directorio-del-proyecto>
```

(Opcional) Para tener un entorno libre inesperado, instale `virtualenv` [usando nuestra guía de instalación](USER_GUIDE.md#using-virtualenv).

Es posible que no tenga todas las dependencias necesarias de forma predeterminada. Instálelos usando el comando pip:
```sh
pip3 install .
```

Y luego, finalmente puedes ejecutar el script:
```sh
python3 -m data_mass.main
```

Al ejecutar este comando, cualquiera podrá ver el menú de la aplicación, y así elegir cualquier opción disponible según el uso..

## Contribuyendo a Data Mass
Todas las contribuciones, informes de errores, correcciones de errores, mejoras de documentación, mejoras e ideas son bienvenidas.

Puede encontrar una descripción detallada sobre cómo contribuir en la [guía de contribución](USER_GUIDE.md#contributing-to-data-mass).

¡Eche un vistazo a nuestra [guía de estilo de código](doc/../C_STYLE_GUIDE.md) (disponible solo en inglés)!

## Informaciones Adicionales
*  [Estándares de Desarrollo][Standards]
*  [Notas de Lanzamiento][Release Notes]

[//]: #  (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

[GitDoc]: https://git-scm.com/doc
[Python]: https://www.python.org/downloads/
[Standards]: https://anheuserbuschinbev.sharepoint.com/sites/b2bengineering/architecture/SitePages/Data-Mass-Application.aspx
[Release Notes]: https://anheuserbuschinbev.sharepoint.com/:b:/s/b2bengineering/EaTlUWEzsp1EqdmKaqBclL4ByT6uvxDV1nF1erEOsD-stQ?e=QQyxU8
