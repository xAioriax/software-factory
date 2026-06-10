# Software Factory

Repositorio base para crear aplicaciones web a pedido desde Telegram o chat, publicarlas en GitHub y dejarlas disponibles en una URL pública.

## Estado actual

Este repositorio ya tiene una base funcional local:

- generación de proyectos estáticos;
- validación mínima;
- build para publicar;
- prompts de agentes por rol;
- primer proyecto real migrado: `tateti`.

## Flujo esperado

1. El usuario pide una app por Telegram.
2. Hermes crea una carpeta bajo `projects/`.
3. Se genera el código con una plantilla.
4. Se valida el build.
5. Se crea o actualiza un repo en GitHub.
6. Se despliega la app.
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

Para publicar en GitHub Pages se necesita:

- token `GITHUB_TOKEN`;
- repo remoto configurado;
- rama `gh-pages` o equivalente.

Ejemplo:

```bash
GITHUB_TOKEN=... ./scripts/deploy-github-pages.sh nombre-app gh-pages
```

## Próximos pasos

- Configurar credenciales de GitHub.
- Instalar `gh` si se prefiere automatización con GitHub CLI.
- Habilitar webhook de Hermes para recibir pedidos desde Telegram.
- Decidir si se publica por GitHub Pages, VPS o ambos.
