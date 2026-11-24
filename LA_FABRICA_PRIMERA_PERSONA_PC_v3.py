import math
import random
import pygame


TILE_SIZE = 44
MAP_COLS = 36
MAP_ROWS = 24
MAP_WIDTH = MAP_COLS * TILE_SIZE
MAP_HEIGHT = MAP_ROWS * TILE_SIZE

PLAYER_SPEED = 195
NPC_WALK_SPEED = 86
PLAYABLE_CHARACTERS = [
    "Charly", "Gonzalo", "Francisco", "Martín", "Alan", "John",
    "Jonathan", "Adrián", "Fernando", "Jessica", "Ricardo", "Silvia"
]


def normalize_name(str_val):
    if not str_val:
        return ""
    replacements = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
        "Á": "a", "É": "e", "Í": "i", "Ó": "o", "Ú": "u",
        "ñ": "n", "Ñ": "n"
    }
    cleaned = "".join(replacements.get(ch, ch) for ch in str_val.strip())
    return " ".join(cleaned.split()).lower()


def pick_random(seq):
    if not seq:
        return ""
    return random.choice(seq)


NPC_BANTER_LINES = [
    "¿Qué hacés acá, muerto? Andá a laburar.",
    "Che, ¿viste la cara de orto que tiene Fernando hoy?",
    "Me contaron que Jessica está prendiendo fuego la oficina...",
    "Dejá de hacerte el ocupado que no engañás a nadie.",
    "Ricardo se compró una chata nueva y a nosotros nos paga con caramelos.",
    "Si te agarra Silvia boludeando te come crudo.",
    "¿Hoy se cobra o seguimos cobrando en promesas?",
    "¡Qué calor de mierda hace en este galpón, hermano!"
]

NPC_FIGHT_LINES = [
    "¡Pará de empujar, gil!",
    "¡Hoy tengo un día de mierda, no me busqués!",
    "¡Vení que te acomodo las ideas!",
    "¡No me grités, pelotudo!",
    "¡Acá tenés tu hora extra!"
]

NPC_GOOD_MOOD_SOLO = [
    "¡Qué lindo día para rascarse un poco!",
    "Hoy ando de diez, ni Fernando me la baja.",
    "Silbando bajito hasta las 17:00...",
    "Hoy me levanté con el pie derecho, papá."
]

NPC_BAD_MOOD_SOLO = [
    "¡Qué podrido me tienen todos acá!",
    "No me hablen hoy que muerdo.",
    "¡Esta máquina de mierda siempre se traba!",
    "¡Qué ganas de mandar todo a la mierda!"
]

BOSS_PASSBY_INSULTS = {
    "ricardo": [
        "¡Mirá al viejo garca este paseando mientras nos debe guita!",
        "¡Pagá los sueldos, rata de mierda!",
        "¡Metete la camioneta 0km en el orto, viejo forro!"
    ],
    "silvia": [
        "¡Ahí pasa la buchona de Silvia, guardá todo!",
        "¡Mirá la cara de orto con la que camina esta forra!",
        "¡Andá a dibujar números a tu oficina, ortiva!"
    ],
    "jessica": [
        "¡Mirá cómo mueve el culo esta calientapavas!",
        "¡Ahí viene la princesa de Ricardo, no hace un carajo!",
        "¡Llegó la acomodada del jefe, qué fácil es laburar así!"
    ]
}

TRASH_INSULT_LINES = [
    "¡La concha de la lora, siempre me toca sacar esta basura de mierda!",
    "¡Qué olor a podrido, manga de vagos del orto!",
    "¡16:00 y yo cargando bolsas como un pelotudo, la puta madre!"
]

RICARDO_BAD_JOKES = [
    "¿Qué le dice un tornillo a otro? ¡No te hagas el roscado!",
    "¿Por qué el gallo no usa reloj? ¡Porque ya tiene despertador!",
    "¿Cuál es el colmo de un carpintero? ¡Tener una hija tabla!",
    "¡Che, si el lunes tuviera cara, le metía un cabezazo!"
]

RICARDO_GOOD_NO_PAY_LINES = [
    "Hoy no le pago nada",
    "¡Hoy no le pago nada a nadie, ja!",
    "Hoy no le pago nada, que laburen por amor al arte"
]


def create_npc_definitions():
    def make_mood():
        is_bad = random.random() < 0.5
        return {
            "is_bad": is_bad,
            "tag": "Mal humor" if is_bad else "Buen humor",
            "expression": "grumpy" if is_bad else "smile"
        }

    moods = {
        k: make_mood()
        for k in [
            "ricardo", "silvia", "jessica", "fernando", "adrian", "charly",
            "gonzalo", "alan", "martin", "john", "francisco", "jonathan"
        ]
    }

    return [
        {
            "id": "ricardo",
            "name": "Ricardo",
            "role": f"Dueño • Oficina de Ricardo ({moods['ricardo']['tag']})",
            "zone": "Oficina de Ricardo",
            "fixed": True,
            "mood_is_bad": moods["ricardo"]["is_bad"],
            "x": 8.5 * TILE_SIZE,
            "y": 5.4 * TILE_SIZE,
            "style": {"shirt": (127, 29, 29), "pants": (15, 23, 42), "hair": (226, 232, 240), "skin": (243, 198, 159)},
            "questions": [
                {"id": "doing", "label": "¿Qué carajo estás haciendo acá adentro?", "responses": ["Viendo cómo cago a los empleados, ¿qué te pensás?", "Rascándome las bolas en el aire acondicionado mientras ustedes transpiren."]},
                {"id": "today", "label": "¿Qué onda hoy, pagás o te hacés el boludo?", "responses": ["No les pagué el sueldo, pero me compré una camioneta 0km. ¡Una nave!", "¿Plata? Andá a pedirle al banco, muerto de hambre."]},
                {"id": "fernando", "label": "¿Qué opinás del forro de Fernando?", "responses": ["Es mi yerno. Me lo tuve que fumar acá para que no me manguee plata en casa."]},
                {"id": "unlocked_camioneta", "label": "¿Con la nuestra te compraste la camioneta, rata?", "unlocked_by": "clue_ricardo_camioneta", "responses": ["¡Y con el aguinaldo me voy a Miami, boludo! Cerrá la puerta del lado de afuera."]}
            ]
        },
        {
            "id": "silvia",
            "name": "Silvia",
            "role": f"Administración • Oficina de Silvia ({moods['silvia']['tag']})",
            "zone": "Oficina de Silvia",
            "fixed": True,
            "mood_is_bad": moods["silvia"]["is_bad"],
            "x": 15.5 * TILE_SIZE,
            "y": 4.6 * TILE_SIZE,
            "style": {"shirt": (126, 34, 206), "pants": (30, 41, 59), "hair": (69, 26, 3), "skin": (245, 203, 167)},
            "questions": [
                {"id": "doing", "label": "¿Qué hacés, Silvia? ¿Laburando o mirando el techo?", "responses": ["Tapando las cagadas contables de Ricardo para que no vayamos todos presos."]},
                {"id": "gossip", "label": "Largá algún chisme picante, dale", "responses": ["Si decís que salió de mí te corto las bolas con la guillotina de papel."]},
                {"id": "unlocked_multi", "label": "¿Qué puterío se comenta en los pasillos?", "unlocked_by": "multi_clue_silvia", "responses": ["Varios comentan que hay más cuernos y arreglos por izquierda en esta fábrica que tornillos en el depósito."]}
            ]
        },
        {
            "id": "jessica",
            "name": "Jessica",
            "role": f"Oficina • Oficina de Jessica ({moods['jessica']['tag']})",
            "zone": "Oficina de Jessica",
            "fixed": True,
            "mood_is_bad": moods["jessica"]["is_bad"],
            "x": 32.5 * TILE_SIZE,
            "y": 5.4 * TILE_SIZE,
            "style": {"shirt": (219, 39, 119), "pants": (15, 23, 42), "hair": (250, 204, 21), "skin": (247, 207, 168)},
            "questions": [
                {"id": "doing", "label": "¿Qué hacés, bombón? ¿Muy ocupada?", "responses": ["Estoy aburrida esperando que venga alguien con ganas de jugar un rato."]},
                {"id": "today", "label": "¿Qué pasó hoy que estás tan sonrisa?", "responses": ["Hoy vi a dos encerrados donde no tendrían que estar... ¡un escándalo!"]},
                {"id": "unlocked_jessica", "label": "Dale, decime quiénes son los dos que andan a los besos", "unlocked_by": "clue_jessica_two", "responses": ["Seguí apretando a los de producción que alguno pisa el palito solo."]}
            ]
        },
        {
            "id": "fernando",
            "name": "Fernando",
            "role": f"Supervisor • Oficina de Fernando ({moods['fernando']['tag']})",
            "zone": "Oficina de Fernando",
            "fixed": True,
            "mood_is_bad": moods["fernando"]["is_bad"],
            "x": 21.5 * TILE_SIZE,
            "y": 4.6 * TILE_SIZE,
            "style": {"shirt": (185, 28, 28), "pants": (30, 41, 59), "hair": (51, 65, 85), "skin": (234, 182, 138)},
            "questions": [
                {"id": "doing", "label": "¿Qué hacés, jefe? ¿Vigilando que nadie respire?", "responses": ["Supervisando. Alguien tiene que mantener este chiquero en orden."]},
                {"id": "workers", "label": "¿Qué opinás de los muchachos de producción?", "responses": ["Son todos unos pelotudos. No sirven ni para espiar."]}
            ]
        },
        {
            "id": "adrian",
            "name": "Adrián",
            "role": f"Producción ({moods['adrian']['tag']})",
            "zone": "Sector Central de Producción",
            "fixed": False,
            "mood_is_bad": moods["adrian"]["is_bad"],
            "x": 7 * TILE_SIZE,
            "y": 13 * TILE_SIZE,
            "style": {"shirt": (2, 132, 199), "pants": (30, 41, 59), "hair": (24, 24, 27), "skin": (243, 198, 159)},
            "questions": [
                {"id": "doing", "label": "¿Qué hacés, Adrián?", "responses": ["Haciendo tiempo hasta la hora de salida sin que me agarre el yerno del patrón."]},
                {"id": "unlocked_adrian", "label": "Largá el secreto ahora", "unlocked_by": "multi_clue_adrian", "responses": ["Uno de acá se hace el moralista de día y de noche manda mensajitos picantes arriba."]}
            ]
        },
        {
            "id": "charly",
            "name": "Charly",
            "role": f"Producción ({moods['charly']['tag']})",
            "zone": "Sector Central de Producción",
            "fixed": False,
            "mood_is_bad": moods["charly"]["is_bad"],
            "x": 12.5 * TILE_SIZE,
            "y": 16.5 * TILE_SIZE,
            "style": {"shirt": (217, 119, 6), "pants": (31, 41, 55), "hair": (120, 53, 15), "skin": (245, 203, 167)},
            "questions": [
                {"id": "doing", "label": "¿Qué hacés, Charly?", "responses": ["Si aparece el forro de Fernando, decile que estaba salvando la producción."]},
                {"id": "gossip", "label": "Tirá la posta del puterío de hoy", "responses": ["Lo normal: tres laburando, cinco boludeando y uno chamuyándose a Jessica."]},
                {"id": "unlocked_charly", "label": "Contame la versión sin censura de hoy", "unlocked_by": "clue_from_charly", "responses": ["Acá se hacen todos los santos, pero hay más trampa que en un boliche."]}
            ]
        },
        {
            "id": "gonzalo",
            "name": "Gonzalo",
            "role": f"Producción ({moods['gonzalo']['tag']})",
            "zone": "Sector Central de Producción",
            "fixed": False,
            "mood_is_bad": moods["gonzalo"]["is_bad"],
            "x": 23.5 * TILE_SIZE,
            "y": 16.5 * TILE_SIZE,
            "style": {"shirt": (13, 148, 136), "pants": (30, 41, 59), "hair": (30, 41, 59), "skin": (243, 198, 159)},
            "questions": [
                {"id": "doing", "label": "¿Qué hacés, Gonzalo?", "responses": ["Acá, tratando de pasar el día sin que me rompan las bolas."]},
                {"id": "secret", "label": "Tirame una pista o un secreto", "responses": ["Andá a apretarlo a Charly, sabe algo heavy que todavía no soltó."]}
            ]
        },
        {
            "id": "alan",
            "name": "Alan",
            "role": f"Producción ({moods['alan']['tag']})",
            "zone": "Sector Central de Producción",
            "fixed": False,
            "mood_is_bad": moods["alan"]["is_bad"],
            "x": 29 * TILE_SIZE,
            "y": 13 * TILE_SIZE,
            "style": {"shirt": (37, 99, 235), "pants": (15, 23, 42), "hair": (82, 40, 12), "skin": (245, 203, 167)},
            "questions": [
                {"id": "doing", "label": "¿Qué hacés, fantasma?", "responses": ["Acá, enseñándoles a estos muertos cómo se labura de verdad."]},
                {"id": "jessica", "label": "¿Vos también le tenés ganas a Jessica?", "responses": ["Mejor preguntale a ella cómo le va conmigo, papá."]}
            ]
        },
        {
            "id": "martin",
            "name": "Martín",
            "role": f"Producción ({moods['martin']['tag']})",
            "zone": "Sector Central de Producción",
            "fixed": False,
            "mood_is_bad": moods["martin"]["is_bad"],
            "x": 9.5 * TILE_SIZE,
            "y": 20 * TILE_SIZE,
            "style": {"shirt": (79, 70, 229), "pants": (30, 41, 59), "hair": (24, 24, 27), "skin": (234, 182, 138)},
            "questions": [
                {"id": "mood_talk", "label": "¿Cómo andás, Martín?", "responses": ["Acá, sobreviviendo un día más en esta cárcel."]}
            ]
        },
        {
            "id": "john",
            "name": "John",
            "role": f"Producción ({moods['john']['tag']})",
            "zone": "Sector Central de Producción",
            "fixed": False,
            "mood_is_bad": moods["john"]["is_bad"],
            "x": 18 * TILE_SIZE,
            "y": 20 * TILE_SIZE,
            "style": {"shirt": (5, 150, 105), "pants": (31, 41, 55), "hair": (39, 39, 42), "skin": (243, 198, 159)},
            "questions": [
                {"id": "doing", "label": "¿Qué hacés, Jon?", "responses": ["Tratando de terminar el día sin comerme ningún garrón."]}
            ]
        },
        {
            "id": "francisco",
            "name": "Francisco",
            "role": f"Producción ({moods['francisco']['tag']})",
            "zone": "Sector Central de Producción",
            "fixed": False,
            "mood_is_bad": moods["francisco"]["is_bad"],
            "x": 27.5 * TILE_SIZE,
            "y": 20 * TILE_SIZE,
            "style": {"shirt": (162, 28, 175), "pants": (30, 41, 59), "hair": (92, 45, 12), "skin": (245, 203, 167)},
            "questions": [
                {"id": "gossip", "label": "¡Dale, largá todo lo que sabés!", "responses": ["Tengo tres bombas. ¿Querés el corto, el largo o el que termina en divorcio?"]}
            ]
        },
        {
            "id": "jonathan",
            "name": "Jonathan",
            "role": f"Producción ({moods['jonathan']['tag']})",
            "zone": "Sector Central de Producción",
            "fixed": False,
            "mood_is_bad": moods["jonathan"]["is_bad"],
            "x": 13.5 * TILE_SIZE,
            "y": 11.5 * TILE_SIZE,
            "style": {"shirt": (51, 65, 85), "pants": (15, 23, 42), "hair": (30, 41, 59), "skin": (243, 198, 159)},
            "questions": [
                {"id": "doing", "label": "¿Qué hacés, Jonathan?", "responses": ["Acá, tratando de que el día pase rápido sin quilombos."]}
            ]
        }
    ]


