from dataclasses import dataclass

from app.services.board_service import GenerationService
from app.valueObjects.luminary import Luminary
from app.valueObjects.sectors import Sectors


@dataclass
class ViewSector:
    visible_sky: bool
    index: int
    moon: bool
    planet: bool
    planet_x: bool
    asteroid: bool
    nebula: bool
    empty_space: bool
    can_have_moon: bool

    @staticmethod
    def create_from(sectors: Sectors, index: int, timer: int) -> 'ViewSector':
        visible_start = timer % Sectors.SIZE
        visible_indices = {visible % Sectors.SIZE for visible in
                           range(visible_start, visible_start + (Sectors.SIZE // 2))}

        return ViewSector(
            visible_sky=index in visible_indices,
            index=index,
            moon=Luminary.MOON in sectors[index],
            planet=Luminary.PLANET in sectors[index],
            planet_x=Luminary.PLANET_X in sectors[index],
            asteroid=Luminary.ASTEROID in sectors[index],
            nebula=Luminary.NEBULA in sectors[index],
            empty_space=Luminary.EMPTY_SPACE in sectors[index],
            can_have_moon=index in GenerationService.POSSIBLE_MOON_SECTORS
        )


@dataclass
class ViewBoard:
    left_board: [ViewSector]
    right_board: [ViewSector]
    visible_degree: int
    icons: [str]
    timer: int

    @staticmethod
    def create_from(board: Sectors, timer: int) -> 'ViewBoard':
        visible_degree = ViewBoard.get_visible_degree(timer)
        left_board = [ViewSector.create_from(board, index, timer) for index in range(0, Sectors.SIZE // 2)]
        right_board = [ViewSector.create_from(board, index, timer) for index in range(Sectors.SIZE // 2, Sectors.SIZE)]
        return ViewBoard(left_board, right_board, visible_degree, [luminary.name for luminary in Luminary], timer)

    @staticmethod
    def get_visible_degree(timer: int) -> int:
        degrees = {
            0: 90,
            1: 40,
            2: 20,
            3: 0,
            4: 340,
            5: 320,
            6: 270,
            7: 220,
            8: 200,
            9: 180,
            10: 160,
            11: 150
        }

        return degrees[timer % Sectors.SIZE]
