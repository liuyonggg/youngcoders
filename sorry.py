"""
1. cards:  
   The modern deck contains 45 cards: there are five 1 cards as well as four each of the other cards (Sorry!, 2, 3, 4, 5, 7, 8, 10, 11 and 12). There are no 6s or 9s, to avoid confusion.
    1   Move a pawn from Start or move a pawn one space forward.
    2   Move a pawn from Start or move a pawn two spaces forward. Drawing a two entitles the player to draw again at the end of his or her turn. If the player cannot use a two to move, he or she can still draw again.
    3   Move a pawn three spaces forward.
    4   Move a pawn four spaces backward.
    5   Move a pawn five spaces forward.
    7   Move one pawn seven spaces forward, or split the seven spaces between two pawns (such as four spaces for one pawn and three for another). This makes it possible for two pawns to enter Home on the same turn, for example. The seven cannot be used to move a pawn out of Start, even if the player splits it into a six and one or a five and two. The entire seven spaces must be used or the turn is lost. You may not move backwards with a split.
    8   Move a pawn eight spaces forward.
    10  Move a pawn 10 spaces forward or one space backward. If none of a player's pawns can move forward 10 spaces, then one pawn must move back one space.
    11  Move 11 spaces forward, or switch the places of one of the player's own pawns and an opponent's pawn. A player that cannot move 11 spaces is not forced to switch and instead can forfeit the turn. An 11 cannot be used to switch a pawn that is in a Safety Zone.
    12  Move a pawn 12 spaces forward.
2. rules:
    1. Each player chooses four pawns of one color and places them in his or her Start. One player is selected to play first.

    2. Each player in turn draws one card from the deck and follows its instructions. To begin the game, all of a player's four pawns are restricted to Start; a player can only move them out onto the rest of the board if he or she draws a 1 or 2 card. A 1 or a 2 places a pawn on the space directly outside of start (a 2 does not entitle the pawn to move a second space).

    3. A pawn can jump over any other pawn during its move. However, two pawns cannot occupy the same square; a pawn that lands on a square occupied by another player's pawn "bumps" that pawn back to its own Start. Players can not bump their own pawns back to Start; if the only way to complete a move would result in a player bumping his or her own pawn, the player's pawns remain in place and the player loses his or her turn.

    4. If a pawn lands at the start of a slide (except those of its own color), either by direct movement or as the result of a switch from an 11 card or a Sorry card, it immediately "slides" to the last square of the slide. All pawns on all spaces of the slide (including those belonging to the sliding player) are sent back to their respective Starts.[4]

    5. The last five squares before each player's Home are "Safety Zones", and are specially colored corresponding to the colors of the Homes they lead to. Access is limited to pawns of the same color. Pawns inside the Safety Zones are immune to being bumped by opponent's pawns or being switched with opponents' pawns via 11 or Sorry! cards. However, if a pawn is forced via a 10 or 4 card to move backwards out of the Safety Zone, it is no longer considered "safe" and may be bumped by or switched with opponents' pawns as usual until it re-enters the Safety Zone.
    6. Sorry! card Take any one pawn from Start and move it directly to a square occupied by any opponent's pawn, sending that pawn back to its own Start. A Sorry! card cannot be used on an opponent's pawn in a Safety Zone. If there are no pawns on the player's Start, or no opponent's pawns on any squares outside Safety Zones, the turn is lost.
3. board:
   1. 4 lines: 15 * 4 = 60 spaces
   2. 4 safety zones, not in the 4 lines, enter point is first space in the corresponding line,  each zone takes 6 spaces
   3. start point is not in the four lines, exit point is 4th space in the corresponding line
   4. slide point: the first space to the 4th space, the 9th space to 13th space
"""

class parameter(object):
    colors = ["YELLOW", "GREEN", "RED", "BLUE"]
    num_space = 60
    enterpoint_safety_zone = 1
    enterpoint_space = 3
    slide_1_space_begin = 1
    slide_1_space_end = 4
    slide_2_space_begin = 9
    slide_2_space_end = 13
    depth_safetyzone = 6
    start_position = -1

    def __setattr__(self, *_):
        assert (False)

