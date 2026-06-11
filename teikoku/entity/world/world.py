from functools import cached_property
import logging
import os

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

from repository.mongo.base import MongoBase
from teikoku.data.world import (
    DEFAULT_WORLD_CHAT_ID,
    LEGEND_BG_COLOR,
    LEGEND_RECT_OUTLINE,
    LEGEND_TEXT_COLOR,
    LEGEND_WORLD_FONT_PATH,
    MIN_MAP_SIZE,
    LEGEND_TEXT_SIZE,
    LEGEND_TITLE_COLOR,
    LEGEND_TITLE_SIZE,
)
from teikoku.entity.unit.unit_base import UnitBase
from teikoku.entity.world.city import City
from teikoku.entity.world.coor import Coordinate
from teikoku.entity.world.terrain_map import TerrainMap
from teikoku.enum.terrain import (
    TerrainColorEnum,
    TerrainTextEnum,
)

logger = logging.getLogger(__name__)


@dataclass
class World(MongoBase):
    name: str
    chat_id: int = DEFAULT_WORLD_CHAT_ID
    cities: Dict[Tuple[int, int], City] = field(default_factory=dict)
    units: Dict[Tuple[int, int], UnitBase] = field(default_factory=dict)

    UPDATABLE_ATTR_LIST = ()

    def __eq__(self, value):
        result = False
        if isinstance(value, World):
            result = self.chat_id == value.chat_id
        elif isinstance(value, str) and value.isnumeric():
            result = self.chat_id == int(value)
        elif isinstance(value, int):
            result = self.chat_id == value

        return result

    # RENDER =================================================================
    def render_base_map(self, terrain_map: TerrainMap = None) -> Image.Image:
        if terrain_map is None:
            terrain_map = TerrainMap()
            terrain_map.generate_terrain_map()
        if not terrain_map:
            terrain_map.generate_terrain_map()

        # 1. Gera os dados de pixels do mapa original
        pixel_data = []
        for terrain_value in terrain_map.flatten:
            color = terrain_map.value_to_color(terrain_value=terrain_value)
            pixel_data.append(color)

        # 2. Cria imagem do mapa base
        size_x, size_y = (terrain_map.size_x, terrain_map.size_y)
        map_img = Image.new("RGB", (size_x, size_y))
        map_img.putdata(pixel_data)
        if MIN_MAP_SIZE[0] > size_x and MIN_MAP_SIZE[1] > size_y:
            map_img = map_img.resize(MIN_MAP_SIZE, Image.Resampling.NEAREST)

        return map_img

    def render_map_coordinates(
        self,
        map_img: Image.Image,
        terrain_map: TerrainMap,
    ) -> Image.Image:
        """
        Adiciona na imagem as coordenadas:
        - centro
        - topo-centro
        - baixo-centro
        - esquerda-centro
        - direita-centro
        - quatro cantos
        """

        img = map_img.copy()
        draw = ImageDraw.Draw(img)
        font = self.font
        size_x, size_y = map_img.size
        cx = terrain_map.central_coor.x
        cy = terrain_map.central_coor.y

        half_w = size_x // 2
        half_h = size_y // 2

        points = {
            "NO": (0, 0),
            "N": (half_w, 0),
            "NE": (size_x - 1, 0),
            "O": (0, half_h),
            "C": (half_w, half_h),
            "L": (size_x - 1, half_h),
            "SO": (0, size_y - 1),
            "S": (half_w, size_y - 1),
            "SE": (size_x - 1, size_y - 1),
        }

        for label, (px, py) in points.items():

            # Converte posição local do mapa para coordenada global
            world_x = cx + (px - half_w)
            world_y = cy + (py - half_h)

            text = f"{label}: ({world_x}, {world_y})"

            bbox = draw.textbbox((0, 0), text, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]

            # Mantém o texto dentro da imagem
            tx = min(max(px + 4, 0), img.width - text_w)
            ty = min(max(py + 4, 0), img.height - text_h)

            # Fundo para melhorar legibilidade
            draw.rectangle(
                (
                    tx - 2,
                    ty - 2,
                    tx + text_w + 2,
                    ty + text_h + 2,
                ),
                fill=(0, 0, 0),
            )

            draw.text(
                (tx, ty),
                text,
                fill=(255, 255, 255),
                font=font,
            )

        return img

    def render_map_legend(self, map_img: Image.Image) -> Image.Image:
        size_x, size_y = map_img.size
        font = self.font
        title_font = self.title_font

        # =========================
        # Configurações visuais
        # =========================
        padding_x = 20
        padding_y = 30
        spacing_y = 12
        box_size = 14
        text_gap = 10

        # =========================
        # Calcula maior largura de texto
        # =========================
        dummy_img = Image.new("RGB", (1, 1))
        dummy_draw = ImageDraw.Draw(dummy_img)

        title = "LEGENDA"

        legend_items = []
        max_text_width = 0

        for terrain_color_enum in TerrainColorEnum:
            enum_name = terrain_color_enum.name
            text = TerrainTextEnum[enum_name].value

            bbox = dummy_draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]

            max_text_width = max(max_text_width, text_width)

            legend_items.append(
                {
                    "color": terrain_color_enum.value,
                    "text": text,
                }
            )

        # Largura do título
        title_bbox = dummy_draw.textbbox((0, 0), title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]

        max_content_width = max(max_text_width, title_width)

        # =========================
        # Define largura dinâmica da legenda
        # =========================
        legend_width = padding_x * 2 + box_size + text_gap + max_content_width

        final_width = size_x + legend_width

        # =========================
        # Cria imagem final
        # =========================
        final_img = Image.new("RGB", (final_width, size_y), LEGEND_BG_COLOR)
        final_img.paste(map_img, (0, 0))

        draw = ImageDraw.Draw(final_img)

        start_x = size_x + padding_x
        current_y = padding_y

        # =========================
        # Título
        # =========================
        draw.text(
            (start_x, current_y),
            text=title,
            fill=LEGEND_TITLE_COLOR,
            font=title_font,
        )

        title_height = title_bbox[3] - title_bbox[1]
        current_y += title_height + 20

        # =========================
        # Itens da legenda
        # =========================
        for item in legend_items:
            color = item["color"]
            text = item["text"]

            # Mede texto
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_height = text_bbox[3] - text_bbox[1]

            # Altura da linha baseada no maior elemento
            line_height = max(box_size, text_height)

            # Centraliza verticalmente o quadrado
            box_y = current_y + (line_height - box_size) // 2

            # Centraliza verticalmente o texto
            text_y = (
                current_y + (line_height - text_height) // 2 - text_bbox[1]
            )

            # Quadrado colorido
            draw.rectangle(
                [
                    (start_x, box_y),
                    (start_x + box_size, box_y + box_size),
                ],
                fill=color,
                outline=LEGEND_RECT_OUTLINE,
                width=1,
            )

            # Texto
            text_x = start_x + box_size + text_gap

            draw.text(
                (text_x, text_y),
                text,
                fill=LEGEND_TEXT_COLOR,
                font=font,
            )

            # Próxima linha
            current_y += line_height + spacing_y

        return final_img

    def render_full_map(self, terrain_map: TerrainMap = None) -> Image.Image:
        if terrain_map is None:
            terrain_map = TerrainMap()
            terrain_map.generate_terrain_map()
        if not terrain_map:
            terrain_map.generate_terrain_map()

        map_img = self.render_base_map(terrain_map=terrain_map)
        map_img = self.render_map_coordinates(map_img, terrain_map)
        map_img = self.render_map_legend(map_img)

        return map_img

    @cached_property
    def font(self) -> ImageFont:
        if os.path.exists(LEGEND_WORLD_FONT_PATH):
            font = ImageFont.truetype(LEGEND_WORLD_FONT_PATH, LEGEND_TEXT_SIZE)
        else:
            font = ImageFont.load_default()

        return font

    @cached_property
    def title_font(self) -> ImageFont:
        if os.path.exists(LEGEND_WORLD_FONT_PATH):
            title_font = ImageFont.truetype(
                LEGEND_WORLD_FONT_PATH, LEGEND_TITLE_SIZE
            )
        else:
            title_font = ImageFont.load_default()

        return title_font

    # CITIES =================================================================
    def add_city(self, city: City):
        if not isinstance(city, City):
            raise TypeError(f"city precisa ser do tipo City ({type(city)}).")

        x = city.coor.x
        y = city.coor.y
        coor = (x, y)
        existing_city = self.cities.get(coor)

        if existing_city is None:
            self.cities[coor] = city
            logger.info(f"Cidade {city.name} adicionada ao Mundo {self.name}.")
        else:
            logger.warning(
                f"Cidade {city.name} NÃO foi adicionada ao Mundo {self.name}, "
                f"por já existir a cidade {existing_city.name} na posição "
                f"{city.coor.show}."
            )

    def get_city(
        self,
        coordinate: Optional[Coordinate],
        x: Optional[int],
        y: Optional[int],
    ) -> Optional[City]:
        if isinstance(coordinate, Coordinate):
            x = coordinate.x
            y = coordinate.y

        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError(
                "Os parâmetros x e y precisam ser do tipo int."
                f"x: {type(x)} | y: {type(y)}"
            )

        coor = (x, y)

        return self.cities.get(coor, None)

    @property
    def total_cities(self) -> int:
        return len(self.cities)

    @property
    def telegram_text(self):
        text = f"*Mundo*: {self.name}\n"
        text += f"*Total de Cidades*: {self.total_cities}\n"

        return text


if __name__ == "__main__":
    from teikoku.entity.register.player import Player

    print(" START LOCAL TEST ".center(79, "="))
    p = Player(user_id=123, name="teste")
    c = City(name="Cidade Teste", x=1, y=2, owner=p)
    cities = {(c.coor.x, c.coor.y): c}
    world = World(name="Mundo Teste", cities=cities)

    print("\nWORLD")
    print(world)

    print("\nWORLD.TELEGRAM_TEXT")
    print(world.telegram_text)

    print("\nWORLD.TO_DICT")
    print(world.to_dict())

    print("\nWORLD.RENDER_BASE_MAP")
    img = world.render_base_map()
    img.show()

    print(" END LOCAL TEST ".center(79, "="))
