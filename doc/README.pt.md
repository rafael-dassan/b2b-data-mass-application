# B2B Data Mass Script
Este repositório contém o B2B Data Mass Script, voltado para quem deseja criar todas as informações necessárias para executar testes, desenvolver novos recursos e até mesmo explorar os aplicativos.

## Requisito de Sistema
* Sistema operacional baseado em UNIX.

## Ferramentas Necessárias
*  [Git][GitDoc]
*  [Python 3.7 ou superior][Python]

## Executando a Aplicação
Para iniciar o menu da aplicação, por favor, siga os steps abaixos após abrir o Terminal:
```sh
cd <diretorio-do-projeto>
```

(Opcional) Para ter um ambiente livre de imprevisto, instale o pacote `virtualenv` [usando nosso guia de instalação](USER_GUIDE.md#using-virtualenv).

Você pode não ter todos as dependências requeridas por padrão. Instale-as usando o comando pip:
```sh
pip3 install .
```

E então, finalmente você poderá executar o script:
```sh
python3 -m data_mass.main
```

Ao rodar este comando, qualquer um estará habilitado a ver o menu da aplicação, e assim, escolher qualquer uma opção disponível dependendo do uso.

## Contribuindo ao Data Mass
Todas contribuições, reports de bugs, bug fixes, melhoria de documentação, melhorias, e ideias são bem-vindas.

Um overview detalhado em como contribuir pode ser encontrado no [guia de contribuição](doc/USER_GUIDE.md#contributing-to-data-mass).

Dê uma olhada em nosso [guia de estilo de código](doc/../C_STYLE_GUIDE.md) (disponível apenas em inglês)!

## Informações Adicionais
*  [Padrões de Desenvolvimento][Standards]
*  [Notas de Release][Release Notes]

[//]: #  (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

[GitDoc]: https://git-scm.com/doc
[Python]: https://www.python.org/downloads/
[Standards]: https://anheuserbuschinbev.sharepoint.com/sites/b2bengineering/architecture/SitePages/Data-Mass-Application.aspx
[Release Notes]: https://anheuserbuschinbev.sharepoint.com/:b:/s/b2bengineering/EaTlUWEzsp1EqdmKaqBclL4ByT6uvxDV1nF1erEOsD-stQ?e=QQyxU8