class pawn(object):
    " pawn: move on the board, each pawn has color/position/player information" 
    def __init__(self, color, player, position):
        self._color = color
        self._player = player
        self._position = position

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position= value

    @property
    def color(self):
        return self._color

    @property
    def player(self):
        return self._player

    def in_start(self):
        return self._position == parameter().start_position

class safetyzone(object):
    """ safetyzone: the place where the pawn won't be influence by opponents' pawn
       not in the 4 lines, enter point is first space in the corresponding line,  each zone takes 6 spaces
    """
    def __init__(self, color, enterpoint, prefix_position):
        self._color = color
        self._enterpoint = enterpoint
        self._depth = 6
        self._prefix = prefix_position

    def position(self, pos, spaces):
        assert (self.entering_safetyzone(pos) or self.in_safetyzone(pos))
        if (pos <= enterpoint) and (pos + spaces >= enterpoint):
            pos += self._prefix
        new_pos = pos + spaces
        if (new_pos > self._prefix + self._depth):
            new_pos = self._prefix + self._depth - (new_pos - self._depth)
            if new_pos <= 0:
                new_pos = self._enterpoint - new_pos
            else:
                new_pos += self.prefix_position
        elif (new_pos <= self._prefix + self._enterpoint):
            new_pos -= self._prefix
        return new_pos

    def in_safetyzone(self, pos):
        return (pos > prefix_position)

    def entering_safetyzone(self, pos):
        return (pos == self._enterpoint)

    def should_enter_safetyzone(self, pos):
        return (pos >= self._enterpoint)

    def in_home(self, pos):
        return (pos == prefix_position + self._enterpoint + self._depth)
        
class board(object):
    """ board: the place where the pawn put on
        1. 4 lines: 15 * 4 = 60 spaces
        2. 4 safety zones, not in the 4 lines, enter point is first space in the corresponding line,  each zone takes 6 spaces
        3. start point is not in the four lines, exit point is 4th space in the corresponding line
        4. slide point: the first space to the 4th space, the 9th space to 13th space
    """
    def __init__(self):
        colors = parameter().colors()
        self._safetyzones = [safetyzone(c, colors[i], parameter().enterpoint_safety_zone + i * 15, parameter.num_space+100) for i in range(len(colors))]
        self._slides = {}
        for i in range(len(colors)):
            self._slides[i*15+1]  = i*15+4
            self._slides[i*15+9]  = i*15+13

    def position(self, pawn, spaces):
        new_pos = pawn.position + spaces
        sz = self._safetyzones[parameter.colors.index[pawn.color]]
        if sz.should_enter_safetyzone(new_pos):
            new_pos = sz.position(pawn.position, spaces)
        return new_pos

    def slide(self, pos):
        new_pos = pos
        if pos in self._slides:
            new_pos = self._slides[pos]
        return new_pos

    def in_home(self, pawn):
        ci = parameter().colors().index(pawn.color)
        return self._safetyzones[ci].in_home(pawn.position())

    def in_safetyzone(self, pawn):
        ci = parameter().colors().index(pawn.color)
        return self._safetyzones[ci].in_safetyzone(pawn.position())

    def dist_home(self, pawn):
        #FIXME: the caculation is wrong!
        "distance to home"
        ci = parameter().colors().index(pawn.color)
        res = 0
        if (self._safetyzones[ci].should_enter_safetyzone(pawn.position)):
            res = self._safetyzones[ci]._enterpoint + parameter().depth_safetyzone - pawn.pos - self._safetyzones[ci]._prefix
        else:
            res = self._safetyzones[ci]._enterpoint + parameter().depth_safetyzone - pawn.pos
        return res

    def distance(self, pawn1, pawn2):
        assert (not self.in_safetyzone(pawn1))
        assert (not self.in_safetyzone(pawn2))
        dis = pawn1.position - pawn2.position
        if dis < 0:
            dis += parameter().num_space
        assert (dis >= 0)
        return dis

