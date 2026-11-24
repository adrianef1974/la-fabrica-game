# LA FÁBRICA

**LA FÁBRICA** es un simulador de vida laboral en primera persona ambientado en una fábrica argentina. El mundo funciona de manera autónoma: los empleados cumplen sus rutinas, se relacionan, discuten, toman decisiones y atraviesan acontecimientos aunque el jugador no esté presente.

El jugador elige a uno de los empleados y vive la misma fábrica desde su perspectiva. No hay una historia lineal de misiones obligatorias ni un final impuesto.

## Estado del proyecto

**Etapa actual: preparación y validación técnica.**

Antes de desarrollar los sistemas completos del juego, se realizará una prueba mínima para validar el motor y la tecnología elegidos en PC y Android. La compatibilidad con Android todavía debe comprobarse; no se considera confirmada.

## Concepto general

- Juego individual, sin multijugador.
- Un único mundo compartido por los personajes dentro de cada partida.
- Doce personajes jugables, cada uno con su propia partida guardada.
- Jornada laboral de 08:00 a 17:00.
- Los personajes no controlados mantienen rutinas y relaciones autónomas.
- Los acontecimientos pueden ocurrir con o sin la participación del jugador.
- Sin límite de días y sin obligación de completar misiones.
- Ambientación, lenguaje y situaciones de tono adulto, con diálogos propios para cada personaje.

## Personajes jugables

- **Operarios:** Charly, Gonzalo, Francisco, Martín, Alan, John y Jonathan.
- **Mantenimiento:** Adrián.
- **Supervisor:** Fernando.
- **Administración:** Jessica.
- **Propietarios:** Ricardo y Silvia.

## Mundo y sistemas previstos

- Sector de producción, oficinas, baños y pasillos.
- Máquinas con estados de funcionamiento, falla, parada y reparación.
- Relaciones dinámicas: confianza, amistad, respeto, rivalidad y desconfianza.
- Acontecimientos espontáneos y encadenados, con consecuencias.
- Economía de la empresa: producción, pedidos, gastos, salarios, mantenimiento, ganancias y pérdidas.
- Inventario según el rol de cada personaje.
- Computadoras, teléfonos, documentos, herramientas y objetos interactivos.
- Guardado automático y manual, con partidas independientes por personaje.

## Dirección visual y técnica

- Perspectiva en primera persona.
- Estética retro pixelada, inspirada en los juegos clásicos de raycasting.
- Prioridad inicial: bajo consumo de recursos y funcionamiento en el equipo de desarrollo disponible.
- Controles de teclado y mouse en PC, y controles táctiles en Android.
- Sonidos ambientales y efectos; sin música ni voces.

## Plan de desarrollo

1. **Validación técnica:** ventana, renderizado raycasting, movimiento, colisiones y controles básicos en PC y Android.
2. **Prototipo del escenario:** mapa inicial de la fábrica, sectores, puertas y objetos.
3. **Personajes autónomos:** movimiento, rutinas, horarios y estados.
4. **Interacciones:** diálogo, objetos, máquinas, teléfonos y computadoras.
5. **Sistemas de simulación:** relaciones, acontecimientos, economía e inventarios.
6. **Partidas y persistencia:** guardado, carga y partidas independientes.
7. **Adaptación y pruebas:** controles, rendimiento y experiencia en ambas plataformas.

## Criterio de trabajo

El desarrollo se hará por etapas pequeñas. Cada cambio deberá probarse antes de avanzar al siguiente. Se conservará el comportamiento ya validado y no se dará por terminada una función hasta comprobarla.

---

*Documento inicial de referencia. Las decisiones técnicas definitivas se tomarán después de completar la validación del primer prototipo.*