def build_factory_layout():
    grid = [[0 for _ in range(MAP_COLS)] for _ in range(MAP_ROWS)]

    for r in range(1, 7):
        for c in range(1, MAP_COLS - 1):
            if (1 <= c <= 11) or (13 <= c <= 23) or (25 <= c <= 34):
                grid[r][c] = 2

    for c in range(MAP_COLS):
        grid[0][c] = 1
        grid[MAP_ROWS - 1][c] = 1
    for r in range(MAP_ROWS):
        grid[r][0] = 1
        grid[r][MAP_COLS - 1] = 1

    for c in range(1, MAP_COLS - 1):
        grid[7][c] = 1
    for r in range(1, 7):
        grid[r][12] = 1
        grid[r][18] = 1
        grid[r][24] = 1

    grid[7][6] = 3
    grid[7][15] = 3
    grid[7][21] = 3
    grid[7][29] = 3

    for r, c in [[3, 4], [3, 5], [3, 6], [3, 14], [3, 15],
                 [3, 20], [3, 21], [3, 22], [3, 28], [3, 29], [3, 30]]:
        grid[r][c] = 4

    for r, c in [[1, 1], [1, 2], [1, 13], [1, 14], [1, 33], [1, 34]]:
        grid[r][c] = 7

    for r, c in [[10, 4], [10, 5], [10, 6], [10, 15], [10, 16], [10, 17], [10, 27], [10, 28], [10, 29]]:
        grid[r][c] = 5

    for r, c in [[14, 9], [14, 10], [14, 15], [14, 16], [14, 21], [14, 22], [18, 15], [18, 16], [18, 25], [18, 26]]:
        grid[r][c] = 6

    for r, c in [[9, 1], [10, 1]]:
        grid[r][c] = 7

    # Cuarto BAÑO (filas 19..22, cols 1..5, entrada en [19][3])
    for r in range(19, 23):
        for c in range(1, 6):
            grid[r][c] = 10
    for c in range(1, 6):
        grid[19][c] = 1
    for r in range(19, 23):
        grid[r][5] = 1
    grid[19][3] = 8

    # El sector inferior derecho queda como circulación/producción abierta.
    for r in range(19, 23):
        for c in range(30, 35):
            grid[r][c] = 0

    solid_rects = []
    for r in range(MAP_ROWS):
        for c in range(MAP_COLS):
            code = grid[r][c]
            if code in (1, 4, 5, 6, 7):
                solid_rects.append(pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    return {"grid": grid, "solid_rects": solid_rects}


def get_zone_at(x, y):
    col = int(x // TILE_SIZE)
    row = int(y // TILE_SIZE)
    if 1 <= row <= 6:
        if 1 <= col <= 11:
            return "Oficina de Ricardo"
        if 13 <= col <= 17:
            return "Oficina de Silvia"
        if 19 <= col <= 23:
            return "Oficina de Fernando"
        if 25 <= col <= 34:
            return "Administración de Jessica"
    if 19 <= row <= 22 and 1 <= col <= 5:
        return "Baño"
    return "Sector Central de Producción"


class FactoryPygame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("LA FÁBRICA - Prototipo Primera Persona")
        self.width = 1080
        self.height = 680
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        self.font_title = pygame.font.SysFont("segoeui", 34, bold=True)
        self.font_hud = pygame.font.SysFont("segoeui", 15, bold=True)
        self.font_label = pygame.font.SysFont("segoeui", 13, bold=True)
        self.font_bubble = pygame.font.SysFont("segoeui", 12, bold=True)
        self.font_btn = pygame.font.SysFont("segoeui", 14, bold=True)
        self.font_dialog = pygame.font.SysFont("segoeui", 16)

        self.map_data = build_factory_layout()
        self.world_props = self.build_world_props()
        self.prop_surfaces = self.build_prop_surfaces()
        self.state = "start"
        self.selected_character_index = 0
        self.input_name = ""

        self.day_number = 1
        self.clock_minutes = 8 * 60
        self.shift_ended = False

        self.fov = math.radians(66)
        self.mouse_sensitivity = 0.0026
        self.camera_pitch = 0.0
        self.camera_horizon = self.height // 2
        self.ray_count = 180
        self.mouse_captured = False

        self.player = {
            "name": "",
            "role_id": "",
            "x": 18 * TILE_SIZE,
            "y": 8.6 * TILE_SIZE,
            "radius": 14,
            "dir_angle": 0.0,
            "walk_phase": 0.0,
            "shirt": (245, 158, 11),
            "pants": (30, 41, 59),
            "hair": (17, 24, 39),
            "skin": (247, 207, 168)
        }
        self.npcs = []
        self.nearby_npc = None
        self.active_npc = None
        self.dialogue_response = "Elegí una pregunta o presioná ESC para cerrar."
        self.visible_questions = []

        self.talked_to_npcs = set()
        self.unlocked_flags = set()
        self.clue_chain = {}

        self.player_fight_timer = 0.0
        self.ricardo_check_timer = 2.0
        self.charly_bath_cooldown = 6.0
        self.charly_bath_phase = "none"
        self.charly_bath_timer = 0.0
        self.bathroom_door_pos = (3.5 * TILE_SIZE, 18.4 * TILE_SIZE)
        self.bathroom_inside_pos = (2.5 * TILE_SIZE, 21.0 * TILE_SIZE)

        self.trash_started = False
        self.trash_done = False
        self.trash_carrier_id = None
        self.alan_late_spawned = False
        self.lunch_meeting_active = False
        self.gonzalo_outside = False
        self.alan_outside = False
        self.jonathan_sleeping = False
        self.jonathan_slept_today = False

        self.btn_start = pygame.Rect(0, 0, 220, 46)
        self.btn_talk = pygame.Rect(0, 0, 120, 42)
        self.btn_fight = pygame.Rect(0, 0, 120, 42)
        self.btn_next_day = pygame.Rect(0, 0, 130, 34)
        self.question_rects = []

    def build_world_props(self):
        """Convierte los bloques bajos del mapa en mobiliario/maquinaria 3D."""
        props = []
        kinds = {4: "desk", 5: "bench", 6: "machine", 7: "cabinet"}
        for row, cells in enumerate(self.map_data["grid"]):
            for col, code in enumerate(cells):
                kind = kinds.get(code)
                if kind:
                    props.append({
                        "x": (col + 0.5) * TILE_SIZE,
                        "y": (row + 0.5) * TILE_SIZE,
                        "kind": kind,
                        "width": 0.92 if kind != "machine" else 0.88,
                        "height": 0.92 if kind != "cabinet" else 1.05
                    })
        # Equipos adicionales para que producción tenga puestos reconocibles.
        for col, row, kind in [
            (8, 11, "machine"), (12, 11, "bench"), (20, 11, "machine"),
            (24, 11, "bench"), (8, 16, "bench"), (20, 16, "machine"),
            (27, 15, "bench"), (11, 20, "cabinet")
        ]:
            if self.map_data["grid"][row][col] == 0:
                props.append({"x": (col+0.5)*TILE_SIZE, "y": (row+0.5)*TILE_SIZE,
                              "kind": kind, "width": 0.90, "height": 0.92})
                self.map_data["solid_rects"].append(
                    pygame.Rect(col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                )
        return props

    def build_prop_surfaces(self):
        """Sprites procedurales livianos: no requieren imágenes externas."""
        sprites = {}
        # Máquina industrial: carcasa, panel, rejillas, botones y base.
        surf = pygame.Surface((72, 88), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, (0, 0, 0, 85), (7, 77, 59, 9))
        pygame.draw.rect(surf, (42, 51, 58), (8, 18, 56, 59), border_radius=4)
        pygame.draw.rect(surf, (91, 108, 117), (12, 12, 48, 61), border_radius=3)
        pygame.draw.rect(surf, (135, 151, 154), (16, 17, 40, 49), 2)
        pygame.draw.rect(surf, (25, 34, 40), (20, 23, 32, 17), border_radius=2)
        pygame.draw.circle(surf, (220, 57, 48), (27, 31), 4)
        pygame.draw.circle(surf, (64, 190, 111), (44, 31), 4)
        for yy in (47, 52, 57):
            pygame.draw.line(surf, (35, 45, 50), (21, yy), (50, yy), 2)
        pygame.draw.rect(surf, (224, 167, 45), (9, 68, 54, 6))
        for xx in range(13, 61, 8):
            pygame.draw.line(surf, (40, 43, 42), (xx, 68), (xx+5, 74), 2)
        pygame.draw.rect(surf, (29, 36, 42), (13, 76, 9, 8))
        pygame.draw.rect(surf, (29, 36, 42), (50, 76, 9, 8))
        sprites["machine"] = surf

        # Banco de trabajo / mesa industrial.
        surf = pygame.Surface((88, 64), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, (0, 0, 0, 75), (8, 52, 72, 9))
        pygame.draw.polygon(surf, (112, 76, 48), [(8, 20), (72, 20), (84, 29), (20, 29)])
        pygame.draw.polygon(surf, (156, 111, 69), [(8, 20), (72, 20), (72, 29), (8, 29)])
        pygame.draw.polygon(surf, (70, 49, 34), [(8, 29), (72, 29), (72, 37), (8, 37)])
        pygame.draw.polygon(surf, (58, 66, 69), [(15, 37), (23, 37), (21, 57), (13, 57)])
        pygame.draw.polygon(surf, (58, 66, 69), [(59, 37), (67, 37), (69, 57), (61, 57)])
        pygame.draw.rect(surf, (187, 190, 178), (31, 12, 22, 8), border_radius=2)
        pygame.draw.line(surf, (40, 45, 46), (34, 14), (49, 14), 2)
        sprites["bench"] = surf

        # Escritorio de oficina con monitor y cajonera.
        surf = pygame.Surface((92, 78), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, (0, 0, 0, 70), (8, 67, 76, 9))
        pygame.draw.polygon(surf, (94, 58, 37), [(8, 30), (75, 30), (88, 39), (20, 39)])
        pygame.draw.polygon(surf, (157, 103, 64), [(8, 30), (75, 30), (75, 39), (8, 39)])
        pygame.draw.polygon(surf, (67, 48, 37), [(8, 39), (75, 39), (75, 47), (8, 47)])
        pygame.draw.rect(surf, (42, 48, 53), (30, 5, 34, 25), border_radius=3)
        pygame.draw.rect(surf, (83, 139, 151), (34, 9, 26, 17), border_radius=2)
        pygame.draw.line(surf, (175, 190, 185), (47, 26), (47, 31), 3)
        pygame.draw.rect(surf, (191, 194, 184), (37, 31, 22, 3))
        pygame.draw.rect(surf, (79, 58, 43), (62, 47, 12, 18))
        pygame.draw.line(surf, (180, 139, 94), (64, 53), (72, 53), 1)
        sprites["desk"] = surf

        # Archivador metálico.
        surf = pygame.Surface((64, 86), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, (0, 0, 0, 75), (5, 78, 54, 7))
        pygame.draw.rect(surf, (73, 87, 94), (8, 7, 48, 72), border_radius=3)
        pygame.draw.rect(surf, (133, 146, 148), (12, 11, 40, 64), 2)
        for yy in (16, 34, 52):
            pygame.draw.rect(surf, (91, 105, 109), (15, yy, 34, 15))
            pygame.draw.line(surf, (194, 199, 187), (25, yy+7), (39, yy+7), 3)
        sprites["cabinet"] = surf
        return sprites

    def draw_world_prop(self, prop, zbuffer, ray_step):
        """Proyecta un objeto 3D tipo billboard y actualiza profundidad por columna."""
        px, py = self.player["x"] / TILE_SIZE, self.player["y"] / TILE_SIZE
        ex, ey = prop["x"] / TILE_SIZE - px, prop["y"] / TILE_SIZE - py
        angle = self.player["dir_angle"]
        dx, dy = math.cos(angle), math.sin(angle)
        plane_x, plane_y = -dy * math.tan(self.fov/2), dx * math.tan(self.fov/2)
        det = plane_x * dy - dx * plane_y
        if abs(det) < 1e-8:
            return
        inv_det = 1.0 / det
        tx = inv_det * (dy * ex - dx * ey)
        depth = inv_det * (-plane_y * ex + plane_x * ey)
        if depth <= 0.22 or depth > 14:
            return
        sprite = self.prop_surfaces[prop["kind"]]
        sh = max(2, min(self.height*2, int(self.height * 0.88 * prop["height"] / depth)))
        sw = max(2, int(sh * sprite.get_width() / sprite.get_height() * prop["width"]))
        center_x = int(self.width/2 * (1 + tx/depth))
        left, right = center_x-sw//2, center_x+sw//2
        if right <= 0 or left >= self.width:
            return
        base_y = self.camera_horizon + int(self.height * 0.44 / depth)
        top = base_y-sh
        scaled = pygame.transform.scale(sprite, (sw, sh))
        for col in range(max(0, left), min(self.width, right)):
            ri = min(self.ray_count-1, max(0, int(col/ray_step)))
            if depth < zbuffer[ri] + 0.025:
                src_x = max(0, min(sw-1, col-left))
                self.screen.blit(scaled.subsurface((src_x, 0, 1, sh)), (col, top))
                zbuffer[ri] = depth

    def setup_random_clue_chain(self):
        targets = [
            {"npc_id": "silvia", "flag": "multi_clue_silvia"},
            {"npc_id": "adrian", "flag": "multi_clue_adrian"},
            {"npc_id": "jessica", "flag": "clue_jessica_two"}
        ]
        chosen = pick_random(targets)
        self.clue_chain = {
            "third_target_npc_id": chosen["npc_id"],
            "third_target_flag": chosen["flag"],
            "ricardo_flag": "clue_ricardo_camioneta",
            "charly_flag": "clue_from_charly"
        }

    def init_npc_ai(self, npc, idx):
        angles = [0.0, math.pi / 2, math.pi, 3 * math.pi / 2]
        ang = angles[idx % len(angles)]
        speed_mult = 1.18 if npc["mood_is_bad"] else 0.92
        spd = NPC_WALK_SPEED * (0.45 if npc["fixed"] else speed_mult)
        return {
            **npc,
            "base_role": npc["role"].split(" (")[0],
            "radius": 14,
            "dir_angle": ang,
            "walk_phase": 0.0,
            "ai_state": "office_wander" if npc["fixed"] else "roam",
            "ai_timer": 1.2 + (idx % 4) * 0.7,
            "mood_timer": 8.0 + (idx % 5) * 4.0,
            "vx": math.cos(ang) * spd,
            "vy": math.sin(ang) * spd,
            "speech_text": "",
            "speech_timer": 0.0,
            "banter_cooldown": 3.0 + (idx % 3) * 1.5,
            "passby_cooldown": 0.0,
            "tour_waypoints": [],
            "tour_idx": 0,
            "tour_talk_cooldown": 0.0,
            "meeting_spot": None
        }

    def start_new_game(self, raw_name=""):
        clean_name = PLAYABLE_CHARACTERS[self.selected_character_index]
        norm = normalize_name(clean_name)
        self.player["name"] = clean_name
        self.player["role_id"] = norm
        selected_def = next((n for n in create_npc_definitions() if normalize_name(n["name"]) == norm), None)
        if selected_def:
            style = selected_def.get("style", {})
            self.player["shirt"] = style.get("shirt", (245, 158, 11))
            self.player["pants"] = style.get("pants", (30, 41, 59))
            self.player["hair"] = style.get("hair", (17, 24, 39))
            self.player["skin"] = style.get("skin", (247, 207, 168))

        if norm == "ricardo":
            self.player["x"], self.player["y"] = 8.5 * TILE_SIZE, 5.4 * TILE_SIZE
            self.player["shirt"] = (127, 29, 29)
        elif norm == "silvia":
            self.player["x"], self.player["y"] = 15.5 * TILE_SIZE, 5.4 * TILE_SIZE
            self.player["shirt"] = (126, 34, 206)
        elif norm == "fernando":
            self.player["x"], self.player["y"] = 21.5 * TILE_SIZE, 5.4 * TILE_SIZE
        elif norm == "jessica":
            self.player["x"], self.player["y"] = 32.5 * TILE_SIZE, 5.4 * TILE_SIZE
        else:
            self.player["x"], self.player["y"] = 18 * TILE_SIZE, 8.6 * TILE_SIZE

        self.day_number = 1
        self.clock_minutes = 8 * 60
        self.shift_ended = False
        self.talked_to_npcs.clear()
        self.unlocked_flags.clear()
        self.setup_random_clue_chain()

        self.player_fight_timer = 0.0
        self.ricardo_check_timer = 2.0
        self.charly_bath_cooldown = 6.0
        self.charly_bath_phase = "none"
        self.trash_started = False
        self.trash_done = False
        self.trash_carrier_id = None
        self.alan_late_spawned = False
        self.lunch_meeting_active = False
        self.gonzalo_outside = False
        self.alan_outside = False
        self.jonathan_sleeping = False
        self.jonathan_slept_today = False

        all_npcs = create_npc_definitions()
        self.npcs = [
            self.init_npc_ai(npc, idx)
            for idx, npc in enumerate(all_npcs)
            if normalize_name(npc["name"]) != norm and npc["id"] != "alan"
        ]
        self.camera_pitch = 0.0
        self.state = "playing"
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        pygame.mouse.get_rel()
        self.mouse_captured = True

    def advance_to_next_day(self):
        self.day_number += 1
        self.clock_minutes = 8 * 60
        self.shift_ended = False
        self.ricardo_check_timer = 2.0
        self.charly_bath_cooldown = 6.0
        self.charly_bath_phase = "none"
        self.trash_started = False
        self.trash_done = False
        self.trash_carrier_id = None
        self.alan_late_spawned = False
        self.lunch_meeting_active = False
        self.gonzalo_outside = False
        self.alan_outside = False
        self.jonathan_sleeping = False
        self.jonathan_slept_today = False

        norm = normalize_name(self.player["name"])
        all_npcs = create_npc_definitions()
        self.npcs = [
            self.init_npc_ai(npc, idx)
            for idx, npc in enumerate(all_npcs)
            if normalize_name(npc["name"]) != norm and npc["id"] != "alan"
        ]

    def circle_intersects_rect(self, cx, cy, cr, rect):
        closest_x = max(rect.left, min(cx, rect.right))
        closest_y = max(rect.top, min(cy, rect.bottom))
        dx = cx - closest_x
        dy = cy - closest_y
        return (dx * dx + dy * dy) < (cr * cr)

    def move_entity_with_collisions(self, entity, move_x, move_y, is_player=False):
        r = entity.get("radius", 14)
        prev_x, prev_y = entity["x"], entity["y"]

        entity["x"] = max(r, min(MAP_WIDTH - r, entity["x"] + move_x))
        for rect in self.map_data["solid_rects"]:
            if self.circle_intersects_rect(entity["x"], entity["y"], r, rect):
                entity["x"] = (rect.left - r) if move_x > 0 else (rect.right + r)

        entity["y"] = max(r, min(MAP_HEIGHT - r, entity["y"] + move_y))
        for rect in self.map_data["solid_rects"]:
            if self.circle_intersects_rect(entity["x"], entity["y"], r, rect):
                entity["y"] = (rect.top - r) if move_y > 0 else (rect.bottom + r)

        if not is_player and not entity.get("fixed", False) and entity["y"] - r < 8 * TILE_SIZE:
            entity["y"] = 8 * TILE_SIZE + r

        entity["x"] = max(TILE_SIZE + r, min(MAP_WIDTH - TILE_SIZE - r, entity["x"]))
        entity["y"] = max(TILE_SIZE + r, min(MAP_HEIGHT - TILE_SIZE - r, entity["y"]))

        return math.hypot(entity["x"] - prev_x, entity["y"] - prev_y) > 0.25

    def update(self, dt):
        if self.state != "playing":
            return

        if not self.shift_ended:
            self.clock_minutes = min(17 * 60, self.clock_minutes + dt * 1.1)
            norm = normalize_name(self.player["name"])

            if not self.alan_late_spawned and self.clock_minutes >= 8 * 60 + 10:
                self.alan_late_spawned = True
                if norm != "alan":
                    alan_def = next((n for n in create_npc_definitions() if n["id"] == "alan"), None)
                    if alan_def:
                        a_npc = self.init_npc_ai(alan_def, 4)
                        a_npc["x"] = 18 * TILE_SIZE
                        a_npc["y"] = (MAP_ROWS - 1.6) * TILE_SIZE
                        a_npc["speech_text"] = "¡Perdón el retraso, había quilombo en el bondi!"
                        a_npc["speech_timer"] = 3.5
                        self.npcs.append(a_npc)

            if not self.lunch_meeting_active and 12 * 60 + 45 <= self.clock_minutes < 13 * 60 + 35:
                self.lunch_meeting_active = True
                self.gonzalo_outside = True
                self.alan_outside = True
                spots = [
                    (14.0 * TILE_SIZE, 13.8 * TILE_SIZE),
                    (15.2 * TILE_SIZE, 13.3 * TILE_SIZE),
                    (16.8 * TILE_SIZE, 13.3 * TILE_SIZE),
                    (18.0 * TILE_SIZE, 13.8 * TILE_SIZE),
                    (14.0 * TILE_SIZE, 15.3 * TILE_SIZE),
                    (15.5 * TILE_SIZE, 15.6 * TILE_SIZE)
                ]
                s_idx = 0
                for npc in self.npcs:
                    if npc["fixed"]:
                        continue
                    if npc["id"] in ("gonzalo", "alan"):
                        npc["ai_state"] = "outside_break"
                    else:
                        npc["ai_state"] = "table_meeting"
                        npc["meeting_spot"] = spots[s_idx % len(spots)]
                        s_idx += 1
                        npc["speech_text"] = "¡12:45! Todos a la mesa a ranchar."
                        npc["speech_timer"] = 3.0

            if not self.jonathan_slept_today and not self.jonathan_sleeping and 13 * 60 + 10 <= self.clock_minutes < 13 * 60 + 25:
                j_npc = next((n for n in self.npcs if n["id"] == "jonathan"), None)
                if j_npc:
                    self.jonathan_sleeping = True
                    self.jonathan_slept_today = True
                    j_npc["ai_state"] = "going_sleep"
                    j_npc["speech_text"] = "Me voy al cuartito a clavar una siesta..."
                    j_npc["speech_timer"] = 3.0

            if self.gonzalo_outside and self.clock_minutes >= 13 * 60 + 20:
                self.gonzalo_outside = False
                if norm != "gonzalo" and not any(n["id"] == "gonzalo" for n in self.npcs):
                    g_def = next((n for n in create_npc_definitions() if n["id"] == "gonzalo"), None)
                    if g_def:
                        g_npc = self.init_npc_ai(g_def, 3)
                        g_npc["x"] = 18 * TILE_SIZE
                        g_npc["y"] = (MAP_ROWS - 1.6) * TILE_SIZE
                        g_npc["ai_state"] = "table_meeting"
                        g_npc["meeting_spot"] = (18.2 * TILE_SIZE, 14.6 * TILE_SIZE)
                        g_npc["speech_text"] = "¡13:20! Ya volví."
                        g_npc["speech_timer"] = 3.0
                        self.npcs.append(g_npc)

            if self.jonathan_sleeping and self.clock_minutes >= 13 * 60 + 25:
                self.jonathan_sleeping = False
                j_npc = next((n for n in self.npcs if n["id"] == "jonathan"), None)
                if j_npc:
                    j_npc["x"] = 32.5 * TILE_SIZE
                    j_npc["y"] = 18.2 * TILE_SIZE
                    j_npc["ai_state"] = "roam"
                    j_npc["speech_text"] = "¡13:25! Qué buena siesta me clavé."
                    j_npc["speech_timer"] = 3.2

            if self.alan_outside and self.clock_minutes >= 13 * 60 + 35:
                self.alan_outside = False
                self.lunch_meeting_active = False
                if norm != "alan" and not any(n["id"] == "alan" for n in self.npcs):
                    a_def = next((n for n in create_npc_definitions() if n["id"] == "alan"), None)
                    if a_def:
                        a_npc = self.init_npc_ai(a_def, 4)
                        a_npc["x"] = 18 * TILE_SIZE
                        a_npc["y"] = (MAP_ROWS - 1.6) * TILE_SIZE
                        a_npc["speech_text"] = "¡13:35! Acá llegó el que faltaba."
                        a_npc["speech_timer"] = 3.0
                        self.npcs.append(a_npc)
                for npc in self.npcs:
                    if npc["ai_state"] == "table_meeting":
                        npc["ai_state"] = "roam"

            if not self.trash_started and not self.trash_done and self.clock_minutes >= 16 * 60:
                self.trash_started = True
                pool = [n for n in self.npcs if not n["fixed"] and n["id"] != "fernando"]
                if pool:
                    chosen = pick_random(pool)
                    self.trash_carrier_id = chosen["id"]
                    chosen["ai_state"] = "taking_trash"
                    chosen["speech_text"] = pick_random(TRASH_INSULT_LINES)
                    chosen["speech_timer"] = 3.2

            if self.clock_minutes >= 17 * 60:
                self.shift_ended = True
                for npc in self.npcs:
                    npc["ai_state"] = "leaving"
                    npc["speech_text"] = "¡Son las 17:00, me rajo!"
                    npc["speech_timer"] = 3.0

        keys = pygame.key.get_pressed()
        angle = self.player["dir_angle"]
        forward = 0.0
        strafe = 0.0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            forward += 1.0
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            forward -= 1.0
        if keys[pygame.K_d]:
            strafe += 1.0
        if keys[pygame.K_a]:
            strafe -= 1.0
        # Flechas izquierda/derecha giran la cámara; A/D hacen desplazamiento lateral.
        turn_speed = 1.8 * dt
        if keys[pygame.K_LEFT]:
            self.player["dir_angle"] -= turn_speed
        if keys[pygame.K_RIGHT]:
            self.player["dir_angle"] += turn_speed
        angle = self.player["dir_angle"]
        move_x = math.cos(angle) * forward - math.sin(angle) * strafe
        move_y = math.sin(angle) * forward + math.cos(angle) * strafe
        if move_x or move_y:
            length = math.hypot(move_x, move_y)
            move_x /= length
            move_y /= length
            self.player["walk_phase"] += dt * 12.0
            self.move_entity_with_collisions(
                self.player, move_x * PLAYER_SPEED * dt,
                move_y * PLAYER_SPEED * dt, True
            )
        else:
            self.player["walk_phase"] = 0.0

        if self.player_fight_timer > 0.0:
            self.player_fight_timer = max(0.0, self.player_fight_timer - dt)
            self.player["walk_phase"] += dt * 24.0

        # Evento baño Charly
        excluded_chant = {"ricardo", "silvia", "fernando", "jessica"}
        charly_npc = next((n for n in self.npcs if n["id"] == "charly"), None)
        if charly_npc and not self.shift_ended:
            if self.charly_bath_phase == "none":
                self.charly_bath_cooldown -= dt
                if self.charly_bath_cooldown <= 0.0:
                    self.charly_bath_cooldown = 15.0 + random.random() * 10.0
                    if random.random() < 0.55:
                        self.charly_bath_phase = "running"
                        self.charly_bath_timer = 5.0
                        charly_npc["ai_state"] = "bathroom"
                        charly_npc["speech_text"] = "¡NO AGUANTO MÁS, AL BAÑOOOO!"
                        charly_npc["speech_timer"] = 2.6
                        for other in self.npcs:
                            if other["id"] not in excluded_chant and other["id"] != "charly":
                                other["speech_text"] = "empuja enmpuja caca viene"
                                other["speech_timer"] = 3.2
            elif self.charly_bath_phase == "running":
                self.charly_bath_timer = max(0.0, self.charly_bath_timer - dt)
                dist_door = math.hypot(self.bathroom_door_pos[0] - charly_npc["x"], self.bathroom_door_pos[1] - charly_npc["y"])
                if dist_door < 22 or self.charly_bath_timer <= 0.0:
                    self.charly_bath_phase = "inside"
                    self.charly_bath_timer = 3.5
                    charly_npc["x"], charly_npc["y"] = self.bathroom_inside_pos
                    charly_npc["speech_text"] = "¡OCUPADOOOO! ¡EMPUJA!"
                    charly_npc["speech_timer"] = 3.2
            elif self.charly_bath_phase == "inside":
                self.charly_bath_timer = max(0.0, self.charly_bath_timer - dt)
                if self.charly_bath_timer <= 0.0:
                    self.charly_bath_phase = "none"
                    charly_npc["ai_state"] = "roam"
                    charly_npc["x"], charly_npc["y"] = 3.5 * TILE_SIZE, 18.1 * TILE_SIZE
                    charly_npc["speech_text"] = "¡Uf, qué alivio!"
                    charly_npc["speech_timer"] = 2.2

        # Recorrido de Ricardo (sin despedir a nadie)
        ricardo_npc = next((n for n in self.npcs if n["id"] == "ricardo"), None)
        if ricardo_npc and not self.shift_ended and ricardo_npc["ai_state"] != "leaving":
            if self.ricardo_check_timer > 0.0:
                self.ricardo_check_timer -= dt
            if ricardo_npc["ai_state"] != "ricardo_tour" and self.ricardo_check_timer <= 0.0 and random.random() < 0.35:
                self.ricardo_check_timer = 14.0 + random.random() * 8.0
                ricardo_npc["ai_state"] = "ricardo_tour"
                ricardo_npc["tour_waypoints"] = [
                    (6.5 * TILE_SIZE, 8.8 * TILE_SIZE),
                    (13.0 * TILE_SIZE, 12.5 * TILE_SIZE),
                    (24.0 * TILE_SIZE, 12.5 * TILE_SIZE),
                    (18.0 * TILE_SIZE, 17.5 * TILE_SIZE),
                    (6.5 * TILE_SIZE, 8.8 * TILE_SIZE),
                    (5.5 * TILE_SIZE, 4.6 * TILE_SIZE)
                ]
                ricardo_npc["tour_idx"] = 0
                ricardo_npc["tour_talk_cooldown"] = 0.0
                ricardo_npc["speech_text"] = (
                    pick_random(RICARDO_BAD_JOKES)
                    if ricardo_npc["mood_is_bad"]
                    else pick_random(RICARDO_GOOD_NO_PAY_LINES)
                )
                ricardo_npc["speech_timer"] = 3.2

        self.update_npcs(dt)

        closest = None
        min_dist = 88.0
        for npc in self.npcs:
            vx = npc["x"] - self.player["x"]
            vy = npc["y"] - self.player["y"]
            d = math.hypot(vx, vy)
            if d < min_dist and d > 0:
                target_angle = math.atan2(vy, vx)
                delta = (target_angle - self.player["dir_angle"] + math.pi) % (2*math.pi) - math.pi
                if abs(delta) < math.radians(48):
                    closest = npc
                    min_dist = d
        self.nearby_npc = closest

    def update_npcs(self, dt):
        boss_pool = BOSS_PASSBY_INSULTS.get(self.player["role_id"])
        for i in range(len(self.npcs) - 1, -1, -1):
            npc = self.npcs[i]

            if npc["speech_timer"] > 0.0:
                npc["speech_timer"] = max(0.0, npc["speech_timer"] - dt)
                if npc["speech_timer"] == 0.0:
                    npc["speech_text"] = ""
            if npc["banter_cooldown"] > 0.0:
                npc["banter_cooldown"] = max(0.0, npc["banter_cooldown"] - dt)
            if npc["passby_cooldown"] > 0.0:
                npc["passby_cooldown"] = max(0.0, npc["passby_cooldown"] - dt)

            if boss_pool and npc["passby_cooldown"] <= 0.0 and not self.shift_ended:
                if math.hypot(npc["x"] - self.player["x"], npc["y"] - self.player["y"]) < 88.0:
                    npc["passby_cooldown"] = 8.0
                    npc["speech_text"] = pick_random(boss_pool)
                    npc["speech_timer"] = 3.2

            if npc["ai_state"] == "outside_break":
                npc["walk_phase"] += dt * 11.0
                tx, ty = 18 * TILE_SIZE, (MAP_ROWS - 1.5) * TILE_SIZE
                dx, dy = tx - npc["x"], ty - npc["y"]
                dist = math.hypot(dx, dy)
                if dist > 14.0:                    self.move_entity_with_collisions(npc, (dx / dist) * NPC_WALK_SPEED * 1.25 * dt, (dy / dist) * NPC_WALK_SPEED * 1.25 * dt, False)
                    npc["dir_angle"] = math.atan2(dx, dy)
                else:
                    npc["walk_phase"] = 0.0
                    if npc["speech_timer"] <= 0.0:
                        npc["speech_text"] = "Afuera tomando aire..."
                        npc["speech_timer"] = 3.0
                continue

            if self.shift_ended or npc["ai_state"] == "leaving":
                npc["walk_phase"] += dt * 12.0
                tx, ty = 18 * TILE_SIZE, (MAP_ROWS - 1.3) * TILE_SIZE
                dx, dy = tx - npc["x"], ty - npc["y"]
                dist = math.hypot(dx, dy)
                if dist > 12.0:
                    npc["x"] += (dx / dist) * NPC_WALK_SPEED * 1.4 * dt
                    npc["y"] += (dy / dist) * NPC_WALK_SPEED * 1.4 * dt
                    npc["dir_angle"] = math.atan2(dx, dy)
                else:
                    self.npcs.pop(i)
                continue

            if npc["ai_state"] == "going_sleep":
                dx, dy = 32.5 * TILE_SIZE - npc["x"], 18.4 * TILE_SIZE - npc["y"]
                dist = math.hypot(dx, dy)
                if dist > 12.0:
                    npc["walk_phase"] += dt * 11.0
                    npc["dir_angle"] = math.atan2(dx, dy)
                    self.move_entity_with_collisions(npc, (dx / dist) * NPC_WALK_SPEED * 1.3 * dt, (dy / dist) * NPC_WALK_SPEED * 1.3 * dt, False)
                else:
                    npc["ai_state"] = "sleeping"
                    npc["x"], npc["y"] = 32.5 * TILE_SIZE, 21.0 * TILE_SIZE
                    npc["walk_phase"] = 0.0
                    npc["speech_text"] = "Zzz... Zzz... (durmiendo)"
                    npc["speech_timer"] = 15.0
                continue

            if npc["ai_state"] == "sleeping":
                npc["walk_phase"] = 0.0
                continue

            if npc["ai_state"] == "table_meeting" and npc["meeting_spot"]:
                dx, dy = npc["meeting_spot"][0] - npc["x"], npc["meeting_spot"][1] - npc["y"]
                dist = math.hypot(dx, dy)
                if dist > 10.0:
                    npc["walk_phase"] += dt * 10.0
                    npc["dir_angle"] = math.atan2(dx, dy)
                    self.move_entity_with_collisions(npc, (dx / dist) * NPC_WALK_SPEED * 1.2 * dt, (dy / dist) * NPC_WALK_SPEED * 1.2 * dt, False)
                else:
                    npc["walk_phase"] = 0.0
                continue

            if npc["id"] == self.trash_carrier_id and npc["ai_state"] == "taking_trash":
                dx, dy = 18 * TILE_SIZE - npc["x"], (MAP_ROWS - 1.3) * TILE_SIZE - npc["y"]
                dist = math.hypot(dx, dy)
                if dist > 12.0:
                    npc["walk_phase"] += dt * 10.0
                    npc["dir_angle"] = math.atan2(dx, dy)
                    npc["x"] += (dx / dist) * NPC_WALK_SPEED * 1.15 * dt
                    npc["y"] += (dy / dist) * NPC_WALK_SPEED * 1.15 * dt
                else:
                    self.trash_done = True
                    self.trash_carrier_id = None
                    npc["ai_state"] = "roam"
                    npc["speech_text"] = "¡Listo, basura afuera!"
                    npc["speech_timer"] = 2.8
                continue

            if npc["id"] == "charly" and self.charly_bath_phase == "running":
                dx, dy = self.bathroom_door_pos[0] - npc["x"], self.bathroom_door_pos[1] - npc["y"]
                length = math.hypot(dx, dy) or 1.0
                npc["walk_phase"] += dt * 18.0
                npc["dir_angle"] = math.atan2(dx, dy)
                npc["x"] += (dx / length) * NPC_WALK_SPEED * 2.15 * dt
                npc["y"] += (dy / length) * NPC_WALK_SPEED * 2.15 * dt
                continue

            if npc["id"] == "ricardo" and npc["ai_state"] == "ricardo_tour":
                wps = npc["tour_waypoints"]
                if npc["tour_idx"] >= len(wps):
                    npc["ai_state"] = "office_wander"
                    npc["walk_phase"] = 0.0
                    continue
                wx, wy = wps[npc["tour_idx"]]
                dx, dy = wx - npc["x"], wy - npc["y"]
                dist = math.hypot(dx, dy)
                if npc["tour_talk_cooldown"] > 0.0:
                    npc["tour_talk_cooldown"] = max(0.0, npc["tour_talk_cooldown"] - dt)

                if npc["tour_talk_cooldown"] <= 0.0:
                    for other in self.npcs:
                        if other["id"] == "ricardo":
                            continue
                        if math.hypot(other["x"] - npc["x"], other["y"] - npc["y"]) < 76.0:
                            npc["tour_talk_cooldown"] = 3.2
                            if npc["mood_is_bad"]:
                                joke = pick_random(RICARDO_BAD_JOKES)
                                npc["speech_text"] = f"{other['name']}, escuchá esto: {joke}"
                                other["speech_text"] = "¡Ja, qué chiste más tonto, Ricardo!"
                            else:
                                line = pick_random(RICARDO_GOOD_NO_PAY_LINES)
                                npc["speech_text"] = f"{other['name']}, {line}"
                                other["speech_text"] = "¿Cómo que hoy no cobramos, Ricardo?"
                            npc["speech_timer"] = 3.4
                            other["speech_timer"] = 2.6
                            break

                if dist > 10.0:
                    npc["walk_phase"] += dt * 11.0
                    npc["dir_angle"] = math.atan2(dx, dy)
                    npc["x"] += (dx / dist) * NPC_WALK_SPEED * 1.15 * dt
                    npc["y"] += (dy / dist) * NPC_WALK_SPEED * 1.15 * dt
                else:
                    npc["tour_idx"] += 1
                continue

            npc["mood_timer"] -= dt
            if npc["mood_timer"] <= 0.0:
                npc["mood_timer"] = 11.0 + random.random() * 10.0
                if random.random() < 0.65:
                    npc["mood_is_bad"] = not npc["mood_is_bad"]
                    mood_label = "Mal humor" if npc["mood_is_bad"] else "Buen humor"
                    npc["role"] = f"{npc['base_role']} ({mood_label})"

            if npc["fixed"]:
                npc["ai_timer"] -= dt
                if npc["ai_timer"] <= 0.0:
                    ang = random.random() * math.pi * 2
                    npc["vx"] = math.cos(ang) * NPC_WALK_SPEED * 0.45
                    npc["vy"] = math.sin(ang) * NPC_WALK_SPEED * 0.45
                    npc["ai_timer"] = 1.6 + random.random() * 2.0
                if npc["id"] == "ricardo":
                    min_x, max_x = 2.2 * TILE_SIZE, 10.8 * TILE_SIZE
                elif npc["id"] == "silvia":
                    min_x, max_x = 13.2 * TILE_SIZE, 17.8 * TILE_SIZE
                elif npc["id"] == "fernando":
                    min_x, max_x = 19.2 * TILE_SIZE, 23.0 * TILE_SIZE
                else:
                    min_x, max_x = 26.2 * TILE_SIZE, 33.5 * TILE_SIZE
                nx = npc["x"] + npc["vx"] * dt
                ny = npc["y"] + npc["vy"] * dt
                if nx < min_x or nx > max_x or ny < 2.0 * TILE_SIZE or ny > 6.1 * TILE_SIZE:
                    npc["vx"] = -npc["vx"]
                    npc["vy"] = -npc["vy"]
                else:
                    npc["dir_angle"] = math.atan2(npc["vx"], npc["vy"])
                    self.move_entity_with_collisions(npc, npc["vx"] * dt, npc["vy"] * dt, True)
                    npc["walk_phase"] += dt * 8.0
                continue

            npc["ai_timer"] -= dt
            if npc["ai_state"] == "fighting":
                npc["walk_phase"] += dt * 24.0
                if npc["ai_timer"] <= 0.0:
                    npc["ai_state"] = "roam"
                continue

            if npc["ai_timer"] <= 0.0:
                ang = random.random() * math.pi * 2
                spd = NPC_WALK_SPEED * (1.2 if npc["mood_is_bad"] else 0.9)
                npc["vx"] = math.cos(ang) * spd
                npc["vy"] = math.sin(ang) * spd
                npc["ai_timer"] = 1.8 + random.random() * 2.6
                if npc["speech_timer"] <= 0.0 and random.random() < 0.35:
                    npc["speech_text"] = pick_random(NPC_BAD_MOOD_SOLO if npc["mood_is_bad"] else NPC_GOOD_MOOD_SOLO)
                    npc["speech_timer"] = 2.6

            moved = self.move_entity_with_collisions(npc, npc["vx"] * dt, npc["vy"] * dt, False)
            if not moved:
                ang = random.random() * math.pi * 2
                npc["vx"] = math.cos(ang) * NPC_WALK_SPEED
                npc["vy"] = math.sin(ang) * NPC_WALK_SPEED
            else:
                npc["walk_phase"] += dt * 9.0
                npc["dir_angle"] = math.atan2(npc["vx"], npc["vy"])

            if npc["banter_cooldown"] <= 0.0:
                for other in self.npcs:
                    if other["id"] == npc["id"] or other["fixed"] or other["banter_cooldown"] > 0.0:
                        continue
                    if math.hypot(other["x"] - npc["x"], other["y"] - npc["y"]) < 54.0:
                        npc["banter_cooldown"] = 8.0
                        other["banter_cooldown"] = 8.0
                        if npc["mood_is_bad"] and other["mood_is_bad"]:
                            npc["ai_state"] = "fighting"
                            other["ai_state"] = "fighting"
                            npc["ai_timer"] = 3.2
                            other["ai_timer"] = 3.2
                            line = f"¡PELEA! {pick_random(NPC_FIGHT_LINES)}"
                            npc["speech_text"] = line
                            other["speech_text"] = line
                        else:
                            npc["speech_text"] = f"{other['name']}: {pick_random(NPC_BANTER_LINES)}"
                            other["speech_text"] = f"{npc['name']}: {pick_random(NPC_BANTER_LINES)}"
                        npc["speech_timer"] = 3.2
                        other["speech_timer"] = 3.2
                        break

    def open_dialogue(self, npc):
        self.active_npc = npc
        self.talked_to_npcs.add(npc["id"])
        if len(self.talked_to_npcs) >= 3:
            self.unlocked_flags.add(self.clue_chain["third_target_flag"])
        if "ricardo" in self.talked_to_npcs or "jessica" in self.talked_to_npcs:
            self.unlocked_flags.add(self.clue_chain["ricardo_flag"])

        self.visible_questions = [
            q for q in npc["questions"]
            if not q.get("unlocked_by") or q["unlocked_by"] in self.unlocked_flags
        ]
        self.dialogue_response = f"Elegí una pregunta para {npc['name']} (1-{max(1, len(self.visible_questions))} o clic)."
        self.state = "dialogue"

    def select_question(self, idx):
        if not self.active_npc or idx < 0 or idx >= len(self.visible_questions):
            return
        q = self.visible_questions[idx]
        npc = self.active_npc
        prefix = "¡Estoy re cruzado hoy! " if npc["mood_is_bad"] else "Hoy ando de diez, che: "
        reply = prefix + pick_random(q["responses"])
        if npc["id"] == "charly" and q["id"] == "gossip":
            self.unlocked_flags.add(self.clue_chain["charly_flag"])
        self.dialogue_response = f"«{reply}»"

    def draw_character(self, surface, cam_x, cam_y, entity, name, is_player=False, mood_is_bad=False, speech_text="", is_nearby=False):
        """Dibuja personajes con volumen, ropa, rostro y animación sin alterar su IA."""
        sx = int(entity["x"] - cam_x)
        sy = int(entity["y"] - cam_y)
        phase = entity.get("walk_phase", 0.0)
        moving = abs(phase) > 0.05
        swing = math.sin(phase) * 4.0 if moving else 0.0
        bob = abs(math.sin(phase * 2.0)) * 1.5 if moving else 0.0

        style = entity.get("style", {})
        shirt = entity.get("shirt", style.get("shirt", (120, 120, 120)))
        pants = entity.get("pants", style.get("pants", (40, 45, 55)))
        hair = entity.get("hair", style.get("hair", (35, 30, 25)))
        skin = entity.get("skin", style.get("skin", (240, 195, 160)))

        def shade(color, amount):
            return tuple(max(0, min(255, int(v + amount))) for v in color)

        # Indicador de proximidad y sombra proyectada.
        if is_nearby:
            pygame.draw.ellipse(surface, (34, 197, 94), (sx - 19, sy + 5, 38, 15), 2)
        pygame.draw.ellipse(surface, (18, 24, 31), (sx - 14, sy + 8, 28, 9))
        pygame.draw.ellipse(surface, (0, 0, 0, 45), (sx - 10, sy + 9, 20, 5))

        # Piernas y calzado.
        hip_y = sy - 1 - bob
        leg_l = (sx - 4, hip_y + 5)
        leg_r = (sx + 4, hip_y + 5)
        foot_l = (sx - 5 - swing, sy + 13 - bob)
        foot_r = (sx + 5 + swing, sy + 13 - bob)
        pygame.draw.line(surface, shade(pants, -28), leg_l, foot_l, 6)
        pygame.draw.line(surface, pants, leg_l, foot_l, 4)
        pygame.draw.line(surface, shade(pants, -28), leg_r, foot_r, 6)
        pygame.draw.line(surface, pants, leg_r, foot_r, 4)
        pygame.draw.ellipse(surface, (24, 28, 34), (foot_l[0] - 4, foot_l[1] - 1, 9, 5))
        pygame.draw.ellipse(surface, (24, 28, 34), (foot_r[0] - 4, foot_r[1] - 1, 9, 5))

        # Brazos detrás del torso.
        arm_y = sy - 8 - bob
        pygame.draw.line(surface, shade(skin, -30), (sx - 8, arm_y), (sx - 11 - swing * 0.35, sy + 2), 5)
        pygame.draw.line(surface, skin, (sx - 8, arm_y), (sx - 11 - swing * 0.35, sy + 2), 3)
        pygame.draw.line(surface, shade(skin, -30), (sx + 8, arm_y), (sx + 11 + swing * 0.35, sy + 2), 5)
        pygame.draw.line(surface, skin, (sx + 8, arm_y), (sx + 11 + swing * 0.35, sy + 2), 3)

        # Torso con luces, costuras y cuello.
        torso = pygame.Rect(sx - 9, sy - 13 - int(bob), 18, 17)
        pygame.draw.rect(surface, shade(shirt, -45), torso.inflate(3, 2), border_radius=6)
        pygame.draw.rect(surface, shirt, torso, border_radius=5)
        pygame.draw.line(surface, shade(shirt, 35), (sx - 5, torso.y + 3), (sx - 5, torso.bottom - 3), 2)
        pygame.draw.line(surface, shade(shirt, -35), (sx + 5, torso.y + 3), (sx + 5, torso.bottom - 3), 2)
        pygame.draw.line(surface, (225, 225, 225), (sx, torso.y + 4), (sx, torso.bottom - 2), 1)
        pygame.draw.rect(surface, (25, 30, 36), torso, 1, border_radius=5)
        pygame.draw.rect(surface, shade(skin, -12), (sx - 3, sy - 16 - int(bob), 6, 5), border_radius=2)

        # Cabeza, orejas y rasgos.
        head_y = sy - 22 - int(bob)
        pygame.draw.circle(surface, shade(skin, -35), (sx, head_y + 1), 8)
        pygame.draw.circle(surface, skin, (sx, head_y), 7)
        pygame.draw.circle(surface, shade(skin, 18), (sx - 2, head_y - 3), 3)
        pygame.draw.circle(surface, shade(skin, -15), (sx - 8, head_y), 2)
        pygame.draw.circle(surface, shade(skin, -15), (sx + 8, head_y), 2)

        # Pelo: silueta y mechones.
        pygame.draw.arc(surface, shade(hair, -35), (sx - 9, head_y - 9, 18, 15), math.pi, math.tau, 5)
        pygame.draw.arc(surface, hair, (sx - 8, head_y - 10, 16, 13), math.pi, math.tau, 4)
        pygame.draw.line(surface, shade(hair, 25), (sx - 5, head_y - 7), (sx - 1, head_y - 9), 2)
        pygame.draw.line(surface, shade(hair, -20), (sx + 2, head_y - 8), (sx + 6, head_y - 5), 2)

        # Expresión simple según humor.
        eye_y = head_y - 1
        pygame.draw.circle(surface, (35, 30, 28), (sx - 3, eye_y), 1)
        pygame.draw.circle(surface, (35, 30, 28), (sx + 3, eye_y), 1)
        if mood_is_bad and not is_player:
            pygame.draw.line(surface, (65, 35, 30), (sx - 5, eye_y - 3), (sx - 1, eye_y - 2), 1)
            pygame.draw.line(surface, (65, 35, 30), (sx + 1, eye_y - 2), (sx + 5, eye_y - 3), 1)
            pygame.draw.arc(surface, (90, 35, 35), (sx - 2, head_y + 1, 5, 4), math.pi, math.tau, 1)
        else:
            pygame.draw.arc(surface, (105, 45, 45), (sx - 2, head_y, 5, 4), 0, math.pi, 1)

        # Contorno exterior para separar el personaje del suelo.
        pygame.draw.ellipse(surface, (25, 30, 36), (sx - 8, head_y - 8, 16, 16), 1)

        # Placa de nombre.
        plate_bg = (250, 190, 45) if is_player else (25, 35, 48)
        plate_fg = (25, 28, 32) if is_player else (245, 247, 250)
        name_surf = self.font_label.render(name, True, plate_fg)
        dot_w = 12 if not is_player else 0
        pw = name_surf.get_width() + 12 + dot_w
        ph = 19
        px = sx - pw // 2
        py = sy - 52
        pygame.draw.rect(surface, (8, 12, 18), (px, py + 2, pw, ph), border_radius=6)
        pygame.draw.rect(surface, plate_bg, (px, py, pw, ph), border_radius=6)
        pygame.draw.rect(surface, shade(plate_bg, -55), (px, py, pw, ph), 1, border_radius=6)
        surface.blit(name_surf, (px + 6, py + 2))
        if not is_player:
            dot_col = (239, 68, 68) if mood_is_bad else (34, 197, 94)
            pygame.draw.circle(surface, dot_col, (px + pw - 8, py + ph // 2), 3)

        # Globo de diálogo con cola y ancho limitado a pantalla.
        if speech_text:
            bub_surf = self.font_bubble.render(speech_text, True, (28, 32, 38))
            max_width = max(130, min(330, surface.get_width() - 24))
            if bub_surf.get_width() > max_width - 16:
                words = speech_text.split()
                lines, current = [], ""
                for word in words:
                    trial = (current + " " + word).strip()
                    if self.font_bubble.size(trial)[0] <= max_width - 16:
                        current = trial
                    else:
                        if current:
                            lines.append(current)
                        current = word
                if current:
                    lines.append(current)
                lines = lines[:3]
                rendered = [self.font_bubble.render(line, True, (28, 32, 38)) for line in lines]
                bw = max(line.get_width() for line in rendered) + 16
                bh = len(rendered) * 15 + 10
            else:
                rendered = [bub_surf]
                bw, bh = bub_surf.get_width() + 16, 25
            bx = max(5, min(surface.get_width() - bw - 5, sx - bw // 2))
            by = max(4, py - bh - 7)
            pygame.draw.polygon(surface, (250, 248, 224), [(sx - 4, by + bh), (sx + 4, by + bh), (sx, by + bh + 7)])
            pygame.draw.rect(surface, (250, 248, 224), (bx, by, bw, bh), border_radius=7)
            pygame.draw.rect(surface, (90, 86, 65), (bx, by, bw, bh), 1, border_radius=7)
            for li, line_surf in enumerate(rendered):
                surface.blit(line_surf, (bx + 8, by + 5 + li * 15))

    def cast_wall(self, ray_angle):
        """DDA: devuelve distancia perpendicular, tipo de bloque y cara golpeada."""
        px = self.player["x"] / TILE_SIZE
        py = self.player["y"] / TILE_SIZE
        ray_x = math.cos(ray_angle)
        ray_y = math.sin(ray_angle)
        map_x, map_y = int(px), int(py)
        delta_x = abs(1.0 / ray_x) if abs(ray_x) > 1e-9 else 1e30
        delta_y = abs(1.0 / ray_y) if abs(ray_y) > 1e-9 else 1e30
        if ray_x < 0:
            step_x, side_x = -1, (px - map_x) * delta_x
        else:
            step_x, side_x = 1, (map_x + 1.0 - px) * delta_x
        if ray_y < 0:
            step_y, side_y = -1, (py - map_y) * delta_y
        else:
            step_y, side_y = 1, (map_y + 1.0 - py) * delta_y
        side = 0
        grid = self.map_data["grid"]
        hit = 1
        for _ in range(90):
            if side_x < side_y:
                side_x += delta_x
                map_x += step_x
                side = 0
            else:
                side_y += delta_y
                map_y += step_y
                side = 1
            if map_x < 0 or map_y < 0 or map_x >= MAP_COLS or map_y >= MAP_ROWS:
                hit = 1
                break
            cell = grid[map_y][map_x]
            if cell == 1:
                hit = cell
                break
        if side == 0:
            distance = (map_x - px + (1 - step_x) / 2) / (ray_x if abs(ray_x) > 1e-9 else 1e-9)
        else:
            distance = (map_y - py + (1 - step_y) / 2) / (ray_y if abs(ray_y) > 1e-9 else 1e-9)
        return max(0.05, distance), hit, side

    def draw_fps_sprite(self, entity, zbuffer, ray_step):
        """Dibuja un NPC como figura humana billboard, con perspectiva y oclusión."""
        px = self.player["x"] / TILE_SIZE
        py = self.player["y"] / TILE_SIZE
        ex = entity["x"] / TILE_SIZE - px
        ey = entity["y"] / TILE_SIZE - py
        angle = self.player["dir_angle"]
        dir_x, dir_y = math.cos(angle), math.sin(angle)
        plane_x = -dir_y * math.tan(self.fov / 2)
        plane_y = dir_x * math.tan(self.fov / 2)
        det = plane_x * dir_y - dir_x * plane_y
        if abs(det) < 1e-8:
            return
        inv_det = 1.0 / det
        transform_x = inv_det * (dir_y * ex - dir_x * ey)
        transform_y = inv_det * (-plane_y * ex + plane_x * ey)
        if transform_y <= 0.18 or transform_y > 22:
            return
        sx = int((self.width / 2) * (1 + transform_x / transform_y))
        sprite_h = min(int(abs(self.height / transform_y) * 0.72), self.height * 2)
        sprite_w = max(4, int(sprite_h * 0.38))
        top = self.camera_horizon - sprite_h // 2 + int(sprite_h * 0.08)
        left = sx - sprite_w // 2
        right = sx + sprite_w // 2
        if right < 0 or left >= self.width:
            return

        style = entity.get("style", {})
        shirt = entity.get("shirt", style.get("shirt", (170, 120, 70)))
        pants = entity.get("pants", style.get("pants", (40, 45, 55)))
        hair = entity.get("hair", style.get("hair", (35, 30, 25)))
        skin = entity.get("skin", style.get("skin", (240, 195, 160)))
        dark = lambda c, n: tuple(max(0, int(v*n)) for v in c)
        # Construimos el personaje en una superficie pequeña y la escalamos.
        sw, sh = 44, 92
        sprite = pygame.Surface((sw, sh), pygame.SRCALPHA)
        phase = entity.get("walk_phase", 0.0)
        swing = int(math.sin(phase) * 3) if abs(phase) > 0.05 else 0
        pygame.draw.ellipse(sprite, (12, 16, 20, 100), (8, 84, 28, 7))
        pygame.draw.line(sprite, dark(pants, .55), (18, 59), (15-swing, 84), 8)
        pygame.draw.line(sprite, pants, (18, 59), (15-swing, 82), 5)
        pygame.draw.line(sprite, dark(pants, .55), (26, 59), (29+swing, 84), 8)
        pygame.draw.line(sprite, pants, (26, 59), (29+swing, 82), 5)
        pygame.draw.ellipse(sprite, (25, 28, 31), (8-swing, 80, 14, 6))
        pygame.draw.ellipse(sprite, (25, 28, 31), (24+swing, 80, 14, 6))
        pygame.draw.line(sprite, dark(skin, .72), (13, 34), (8-swing, 59), 7)
        pygame.draw.line(sprite, skin, (13, 34), (8-swing, 59), 4)
        pygame.draw.line(sprite, dark(skin, .72), (31, 34), (36+swing, 59), 7)
        pygame.draw.line(sprite, skin, (31, 34), (36+swing, 59), 4)
        pygame.draw.polygon(sprite, dark(shirt, .55), [(11, 31), (17, 27), (27, 27), (33, 31), (31, 61), (13, 61)])
        pygame.draw.polygon(sprite, shirt, [(13, 31), (18, 29), (26, 29), (31, 31), (29, 58), (15, 58)])
        pygame.draw.line(sprite, tuple(min(255, v+40) for v in shirt), (18, 32), (18, 55), 2)
        pygame.draw.rect(sprite, skin, (19, 23, 6, 8))
        pygame.draw.ellipse(sprite, dark(skin, .75), (13, 4, 19, 23))
        pygame.draw.ellipse(sprite, skin, (14, 3, 17, 22))
        pygame.draw.arc(sprite, hair, (12, 0, 21, 17), math.pi, math.tau, 7)
        pygame.draw.line(sprite, hair, (14, 9), (19, 4), 4)
        pygame.draw.line(sprite, hair, (25, 4), (31, 9), 3)
        if entity.get("mood_is_bad", False):
            pygame.draw.line(sprite, (60, 30, 25), (17, 14), (21, 15), 1)
            pygame.draw.line(sprite, (60, 30, 25), (24, 15), (28, 14), 1)
        else:
            pygame.draw.circle(sprite, (35, 28, 25), (19, 14), 1)
            pygame.draw.circle(sprite, (35, 28, 25), (26, 14), 1)

        scaled = pygame.transform.scale(sprite, (sprite_w, sprite_h))
        # Recorte vertical por z-buffer para que las paredes oculten al NPC.
        for col in range(max(0, left), min(self.width, right)):
            ray_index = min(self.ray_count-1, max(0, int(col / ray_step)))
            if transform_y < zbuffer[ray_index] + 0.08:
                src_x = max(0, min(sprite_w-1, col-left))
                strip = scaled.subsurface((src_x, 0, 1, sprite_h))
                self.screen.blit(strip, (col, top))
                zbuffer[ray_index] = transform_y
        # Nombre solo a distancia corta para no saturar la escena.
        if transform_y < 5.5:
            label = self.font_label.render(entity["name"], True, (255, 245, 205))
            lx = max(4, min(self.width-label.get_width()-4, sx-label.get_width()//2))
            self.screen.blit(label, (lx, max(42, top-18)))
            if entity.get("speech_timer", 0) > 0 and transform_y < 4.0:
                bubble = self.font_bubble.render(entity.get("speech_text", "")[:42], True, (255, 245, 220))
                bx = max(4, min(self.width-bubble.get_width()-8, sx-bubble.get_width()//2))
                self.screen.blit(bubble, (bx, max(58, top-36)))

    def draw_first_person_body(self):
        """Brazos, manos, torso y piernas del empleado al mirar hacia abajo."""
        # Cuanto más se inclina la cámara hacia el piso, más cuerpo entra en cuadro.
        look_down = max(0.0, self.camera_pitch)
        if look_down < 0.06:
            return
        w, h = self.width, self.height
        shirt = self.player.get("shirt", (190, 105, 35))
        pants = self.player.get("pants", (35, 42, 52))
        skin = self.player.get("skin", (225, 180, 145))
        factor = min(1.0, look_down / 0.72)
        center = w // 2
        base_y = h + int(18 - factor * 38)

        def shade(color, amount):
            return tuple(max(0, min(255, c + amount)) for c in color)

        # Piernas y calzado: visibles al bajar la mirada.
        leg_top = base_y - int(105 + 45 * factor)
        leg_w = int(w * 0.105)
        pygame.draw.polygon(self.screen, shade(pants, -35), [
            (center-leg_w-18, leg_top), (center-10, leg_top+8),
            (center-22, base_y), (center-leg_w-42, base_y)])
        pygame.draw.polygon(self.screen, pants, [
            (center-leg_w-10, leg_top+4), (center-14, leg_top+12),
            (center-29, base_y), (center-leg_w-30, base_y)])
        pygame.draw.polygon(self.screen, shade(pants, -35), [
            (center+10, leg_top+8), (center+leg_w+18, leg_top),
            (center+leg_w+42, base_y), (center+22, base_y)])
        pygame.draw.polygon(self.screen, pants, [
            (center+14, leg_top+12), (center+leg_w+10, leg_top+4),
            (center+leg_w+30, base_y), (center+29, base_y)])
        shoe_y = h - 5
        pygame.draw.ellipse(self.screen, (22, 25, 29), (center-leg_w-42, shoe_y-17, 58, 24))
        pygame.draw.ellipse(self.screen, (22, 25, 29), (center+leg_w-15, shoe_y-17, 58, 24))

        # Torso con cuello y hombros, usando los colores de ropa del personaje elegido.
        torso_top = h - int(175 + 55 * factor)
        torso_w = int(w * (0.30 + 0.05 * factor))
        pygame.draw.polygon(self.screen, shade(shirt, -45), [
            (center-torso_w//2, torso_top+28), (center-torso_w//2+35, torso_top),
            (center+torso_w//2-35, torso_top), (center+torso_w//2, torso_top+28),
            (center+torso_w//2-18, h+10), (center-torso_w//2+18, h+10)])
        pygame.draw.polygon(self.screen, shirt, [
            (center-torso_w//2+12, torso_top+30), (center-torso_w//2+42, torso_top+8),
            (center+torso_w//2-42, torso_top+8), (center+torso_w//2-12, torso_top+30),
            (center+torso_w//2-30, h+4), (center-torso_w//2+30, h+4)])
        pygame.draw.line(self.screen, shade(shirt, 35), (center-10, torso_top+22),
                         (center-10, h-8), 3)

        # Brazos y manos adelante, como parte del cuerpo y no como un arma.
        arm_y = torso_top + 42
        arm_end_y = h - int(35 + 28 * factor)
        arm_spread = int(w * (0.22 + 0.025 * factor))
        sleeve = shade(shirt, -22)
        pygame.draw.polygon(self.screen, sleeve, [
            (center-torso_w//2+22, arm_y), (center-torso_w//2-8, arm_y+18),
            (center-arm_spread, arm_end_y-16), (center-arm_spread+30, arm_end_y),
            (center-20, arm_y+68)])
        pygame.draw.polygon(self.screen, sleeve, [
            (center+torso_w//2-22, arm_y), (center+torso_w//2+8, arm_y+18),
            (center+arm_spread, arm_end_y-16), (center+arm_spread-30, arm_end_y),
            (center+20, arm_y+68)])
        pygame.draw.polygon(self.screen, skin, [
            (center-arm_spread+2, arm_end_y-20), (center-arm_spread+31, arm_end_y-10),
            (center-arm_spread+42, arm_end_y+8), (center-arm_spread+16, arm_end_y+16)])
        pygame.draw.polygon(self.screen, skin, [
            (center+arm_spread-2, arm_end_y-20), (center+arm_spread-31, arm_end_y-10),
            (center+arm_spread-42, arm_end_y+8), (center+arm_spread-16, arm_end_y+16)])

    def draw_world(self):
        self.width, self.height = self.screen.get_size()
        self.screen.fill((17, 21, 26))

        if self.state == "start":
            card_w, card_h = 520, 330
            cx = (self.width-card_w)//2
            cy = (self.height-card_h)//2
            for band in range(0, self.height, 34):
                pygame.draw.line(self.screen, (22, 29, 37), (0, band), (self.width, band), 1)
            pygame.draw.rect(self.screen, (8, 12, 18), (cx-5, cy+5, card_w+10, card_h+10), border_radius=18)
            pygame.draw.rect(self.screen, (39, 49, 61), (cx, cy, card_w, card_h), border_radius=14)
            pygame.draw.rect(self.screen, (105, 120, 132), (cx, cy, card_w, card_h), 2, border_radius=14)
            pygame.draw.rect(self.screen, (250, 190, 45), (cx+18, cy+66, card_w-36, 3), border_radius=2)
            title = self.font_title.render("LA FÁBRICA", True, (251, 191, 36))
            self.screen.blit(title, (cx+(card_w-title.get_width())//2, cy+20))
            prompt = self.font_dialog.render("Elegí con las flechas izquierda / derecha:", True, (226, 232, 240))
            self.screen.blit(prompt, (cx+30, cy+82))
            self.btn_prev = pygame.Rect(cx+42, cy+132, 52, 54)
            self.btn_next_char = pygame.Rect(cx+card_w-94, cy+132, 52, 54)
            for rect, glyph in ((self.btn_prev, "<"), (self.btn_next_char, ">")):
                pygame.draw.rect(self.screen, (67, 83, 98), rect, border_radius=9)
                pygame.draw.rect(self.screen, (13, 16, 21), rect, 2, border_radius=9)
                g = self.font_title.render(glyph, True, (248, 250, 252))
                self.screen.blit(g, (rect.centerx-g.get_width()//2, rect.centery-g.get_height()//2-2))
            chosen = PLAYABLE_CHARACTERS[self.selected_character_index]
            name_s = self.font_title.render(chosen, True, (251, 191, 36))
            self.screen.blit(name_s, (cx+(card_w-name_s.get_width())//2, cy+138))
            role_map = {
                "Charly":"Operario", "Gonzalo":"Operario", "Francisco":"Operario", "Martín":"Operario",
                "Alan":"Operario", "John":"Operario", "Jonathan":"Operario", "Adrián":"Mantenimiento",
                "Fernando":"Supervisor", "Jessica":"Administración", "Ricardo":"Dueño", "Silvia":"Administración"
            }
            role_s = self.font_dialog.render(role_map.get(chosen, "Empleado"), True, (220, 228, 235))
            self.screen.blit(role_s, (cx+(card_w-role_s.get_width())//2, cy+192))
            self.btn_start = pygame.Rect(cx+(card_w-220)//2, cy+235, 220, 44)
            pygame.draw.rect(self.screen, (251, 191, 36), self.btn_start, border_radius=10)
            b = self.font_btn.render("COMENZAR JORNADA", True, (17, 21, 26))
            self.screen.blit(b, (self.btn_start.x+(self.btn_start.w-b.get_width())//2, self.btn_start.y+14))
            hint = self.font_label.render("WASD mover  |  Ratón mirar  |  E hablar  |  ESC liberar ratón", True, (190, 200, 210))
            self.screen.blit(hint, (cx+(card_w-hint.get_width())//2, cy+294))
            return

        # Escenario industrial en primera persona: techo, horizonte y piso con profundidad.
        horizon = int(self.height * 0.50 - self.camera_pitch * self.height * 0.43)
        horizon = max(int(self.height * 0.16), min(int(self.height * 0.84), horizon))
        self.camera_horizon = horizon
        self.screen.fill((57, 72, 83), (0, 0, self.width, horizon))
        self.screen.fill((65, 62, 54), (0, horizon, self.width, self.height-horizon))

        # Vigas y luminarias del techo: referencias visuales de un galpón fabril.
        for band in range(1, 5):
            yy = int(horizon * band / 5)
            pygame.draw.line(self.screen, (48, 61, 70), (0, yy), (self.width, yy), 2)
        for lamp_x in range(90, self.width, 270):
            pygame.draw.rect(self.screen, (112, 126, 128), (lamp_x, max(3, horizon//5), 74, 5))
            pygame.draw.line(self.screen, (153, 158, 143), (lamp_x+8, max(8, horizon//5+7)),
                             (lamp_x+66, max(8, horizon//5+7)), 2)

        # Juntas del piso en perspectiva; el espaciado aumenta hacia el jugador.
        floor_h = max(1, self.height-horizon)
        for n in range(1, 13):
            t = n / 12.0
            yy = horizon + int((t*t) * floor_h)
            pygame.draw.line(self.screen, (82, 77, 66), (0, yy), (self.width, yy), 1)
        for n in range(-8, 9):
            bottom_x = self.width//2 + n * max(24, self.width//13)
            pygame.draw.line(self.screen, (79, 74, 64), (self.width//2, horizon),
                             (bottom_x, self.height), 1)

        px = self.player["x"] / TILE_SIZE
        py = self.player["y"] / TILE_SIZE
        direction = self.player["dir_angle"]
        plane_len = math.tan(self.fov/2)
        plane_x = -math.sin(direction) * plane_len
        plane_y = math.cos(direction) * plane_len
        ray_step = self.width / self.ray_count
        zbuffer = [30.0] * self.ray_count
        wall_colors = {1: (105, 117, 126)}
        for i in range(self.ray_count):
            camera_x = 2 * (i + 0.5) / self.ray_count - 1
            ray_x = math.cos(direction) + plane_x * camera_x
            ray_y = math.sin(direction) + plane_y * camera_x
            ray_angle = math.atan2(ray_y, ray_x)
            distance, block, side = self.cast_wall(ray_angle)
            # Corrige distorsión de ojo de pez.
            corrected = max(0.08, distance * math.cos(ray_angle-direction))
            zbuffer[i] = corrected
            wall_h = min(self.height*2, int(self.height * 0.88 / corrected))
            top = horizon - wall_h//2
            base = wall_colors.get(block, (100, 110, 120))
            shade = 0.72 if side else 1.0
            shade *= max(0.38, 1.0 - corrected/19.0)
            color = tuple(max(0, min(255, int(v*shade))) for v in base)
            x = int(i*ray_step)
            w = max(1, int((i+1)*ray_step)-x+1)
            pygame.draw.rect(self.screen, color, (x, top, w, wall_h))
            # Líneas sutiles para dar textura industrial sin cargar el procesador.
            if wall_h > 28 and i % 5 == 0:
                pygame.draw.line(self.screen, tuple(min(255, c+18) for c in color), (x, top+8), (x+w-1, top+8), 1)

        # Mobiliario y maquinaria tridimensional, con oclusión respecto de paredes.
        for prop in sorted(self.world_props,
                           key=lambda item: math.hypot(item["x"]-self.player["x"], item["y"]-self.player["y"]),
                           reverse=True):
            self.draw_world_prop(prop, zbuffer, ray_step)

        # Personajes a escala de profundidad, de más lejano a más cercano.
        visible = []
        for npc in self.npcs:
            d = math.hypot(npc["x"]-self.player["x"], npc["y"]-self.player["y"])
            visible.append((d, npc))
        for _, npc in sorted(visible, reverse=True, key=lambda item: item[0]):
            self.draw_fps_sprite(npc, zbuffer, ray_step)

        # El cuerpo del jugador aparece en primer plano cuando mira hacia el piso.
        self.draw_first_person_body()

        # HUD fijo de primera persona.
        total_min = int(self.clock_minutes)
        time_text = f"{total_min//60:02d}:{total_min%60:02d}"
        zone = get_zone_at(self.player["x"], self.player["y"])
        hud_text = f"{self.player['name']}  |  {zone}  |  Día {self.day_number} • {time_text}"
        hud = self.font_hud.render(hud_text, True, (251, 191, 36))
        hud_box = pygame.Rect(12, 12, hud.get_width()+24, 34)
        pygame.draw.rect(self.screen, (24, 30, 38), hud_box, border_radius=8)
        pygame.draw.rect(self.screen, (13, 16, 21), hud_box, 2, border_radius=8)
        self.screen.blit(hud, (hud_box.x+12, hud_box.y+8))
        cross = self.width//2, self.height//2
        pygame.draw.line(self.screen, (235, 235, 220), (cross[0]-7, cross[1]), (cross[0]+7, cross[1]), 1)
        pygame.draw.line(self.screen, (235, 235, 220), (cross[0], cross[1]-7), (cross[0], cross[1]+7), 1)
        help_text = self.font_label.render("WASD mover  |  Ratón mirar  |  E hablar  |  ESC liberar/capturar ratón", True, (245, 245, 235))
        self.screen.blit(help_text, (12, self.height-24))

        if self.nearby_npc and self.state == "playing":
            prompt = self.font_btn.render(f"E  HABLAR CON {self.nearby_npc['name'].upper()}", True, (255, 245, 205))
            pygame.draw.rect(self.screen, (24, 35, 39), (self.width-prompt.get_width()-34, self.height-58, prompt.get_width()+22, 36), border_radius=8)
            self.screen.blit(prompt, (self.width-prompt.get_width()-23, self.height-49))

        if self.shift_ended:
            self.btn_next_day = pygame.Rect(self.width-146, 12, 134, 34)
            pygame.draw.rect(self.screen, (245, 158, 11), self.btn_next_day, border_radius=8)
            nd = self.font_btn.render("SIGUIENTE DÍA", True, (17, 21, 26))
            self.screen.blit(nd, (self.btn_next_day.x+(self.btn_next_day.w-nd.get_width())//2, self.btn_next_day.y+9))

        if self.state == "dialogue" and self.active_npc:
            if self.mouse_captured:
                pygame.event.set_grab(False)
                pygame.mouse.set_visible(True)
                self.mouse_captured = False
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((8, 11, 15, 190))
            self.screen.blit(overlay, (0, 0))
            box_w, box_h = min(720, self.width-40), min(440, self.height-60)
            bx, by = (self.width-box_w)//2, (self.height-box_h)//2
            pygame.draw.rect(self.screen, (30, 37, 48), (bx, by, box_w, box_h), border_radius=14)
            pygame.draw.rect(self.screen, (13, 16, 21), (bx, by, box_w, box_h), 3, border_radius=14)
            hdr = self.font_hud.render(f"{self.active_npc['name']} — {self.active_npc['role']}", True, (251, 191, 36))
            self.screen.blit(hdr, (bx+18, by+16))
            resp = self.font_dialog.render(self.dialogue_response[:95], True, (248, 250, 252))
            self.screen.blit(resp, (bx+18, by+52))
            self.question_rects = []
            qy = by+102
            for idx, q in enumerate(self.visible_questions):
                rect = pygame.Rect(bx+18, qy, box_w-36, 36)
                self.question_rects.append(rect)
                pygame.draw.rect(self.screen, (51, 65, 85), rect, border_radius=8)
                pygame.draw.rect(self.screen, (13, 16, 21), rect, 2, border_radius=8)
                label = self.font_btn.render(f"[{idx+1}] {q['label']}", True, (248, 250, 252))
                self.screen.blit(label, (rect.x+10, rect.y+9))
                qy += 44

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEMOTION and self.state == "playing" and self.mouse_captured:
                self.player["dir_angle"] += event.rel[0] * self.mouse_sensitivity
                # Mirada vertical: permite mirar el piso y ver el cuerpo del empleado.
                self.camera_pitch = max(-0.72, min(0.88,
                    self.camera_pitch + event.rel[1] * self.mouse_sensitivity * 1.8))

            if event.type == pygame.KEYDOWN:
                if self.state == "start":
                    if event.key == pygame.K_RETURN:
                        self.start_new_game()
                    elif event.key in (pygame.K_LEFT, pygame.K_UP):
                        self.selected_character_index = (self.selected_character_index-1) % len(PLAYABLE_CHARACTERS)
                    elif event.key in (pygame.K_RIGHT, pygame.K_DOWN):
                        self.selected_character_index = (self.selected_character_index+1) % len(PLAYABLE_CHARACTERS)
                elif self.state == "playing":
                    if event.key == pygame.K_ESCAPE:
                        self.mouse_captured = not self.mouse_captured
                        pygame.event.set_grab(self.mouse_captured)
                        pygame.mouse.set_visible(not self.mouse_captured)
                        pygame.mouse.get_rel()
                    elif event.key == pygame.K_e and self.nearby_npc:
                        self.open_dialogue(self.nearby_npc)
                    elif event.key == pygame.K_f and self.nearby_npc and self.nearby_npc["mood_is_bad"]:
                        self.player_fight_timer = 3.2
                        self.nearby_npc["ai_state"] = "fighting"
                        self.nearby_npc["ai_timer"] = 3.2
                        self.nearby_npc["speech_text"] = f"¡PELEA! {pick_random(NPC_FIGHT_LINES)}"
                        self.nearby_npc["speech_timer"] = 3.2
                elif self.state == "dialogue":
                    if event.key == pygame.K_ESCAPE:
                        self.state = "playing"
                        self.active_npc = None
                        pygame.event.set_grab(True)
                        pygame.mouse.set_visible(False)
                        pygame.mouse.get_rel()
                        self.mouse_captured = True
                    elif pygame.K_1 <= event.key <= pygame.K_9:
                        self.select_question(event.key - pygame.K_1)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if self.state == "start":
                    if self.btn_start.collidepoint(pos):
                        self.start_new_game()
                    elif self.btn_prev.collidepoint(pos):
                        self.selected_character_index = (self.selected_character_index-1) % len(PLAYABLE_CHARACTERS)
                    elif self.btn_next_char.collidepoint(pos):
                        self.selected_character_index = (self.selected_character_index+1) % len(PLAYABLE_CHARACTERS)
                elif self.state == "playing":
                    if self.shift_ended and self.btn_next_day.collidepoint(pos):
                        self.advance_to_next_day()
                    elif self.nearby_npc and self.btn_talk.collidepoint(pos):
                        self.open_dialogue(self.nearby_npc)
                    elif self.nearby_npc and self.nearby_npc["mood_is_bad"] and self.btn_fight.collidepoint(pos):
                        self.player_fight_timer = 3.2
                        self.nearby_npc["ai_state"] = "fighting"
                        self.nearby_npc["ai_timer"] = 3.2
                        self.nearby_npc["speech_text"] = f"¡PELEA! {pick_random(NPC_FIGHT_LINES)}"
                        self.nearby_npc["speech_timer"] = 3.2
                elif self.state == "dialogue":
                    for idx, r in enumerate(self.question_rects):
                        if r.collidepoint(pos):
                            self.select_question(idx)
                            break
        return True

    def run(self):
        running = True
        while running:
            dt = min(self.clock.tick(30) / 1000.0, 0.05)
            running = self.handle_events()
            self.update(dt)
            self.draw_world()
            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    FactoryPygame().run()