class player(object):
    """each player has a name, color, 4 pawns and a strategy"""
    def __init__(self, name, color, strategy):
        self._name = name
        self._color = color
        self._pawns = [pawn(color, self, parameter.start_position) for i in range(4)]
        self._strategy = strategy

    def is_win(self):
        reduce(lambda x, y: x.in_home() and y.in_home(), self._pawns)

    def move(self, card):
        self.strategy.apply(self, card)

    @property
    def name(self):
        return self._name

    @property
    def color(self):
        return self._color

    @property
    def pawns(self):
        return self._pawns

    @property
    def strategy(self):
        return self._strategy

class card(object):
    """
   The modern deck contains 45 cards: there are five 1 cards as well as four each of the other cards (Sorry!, 2, 3, 4, 5, 7, 8, 10, 11 and 12). There are no 6s or 9s, to avoid confusion.
    1   Move a pawn from Start or move a pawn one space forward.(unary)
    2   Move a pawn from Start or move a pawn two spaces forward. Drawing a two entitles the player to draw again at the end of his or her turn. If the player cannot use a two to move, he or she can still draw again. (unary)
    3   Move a pawn three spaces forward. (unary)
    4   Move a pawn four spaces backward. (unary)
    5   Move a pawn five spaces forward. (unary)
    7   Move one pawn seven spaces forward, or split the seven spaces between two pawns (such as four spaces for one pawn and three for another). This makes it possible for two pawns to enter Home on the same turn, for example. The seven cannot be used to move a pawn out of Start, even if the player splits it into a six and one or a five and two. The entire seven spaces must be used or the turn is lost. You may not move backwards with a split. (binary)
    8   Move a pawn eight spaces forward. (unary)
    10  Move a pawn 10 spaces forward or one space backward. If none of a player's pawns can move forward 10 spaces, then one pawn must move back one space. (unary)
    11  Move 11 spaces forward, or switch the places of one of the player's own pawns and an opponent's pawn. A player that cannot move 11 spaces is not forced to switch and instead can forfeit the turn. An 11 cannot be used to switch a pawn that is in a Safety Zone. (unary/binary)
    12  Move a pawn 12 spaces forward. (unary)
    13(Sorry!) card Take any one pawn from Start and move it directly to a square occupied by any opponent's pawn, sending that pawn back to its own Start. A Sorry! card cannot be used on an opponent's pawn in a Safety Zone. If there are no pawns on the player's Start, or no opponent's pawns on any squares outside Safety Zones, the turn is lost. (binary)
    """
    def __init__(self):
        pass

    def apply(self, pawn1, pawn2, mode, board):
        assert (False)

    def getmodes(self):
        assert (False)

class cardcommon(card):
    def apply(self, pawn1, pawn2, mode, board, spaces):
        pawn1.position = board.position(pawn1, spaces)
        pawn1.position = board.position(pawn1, spaces)

    
class card1(cardcommon):
    " card 1: Move a pawn from Start or move a pawn one space forward.(unary) "
    CARD_MODE = ["START", "FORWARD"]
    def apply(self, pawn1, pawn2, mode, board):
        if mode == CARD_MODE[1]:
            super(self, cardcommon).apply(pawn1, pawn2, mode, board, 1)
        else:
            assert(mode == CARD_MODE[0])
            pawn1.position = parameter().colors.index(pawn1.color)*15 + parameter().enterpoint_space

    def getmodes(self):
        return card1.CARD_MODE


class card2(cardcommon):
    "card 2: Move a pawn from Start or move a pawn two spaces forward. Drawing a two entitles the player to draw again at the end of his or her turn. If the player cannot use a two to move, he or she can still draw again. (unary)"
    CARD_MODE = ["START", "FORWARD"]
    def apply(self, pawn1, pawn2, mode, board):
        if mode == CARD_MODE[1]:
            super(self, cardcommon).apply(pawn1, pawn2, mode, board, 2)
        else:
            pawn1.position = parameter().colors.index(pawn1.color)*15 + parameter().enterpoint_space

