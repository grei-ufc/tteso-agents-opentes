# Documentação

Este site é construído com [MkDocs](https://www.mkdocs.org/) e o tema
[Material](https://squidfunk.github.io/mkdocs-material/), no mesmo modelo dos
demais repositórios do OpenTES, como o
[tsre-der-opentes](https://grei-ufc.github.io/tsre-der-opentes/).

## Ver localmente

```bash
uv sync --group docs
uv run --group docs mkdocs serve          # http://127.0.0.1:8000
```

O `serve` recarrega a página a cada arquivo salvo.

## Onde fica cada coisa

```
mkdocs.yml                  configuração e menu (nav)
docs/
  index.md                  página inicial
  getting-started/          instalação e primeira negociação
  tutorials/                passo a passo de um estudo
  how-to-guides/            receitas para uma tarefa
  reference/                agentes, protocolos, exemplos, comandos, variáveis e a API gerada
  explanation/              a atualização do PADE, a negociação e a camada de rede
  contributing/, changelog.md, citation.md, license.md
  assets/grei-colors.css    a paleta do GREI
```
Uma página nova só aparece no menu depois de entrar no `nav` do `mkdocs.yml`.
As páginas de `reference/api/` têm só o título e as diretivas `::: modulo`; o
conteúdo vem das docstrings, pelo mkdocstrings.

## Antes de enviar

```bash
uv run --group docs mkdocs build --strict
```

O `--strict` transforma qualquer aviso em erro: link quebrado, página fora do
`nav`, módulo que a API não encontra. É o mesmo build que o CI roda em cada pull
request.

## Publicação

O workflow `.github/workflows/ci.yml` tem dois jobs:

- `docs`: o build com `--strict`, em todo push para `main` e em todo pull
  request;
- `deploy`: só em push para `main`, depois do `docs`, publica o site na branch
  `gh-pages` com `mkdocs gh-deploy`.

O site fica em <https://grei-ufc.github.io/tteso-agents-opentes/>. Na primeira
publicação, um administrador do repositório precisa ativar o GitHub Pages em
*Settings → Pages*, com a fonte *Deploy from a branch*, branch `gh-pages`, pasta
`/ (root)`.
