---
description: "better-theme — Skill de diseño front-end para agentes de IA: color, radios, textos, animación y accesibilidad. Cura la enfermedad de las plantillas."
---

# AI-Skills: better-theme

## Language / 语言

| Language | File                                   |
| :------- | :------------------------------------- |
| English  | [README-EN.md](README-EN.md)           |
| 汉语（简体）   | [README.md](../README.md)              |
| 漢語（繁體）   | [README-CN-HANT.md](README-CN-HANT.md) |
| 日本語      | [README-JP.md](README-JP.md)           |
| español  | **README-ES.md** (actual)              |

## Introducción

> Genera propuestas de diseño con una estética propia para front-ends web, y evita el estilo de plantilla SaaS repetido hasta el cansancio.
> An opinionated front-end design skill for AI agents.

Un Skill de diseño front-end para AI Agents: se encarga de la paleta, los radios, los textos, las animaciones y la accesibilidad, y está hecho específicamente para curar la enfermedad de las plantillas generativas: "degradado azul-violeta + radios grandes + Hero con tres tarjetas + textos vacíos".

## Estructura

```text
better-theme/
├── SKILL.md                      # Entrada: lineamientos generales de diseño + flujo de trabajo + modo estricto
├── README.md                     # Explicación en chino simplificado (este archivo)
├── readme/                       # Explicaciones en otros idiomas
├── references/                   # Documentos de referencia que se cargan según demanda (ver references/README.md)
│   ├── README.md                 # Índice: cuál leer y cuándo
│   ├── agent-guide.md            # Manual de operación para optimizar: clasificar → diagnosticar → corregir → checklist
│   ├── color-theme.md            # 7 paletas por escenario + árbol de decisión para elegir color
│   ├── radius.md                 # Norma de radios estilo macOS (token / anidamiento concéntrico / curvatura continua)
│   ├── copywriting.md            # Referencia de textos de UI (404 / estado vacío / inicio de sesión / carga)
│   ├── interaction.md            # Normas de animación e interacción (duración / easing / a11y / antipatrones)
│   └── cases/
│       └── deepseek-glass.md     # Caso: glassmorphism + fluido WebGL + animación Spring
├── asset/
│   └── icon/                     # Más de 600 iconos SVG offline (recopilados de la librería de iconos de Alibaba)
└── scripts/
    ├── check-refs.py             # Revisión de higiene de la documentación (referencias cruzadas / frontmatter / saltos de línea / espacios al final de línea)
    └── sync-global.sh            # Sincroniza a la instalación global ~/.dsh/skills/better-theme
```

**Principio de carga**: `SKILL.md` es la entrada, y `references/` se lee según demanda. Carga solo los archivos que la tarea actual realmente necesita: una tarea de pura paleta no necesita leer `interaction.md`.

## Instalación

Para usarlo como Skill de DSH, basta con poner el repositorio en el directorio de skills:

```bash
git clone https://github.com/JinSuperOfficial/better-theme.git ~/.dsh/skills/better-theme
```

También puedes pegar directamente el contenido de `SKILL.md` en la conversación (cuando la AI en versión web no puede leer archivos locales).
Iconos para explorar en línea: [asset/icon](https://github.com/JinSuperOfficial/better-theme/tree/main/asset/icon/)

## Tres líneas rojas

1. **Lo que pide el usuario va primero**: el color de marca, el estilo y el stack que el usuario especifique pesan más que cualquier sugerencia de este repositorio.
2. **La accesibilidad no se negocia**: contraste, foco de teclado y `prefers-reduced-motion` son tres puntos que no se pueden omitir.
3. **Nada de plantillas**: si cambias el nombre del producto y la propuesta sigue funcionando igual, es que no es lo bastante específica: rehazla.

## Antipatrones, consulta rápida

Fondo crema cálido + títulos con serif + naranja terracota / fondo casi negro + verde ácido · bermellón / bordes finos + cero radios + columnas densas /
Hero + tres tarjetas / centrado mecánico en toda la página / un mismo radio grande para todos los componentes. Si aciertas en cualquiera, rehazlo de inmediato.

## Mantenimiento

Después de cambiar la documentación, corre la revisión para asegurarte de que las referencias cruzadas no se rompieron, el frontmatter es YAML válido, la tabla de idiomas está completa y los saltos de línea son uniformes:

```bash
python3 scripts/check-refs.py
```

Si cambiaste el contenido y quieres actualizar la instalación global, sincroniza con un solo comando (`--dry-run` te deja ver antes qué se va a modificar):

```bash
./scripts/sync-global.sh
```

## Convenciones

- Nombres de archivo todo en minúsculas, kebab-case, sin número de versión; los nombres en chino se cambian a inglés.
- Los documentos de casos van en `references/cases/`.
- Las referencias cruzadas entre documentos usan rutas relativas, y se actualizan al renombrar.
- Saltos de línea siempre LF.

## Uso de assets y aviso de derechos de autor

El directorio `asset/` de este repositorio sirve para proporcionarle a `better-theme` los iconos, imágenes y otros recursos de referencia visual que necesita el diseño web.

Parte de los recursos puede venir de terceros, y sus derechos de autor, derechos de marca y demás derechos relacionados siguen perteneciendo a sus titulares originales. El autor del repositorio no reclama ningún derecho sobre recursos de terceros que no pertenezcan claramente a este proyecto.

Para los recursos de terceros, su uso debe regirse por las condiciones de autorización que establezcan el autor original, la plataforma de publicación o la licencia correspondiente. Si la licencia, la procedencia o el estado de autorización de algún recurso no está claro, no lo uses directamente en publicaciones abiertas, proyectos comerciales u otros escenarios que puedan generar riesgo de derechos de autor.

La AI puede acceder y leer el contenido de `asset/` para:

- conocer el estilo visual de better-theme;
- buscar materiales adecuados para el diseño web;
- usarlos en las páginas web que genere cuando confirme que el recurso cuenta con la licencia de uso correspondiente.

La AI no debe dar por sentado, solo porque un recurso esté en este repositorio, que el recurso pertenece a este proyecto, que se puede redistribuir sin límites o que se puede usar para cualquier fin comercial.

Si surge una disputa de derechos de autor, marcas u otros derechos relacionada con recursos de terceros, se debe atender a la titularidad real del recurso, su procedencia y la información de su licencia. El autor del repositorio no hace declaración de derechos sobre recursos de terceros no autorizados.

### Principios de uso para la AI

Da prioridad a los recursos que este proyecto ofrece de forma explícita, cuya procedencia es clara y cuya licencia permite su uso.

Para los recursos con licencia desconocida o estado de autorización poco claro:

1. se pueden usar como referencia visual;
2. no se deben incrustar por defecto directamente en la página web final;
3. se deben reemplazar preferentemente por recursos con autorización clara;
4. si es necesario, pídele al usuario que confirme su derecho de uso.

Este aviso no modifica la licencia ni el estado de derechos originales de ningún recurso de terceros.

## License

El contenido propio de este repositorio (`SKILL.md`, `references/`, `scripts/`) se puede usar libremente para diseño y desarrollo; la autorización de los recursos de terceros bajo `asset/` se describe arriba.