class card3(cardcommon):
    "card 3: Move a pawn three spaces forward. (unary)"
    def apply(self, pawn1, pawn2, mode, board):
        super(self, cardcommon).apply(pawn1, pawn2, mode, board, 3)

class card4(cardcommon):
    "card 4: Move a pawn four spaces backward. (unary)"
    def apply(self, pawn1, pawn2, mode, board):
        super(self, cardcommon).apply(pawn1, pawn2, mode, board, -4)
        
class card5(cardcommon):
    "card 5: Move a pawn five spaces forward. (unary)"
    def apply(self, pawn1, pawn2, mode, board):
        super(self, cardcommon).apply(pawn1, pawn2, mode, board, 5)

class card7(cardcommon):
    "card 7: Move one pawn seven spaces forward, or split the seven spaces between two pawns (such as four spaces for one pawn and three for another). This makes it possible for two pawns to enter Home on the same turn, for example. The seven cannot be used to move a pawn out of Start, even if the player splits it into a six and one or a five and two. The entire seven spaces must be used or the turn is lost. You may not move backwards with a split. (binary)"
    def apply(self, pawn1, pawn2, mode, board):
        super(self, cardcommon).apply(pawn1, pawn2, mode, board, 7)

class card8(cardcommon):
    "card 8: Move a pawn eight spaces forward. (unary)"
    def apply(self, pawn1, pawn2, mode, board):
        super(self, cardcommon).apply(pawn1, pawn2, mode, board, 8)

class card10(cardcommon):
    "card 10: Move a pawn 10 spaces forward or one space backward. If none of a player's pawns can move forward 10 spaces, then one pawn must move back one space. (unary)"
    CARD_MODE = ["BACKWARD", "FORWARD"]
    def apply(self, pawn1, pawn2, mode, board):
        if mode == CARD_MODE[1]:
            super(self, cardcommon).apply(pawn1, pawn2, mode, board, 10)
        else:
            assert(mode == CARD_MODE[0])
            super(self, cardcommon).apply(pawn1, pawn2, mode, board, -1)

class card11(cardcommon):
    "card 11: Move 11 spaces forward, or switch the places of one of the player's own pawns and an opponent's pawn. A player that cannot move 11 spaces is not forced to switch and instead can forfeit the turn. An 11 cannot be used to switch a pawn that is in a Safety Zone. (unary/binary)"
    CARD_MODE = ["FORWARD", "EXCHANGE"]
    def apply(self, pawn1, pawn2, mode, board):
        if mode == CARD_MODE[0]:
            super(self, cardcommon).apply(pawn1, pawn2, mode, board, 11)
        else:
            assert(mode == CARD_MODE[1])
            p = pawn1.position
            pawn1.position = pawn2.position
            pawn2.position = p

class card12(cardcommon):
    "card 12: Move a pawn 12 spaces forward. (unary)"
    def apply(self, pawn1, pawn2, mode, board):
        super(self, cardcommon).apple(pawn1, pawn2, mode, board, 12)

class cardsorry(cardcommon):
    "card sorry: Take any one pawn from Start and move it directly to a square occupied by any opponent's pawn, sending that pawn back to its own Start. A Sorry! card cannot be used on an opponent's pawn in a Safety Zone. If there are no pawns on the player's Start, or no opponent's pawns on any squares outside Safety Zones, the turn is lost. (binary)"
    def apply(self, pawn1, pawn2, mode, board):
        pawn1.positon = pawn2
        pawn2.positon = -1


