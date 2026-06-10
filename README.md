# Software Factory

Repositorio base para crear aplicaciones web a pedido desde Telegram o chat, publicarlas en GitHub y dejarlas disponibles en una URL pública.

Repo remoto: https://github.com/xAioriax/software-factory

Publicación inicial: GitHub Pages, con una página índice y subcarpetas por proyecto.

## Estado actual

Este repositorio ya tiene una base funcional local:

- generación de proyectos estáticos;
- validación mínima;
- build para publicar;
- prompts de agentes por rol;
- primer proyecto real migrado: `tateti`;
- GitHub CLI autenticado;
- workflow de GitHub Actions para publicar en GitHub Pages.

## Flujo esperado

1. El usuario pide una app por Telegram.
2. Hermes crea una carpeta bajo `projects/`.
3. Se genera el código con una plantilla.
4. Se valida el build.
5. Se crea commit y se sube a GitHub.
6. GitHub Actions publica la app en GitHub Pages.
7. Hermes responde con la URL.

## Carpetas

- `agents/`: prompts de agentes especializados.
- `scripts/`: scripts de generación, validación y despliegue.
- `projects/`: proyectos generados.
- `templates/static-app/`: plantilla base para apps estáticas.

## Comandos básicos

Crear un proyecto nuevo:

```bash
./scripts/init-project.sh nombre-app "Descripcion corta"
```

Validar un proyecto:

```bash
./scripts/validate-project.sh nombre-app
```

Build estático:

```bash
./scripts/build-static.sh nombre-app
```

## Despliegue

El workflow `.github/workflows/pages.yml` publica automáticamente en GitHub Pages cuando se hace push a `main`.

Cada app queda disponible en:

`https://xAioriax.github.io/software-factory/projects/<nombre-proyecto>/`

La página índice queda en:

`https://xAioriax.github.io/software-factory/`

## Próximos pasos

- Configurar credenciales de GitHub.
- Instalar `gh` si se prefiere automatización con GitHub CLI.
- Habilitar webhook de Hermes para recibir pedidos desde Telegram.
- Decidir si se publica por GitHub Pages, VPS o ambos.
