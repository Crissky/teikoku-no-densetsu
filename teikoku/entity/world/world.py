import logging
import os

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

from repository.mongo.base import MongoBase
from teikoku.data.world import (
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
    cities: Dict[Tuple[int, int], City] = field(default_factory=dict)
    units: Dict[Tuple[int, int], UnitBase] = field(default_factory=dict)

    UPDATABLE_ATTR_LIST = ()

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

    def render_map_legend(self, map_img: Image.Image) -> Image.Image:
        size_x, size_y = map_img.size

        # =========================
        # Fontes
        # =========================
        if os.path.exists(LEGEND_WORLD_FONT_PATH):
            font = ImageFont.truetype(LEGEND_WORLD_FONT_PATH, LEGEND_TEXT_SIZE)
            title_font = ImageFont.truetype(
                LEGEND_WORLD_FONT_PATH, LEGEND_TITLE_SIZE
            )
        else:
            font = ImageFont.load_default()
            title_font = font

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
        map_img = self.render_base_map(terrain_map)
        map_img = self.render_map_legend(map_img)

        return map_img

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
