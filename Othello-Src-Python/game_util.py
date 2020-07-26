#!/usr/bin/env python3

import board as board
import coord as coord


def is_end(_board: board.Board) -> bool:
    """ Check Whether the board is in terminated state or not """
    # Traverse Board
    for r in range(board.BOARD_H):
        for c in range(board.BOARD_W):
            # Only Need to Check the Celss thar are unoccupied
            if _board.get(r, c) == board.Status.UNOCCUPIED:
                # There exists at least one vaid step for one of the color
                if(is_valid_step(_board, True, coord.Coord(r, c)) or
                   is_valid_step(_board, False, coord.Coord(r, c))):
                    # The Gaem is not over yet
                    return False

    # We can't find valid step
    return True


def is_valid_step(_board: board.Board, _is_black: bool, _step: coord.Coord) -> bool:
    # Abort
    if _step == coord.NO_ACTION:
        return False

    # You can't set piece on not UNOCCUPIED
    if _board.get(_step.x, _step.y) != board.Status.UNOCCUPIED:
        return False

    # Inside Safe Area (Central 6x6), No need to Check
    if (_step.x >= 1 and _step.x <= board.BOARD_H-2 and
            _step.y >= 1 and _step.y <= board.BOARD_W-2):
        return True

    """ 
        [B]    [W]     [...][B]
        [start][middle][...][end]
    """
    middle_color = board.Status.WHITE if (_is_black) else board.Status.BLACK
    end_color = board.Status.BLACK if (_is_black) else board.Status.WHITE

    # Eight Dierection
    for dir in coord.direction:
        # Reset
        cur_r = _step.x
        cur_c = _step.y
        state = 0

        # Check
        while(_board.check_boundary(cur_r, cur_c)):
            # Step Out
            cur_r += dir.x
            cur_c += dir.y

            if(state == 0 and _board.get(cur_r, cur_c) == middle_color):
                # [B][W]
                state = 1
            elif(state == 1 and _board.get(cur_r, cur_c) == middle_color):
                # [B][W][...]
                state = 1
            elif(state == 1 and _board.get(cur_r, cur_c) == end_color):
                # [B][W][...][B]
                return True
            else:
                # Other Fail Situation
                break

    # Fail
    return False