class strategy(object):
    def __init__(self, player, game):
        self._player = player
        self._game = game
        self.cardstretegies = {type(card1()):self.card1_strategy, 
                               type(card2()):self.card2_strategy, 
                               type(card3()):self.card3_strategy, 
                               type(card4()):self.card4_strategy, 
                               type(card5()):self.card5_strategy, 
                               type(card7()):self.card7_strategy, 
                               type(card8()):self.card8_strategy, 
                               type(card10()):self.card10_strategy, 
                               type(card11()):self.card11_strategy, 
                               type(card12()):self.card12_strategy, 
                               type(cardsorry()):self.cardsorry_strategy
                               }
        

    def apply(self, card):
        self.cardstretegies[type(card)](card)

    def filtersortpawns(self):
		pawns = filter(lambda x: not self.game.board.in_home(x), self._player.pawns)
        return sorted(pawns, lambda x, y: cmp(x.positon, y.positon))

    def card1_2_common_strategy(self, card):
		pawns = self.filtersortpawns()
        done = False
        for pawn in pawns:
            pos = self.game.board.positon(card, pawn)
            slided_pos = self.game.board.slide(pos)
            if slided_pos > pawns.position():
                pawn.position = slided_pos
                done = True
                break
        if not done:
            for pawn in pawns:
                if pawn.in_start():
                    card.apply(pawn, None, card.CARD_MODE, self.game.board)
                    break

    def only_move_cards_common_strategy(self, card):
		pawns = self.filtersortpawns()
        for pawn in pawns:
            pos = self.game.board.positon(card, pawn)
            slided_pos = self.game.board.slide(pos)
            if slided_pos > pawns.position():
                pawn.position = slided_pos
                break

    def move_backwards_strategy(self, card):
		pawns = self.filtersortpawns()
        for pawn in pawns[::-1]:
            pos = self.game.board.positon(card, pawn)
            slided_pos = self.game.board.slide(pos)
            if slided_pos < pawns.position():
                pawn.position = slided_pos
                break

    def card1_strategy(self, card):
        card1_2_common_strategy(card)

    def card2_strategy(self, card):
        card1_2_common_strategy(card)

    def card3_strategy(self, card):
        only_move_cards_common_strategy(card)

    def card4_strategy(self, card):
        move_backwards_strategy(card)

    def card5_strategy(self, card):
        only_move_cards_common_strategy(card)

    def card7_strategy(self, card):
        only_move_cards_common_strategy(card)

    def card8_strategy(self, card):
        only_move_cards_common_strategy(card)

    def card10_strategy(self, card):
        pawns = self.filtersortpawns()
        done = False
        for pawn in pawns:
            pos = self.game.board.positon(card, pawn)
            slided_pos = self.game.board.slide(pos)
            if slided_pos > pawns.position():
                pawn.position = slided_pos
                done = True
                break
        if not done:
            for pawn in pawns[::-1]:
                pos = self.game.board.positon(card, pawn)
                slided_pos = self.game.board.slide(pos)
                if slided_pos < pawns.position():
                    pawn.position = slided_pos
                    break


    def card11_strategy(self, card):
        pawns = self.filtersortpawns()
        for pawn in pawns[::-1]:
            if pawn.position >= 0 and not self.game.board.in_safetyzone(pawn):
                break
        if not pawn: 
            # forfeit the turn due to no available pawns
            return
        ci = parameter().colors().index(pawn.color)

        min_dist = parameter().num_space 
        min_pawn = None
        for player in self._game.players:
            if player != self._player:
                for op in player.pawns:
                    if not self._game.board.in_safetyzone(op) and op.position != parameter().start_position:
                        dist = self._game.board.dist_home(op)
                        if dist < min_dist:
                            min_pawn = op
        if min_pawn:
            if self._game.board.distance(pawn, min_pawn) > 11:
                # switch
                pass
            else:
                # move foward 11 spaces
                pass

    def card12_strategy(self, card):
        only_move_cards_common_strategy(card)

    def cardsorry_strategy(self, card):
        pass

class game(object):
    def __init__(self):
        self._board = board()
        self._players = []
        self._strategy = strategy()

    def play():
        pass

    @property
    def board(self):
        return self._board

    @property
    def players(self):
        return self._players

    @property
    def strategy(self):
        return self._strategy
