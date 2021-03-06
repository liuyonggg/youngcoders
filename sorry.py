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
import random
import copy

class parameter(object):
    colors = ["YELLOW", "GREEN", "RED", "BLUE"]
    num_space = 60
    enterpoint_safety_zone = 1
    enterpoint_space = 3
    slide_1_space_begin = 0
    slide_1_space_end = 3
    slide_2_space_begin = 8
    slide_2_space_end = 12
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

    def in_home(self):
        return self._position == parameter.colors.index(self._color) * 15 + parameter().enterpoint_safety_zone + parameter().depth_safetyzone + 100 +parameter().num_space

class safetyzone(object):
    """ safetyzone: the place where the pawn won't be influence by opponents' pawn
       not in the 4 lines, enter point is first space in the corresponding line,  each zone takes 6 spaces
    """
    def __init__(self, color, enterpoint, prefix_position):
        self._color = color
        self._enterpoint = enterpoint
        self._depth = parameter.depth_safetyzone
        self._prefix = prefix_position

    def position(self, pos, spaces):
        assert (self.in_or_entering_safetyzone(pos))
        home_pos = self._prefix + self._depth + self._enterpoint
        if (pos == self._enterpoint):
            pos += self._prefix
        new_pos = pos + spaces
        if (new_pos > home_pos):
            new_pos = home_pos - (new_pos - home_pos)
        if (new_pos <= self._prefix + self._enterpoint):
            new_pos -= self._prefix
            if new_pos < 0:
                new_pos += 60
        return new_pos

    def in_safetyzone(self, pos):
        """
        decide if a position is in this safetyzone
        pos = number representing a position on the board
        """
        assert(pos <= self._prefix + self._depth + self._enterpoint)
        return (pos > self._prefix)

    def entering_safetyzone(self, pos):
        """
        decide if a position is at the enter point of this safetyzone
        pos = number representing a position on the board
        """
        return (pos == self._enterpoint)

    def in_or_entering_safetyzone(self, pos):
        """
        decide if a position is at the enter point of this safetyzone or the safetyzone itself
        pos = number representing a position on the board
        """
        return self.entering_safetyzone(pos) or self.in_safetyzone(pos)

    def in_home(self, pos):
        """
        decide if a position is in the home of the safety zone
        pos = number representing a position on the board
        """
        return (pos == self._prefix + self._enterpoint + self._depth)
        
class board(object):
    """ board: the place where the pawn put on
        1. 4 lines: 15 * 4 = 60 spaces
        2. 4 safety zones, not in the 4 lines, enter point is first space in the corresponding line,  each zone takes 6 spaces
        3. start point is not in the four lines, exit point is 4th space in the corresponding line
        4. slide point: the first space to the 4th space, the 9th space to 13th space
    """
    def __init__(self):
        colors = parameter().colors
        self._safetyzones = [safetyzone(colors[i], parameter.enterpoint_safety_zone + i * 15, parameter.num_space+100) for i in range(len(colors))]
        self._slides = {}
        for i in range(len(colors)):
            self._slides[i*15+parameter.slide_1_space_begin]  = i*15+parameter.slide_1_space_end
            self._slides[i*15+parameter.slide_2_space_begin]  = i*15+parameter.slide_2_space_end

    def position(self, pawn, spaces):
        if spaces < 0:
            return self.negative_position(pawn, spaces)
        new_pos = pawn.position
        entering_safetyzone = False
        for i in xrange(spaces):
            sz = self._safetyzones[parameter.colors.index(pawn.color)]
            if sz.in_or_entering_safetyzone(new_pos):
                entering_safetyzone = True
                break
            new_pos = new_pos + 1
            new_pos = new_pos % 60
        if entering_safetyzone:
            new_pos = sz.position(new_pos, spaces - i)
        return new_pos

    def negative_position(self, pawn, spaces):
        start = parameter.colors.index(pawn.color) * parameter.enterpoint_space
        if pawn.position > 100 + parameter.num_space + parameter.colors.index(pawn.color) * 15 + parameter.enterpoint_safety_zone:
            return self._safetyzones[parameter.colors.index(pawn.color)].position(pawn.position, spaces)

        if pawn.position + spaces < 2:
            return
        return pawn.position + spaces

    def slide(self, pawn):
        new_pos = pawn.position
        if new_pos == parameter.colors.index(pawn.color)*15:
            return new_pos
        if pawn.position in self._slides:
            new_pos = self._slides[pawn.position]
        return new_pos

    def in_home(self, pawn):
        ci = parameter().colors.index(pawn.color)
        return self._safetyzones[ci].in_home(pawn.position)

    def in_safetyzone(self, pawn):
        ci = parameter().colors.index(pawn.color)
        return self._safetyzones[ci].in_safetyzone(pawn.position)

    def dist_home(self, pawn):
        "distance to home"
        ci = parameter().colors.index(pawn.color)
        sz = self._safetyzones[ci]
        enterpoint = self._safetyzones[ci]._enterpoint
        if self.in_safetyzone(pawn):
            return (sz._enterpoint + sz._prefix + sz._depth) - pawn.position
        if pawn.position <= enterpoint:
            return (enterpoint - pawn.position) + sz._depth
        else:
            return (parameter.num_space - pawn.position) + enterpoint + sz._depth

    def distance(self, pawn1, pawn2):
        """
        distance from pawn1 to pawn2 counted in spaces on board
        pawn1: pawn object
        pawn2: pawn object
        """
        assert (not self.in_safetyzone(pawn1))
        assert (not self.in_safetyzone(pawn2))
        assert (pawn2.position != pawn1.position)
        if pawn2.position < pawn1.position:
            return parameter().num_space - (pawn1.position - pawn2.position)
        return pawn2.position - pawn1.position

class player(object):
    """each player has a name, color, 4 pawns and a strategy"""
    def __init__(self, name, color, strategy):
        self._name = name
        self._color = color
        self._pawns = [pawn(color, self, parameter.start_position) for i in range(4)]
        self._strategy = strategy

    def is_win(self):
        i = 0
        for pawn in self._pawns:
            if pawn.in_home():
                i += 1
        return i == len(self._pawns)

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

    def positions(self):
        return "%s's pawn positions:\n\t%d\n\t%d\n\t%d\n\t%d" % (self._name, self._pawns[0].position, self._pawns[1].position, self._pawns[2].position, self._pawns[3].position)

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
        if pawn1.position < 0:
            return
        new_pos = board.position(pawn1, spaces)
        if new_pos != None:
            pawn1.position = new_pos

    
class card1(cardcommon):
    " card 1: Move a pawn from Start or move a pawn one space forward.(unary) "
    CARD_MODE = ["START", "FORWARD"]
    def apply(self, pawn1, pawn2, mode, board):
        assert(not pawn2)
        if mode == self.CARD_MODE[1]:
            super(card1, self).apply(pawn1, pawn2, mode, board, 1)
        else:
            assert(mode == self.CARD_MODE[0])
            pawn1.position = parameter().colors.index(pawn1.color)*15 + parameter().enterpoint_space

    def getmodes(self):
        return self.CARD_MODE

    def __str__(self):
        return "You got card 1!"

    def __repr__(self):
        return self.__str__()

class card2(cardcommon):
    "card 2: Move a pawn from Start or move a pawn two spaces forward. Drawing a two entitles the player to draw again at the end of his or her turn. If the player cannot use a two to move, he or she can still draw again. (unary)"
    CARD_MODE = ["START", "FORWARD"]
    def apply(self, pawn1, pawn2, mode, board):
        assert(not pawn2)
        if mode == self.CARD_MODE[1]:
            super(card2, self).apply(pawn1, pawn2, mode, board, 2)
        else:
            pawn1.position = parameter().colors.index(pawn1.color)*15 + parameter().enterpoint_space
            print ("DEBUG: %s" % pawn1)

    def __str__(self):
        return "You got card 2!"

    def __repr__(self):
        return self.__str__()

class card3(cardcommon):
    "card 3: Move a pawn three spaces forward. (unary)"
    CARD_MODE = ["FORWARD"]
    def apply(self, pawn1, pawn2, mode, board):
        assert(not pawn2)
        super(card3, self).apply(pawn1, pawn2, mode, board, 3)

    def __str__(self):
        return "You got card 3!"

    def __repr__(self):
        return self.__str__()

class card4(cardcommon):
    "card 4: Move a pawn four spaces backward. (unary)"
    CARD_MODE = ["BACKWARDS"]
    def apply(self, pawn1, pawn2, mode, board):
        assert(not pawn2)
        super(card4, self).apply(pawn1, pawn2, mode, board, -4)

    def __str__(self):
        return "You got card 4!"

    def __repr__(self):
        return self.__str__()

class card5(cardcommon):
    "card 5: Move a pawn five spaces forward. (unary)"
    CARD_MODE = ["FORWARD"]
    def apply(self, pawn1, pawn2, mode, board):
        assert(not pawn2)
        super(card5, self).apply(pawn1, pawn2, mode, board, 5)

    def __str__(self):
        return "You got card 5!"

    def __repr__(self):
        return self.__str__()

class card7(cardcommon):
    "card 7: Move one pawn seven spaces forward, or split the seven spaces between two pawns (such as four spaces for one pawn and three for another). This makes it possible for two pawns to enter Home on the same turn, for example. The seven cannot be used to move a pawn out of Start, even if the player splits it into a six and one or a five and two. The entire seven spaces must be used or the turn is lost. You may not move backwards with a split. (binary)"
    CARD_MODE = ["FORWARD", "SPLIT"]
    def apply(self, pawn1, pawn2, mode, board):
        assert(not pawn2)
        super(card7, self).apply(pawn1, pawn2, mode, board, 7)

    def __str__(self):
        return "You got card 7!"

    def __repr__(self):
        return self.__str__()

class card8(cardcommon):
    "card 8: Move a pawn eight spaces forward. (unary)"
    CARD_MODE = ["FORWARD"]
    def apply(self, pawn1, pawn2, mode, board):
        assert(not pawn2)
        super(card8, self).apply(pawn1, pawn2, mode, board, 8)

    def __str__(self):
        return "You got card 8!"

    def __repr__(self):
        return self.__str__()

class card10(cardcommon):
    "card 10: Move a pawn 10 spaces forward or one space backward. If none of a player's pawns can move forward 10 spaces, then one pawn must move back one space. (unary)"
    CARD_MODE = ["BACKWARD", "FORWARD"]
    def apply(self, pawn1, pawn2, mode, board):
        assert(not pawn2)
        if mode == self.CARD_MODE[1]:
            super(card10, self).apply(pawn1, pawn2, mode, board, 10)
        else:
            assert(mode == self.CARD_MODE[0])
            super(card10, self).apply(pawn1, pawn2, mode, board, -1)

    def __str__(self):
        return "You got card 10!"

    def __repr__(self):
        return self.__str__()

class card11(cardcommon):
    "card 11: Move 11 spaces forward, or switch the places of one of the player's own pawns and an opponent's pawn. A player that cannot move 11 spaces is not forced to switch and instead can forfeit the turn. An 11 cannot be used to switch a pawn that is in a Safety Zone. (unary/binary)"
    CARD_MODE = ["FORWARD", "EXCHANGE"]
    def apply(self, pawn1, pawn2, mode, board):
        if mode == self.CARD_MODE[0]:
            super(card11, self).apply(pawn1, pawn2, mode, board, 11)
        else:
            assert(mode == self.CARD_MODE[1])
            p = pawn1.position
            pawn1.position = pawn2.position
            pawn2.position = p

    def __str__(self):
        return "You got card 11!"

    def __repr__(self):
        return self.__str__()

class card12(cardcommon):
    "card 12: Move a pawn 12 spaces forward. (unary)"
    CARD_MODE = ["FORWARD"]
    def apply(self, pawn1, pawn2, mode, board):
        assert(not pawn2)
        super(card12, self).apply(pawn1, pawn2, mode, board, 12)

    def __str__(self):
        return "You got card 12!"

    def __repr__(self):
        return self.__str__()

class cardsorry(cardcommon):
    "card sorry: Take any one pawn from Start and move it directly to a square occupied by any opponent's pawn, sending that pawn back to its own Start. A Sorry! card cannot be used on an opponent's pawn in a Safety Zone. If there are no pawns on the player's Start, or no opponent's pawns on any squares outside Safety Zones, the turn is lost. (binary)"
    def apply(self, pawn1, pawn2, mode, board):
        pawn1.position = pawn2.position
        pawn2.position = -1

    def __str__(self):
        return "You got card sorry!"

    def __repr__(self):
        return self.__str__()

class strategy(object):
    def __init__(self, game):
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

    def __str__(self):
        return "Automatic"

    def __repr__(self):
        return self.__str__()
        
    def set_player(self, player):
        self._player = player

    def apply(self, card):
        self.cardstretegies[type(card)](card)

    def filtersortpawns(self):
        pawns = filter(lambda x: not self._game.board.in_home(x), self._player.pawns)
        return sorted(pawns, lambda x, y: cmp(x.position, y.position), reverse=True)

    def card1_2_common_strategy(self, card):
        pawns = self.filtersortpawns()
        done = False
        for pawn in pawns:
            try:
                card.apply(pawn, None, card.CARD_MODE[1], self._game._board)
            except:
                break
            slided_pos = self._game.board.slide(pawn)
            done = True
            if slided_pos > pawn.position:
                pawn.position = slided_pos
                break
        if not done:
            for pawn in pawns:
                if pawn.in_start():
                    card.apply(pawn, None, card.CARD_MODE[0], self._game.board)
                    break

    def only_move_cards_common_strategy(self, card):
        pawns = self.filtersortpawns()
        for pawn in pawns:
            try:
                card.apply(pawn, None, None, self._game._board)
            except:
                return
            slided_pos = self._game.board.slide(pawn)
            if slided_pos > pawn.position:
                pawn.position = slided_pos
                break

    def move_backwards_strategy(self, card):
        pawns = self.filtersortpawns()
        for pawn in pawns[::-1]:
            try:
                card.apply(pawn, None, None, self._game._board)
            except:
                continue
            slided_pos = self._game.board.slide(pawn)
            if slided_pos > pawn.position:
                pawn.position = slided_pos
                break

    def card1_strategy(self, card):
        self.card1_2_common_strategy(card)

    def card2_strategy(self, card):
        self.card1_2_common_strategy(card)

    def card3_strategy(self, card):
        self.only_move_cards_common_strategy(card)

    def card4_strategy(self, card):
        self.move_backwards_strategy(card)

    def card5_strategy(self, card):
        self.only_move_cards_common_strategy(card)

    def card7_strategy(self, card):
        self.only_move_cards_common_strategy(card)

    def card8_strategy(self, card):
        self.only_move_cards_common_strategy(card)

    def card10_strategy(self, card):
        pawns = self.filtersortpawns()
        done = False
        for pawn in pawns:
            copy_pawn = copy.deepcopy(pawn)
            try:
                card.apply(copy_pawn, None, card.CARD_MODE[1], self._game.board)
            except:
                break
            if copy_pawn.position < pawn.position:
                break
            slided_pos = self._game.board.slide(copy_pawn)
            if slided_pos >= copy_pawn.position:
                pawn.position = slided_pos
                done = True
                pawn = copy_pawn
                return
        if not done:
            for pawn in pawns:
                try:
                    card.apply(pawn, None, card.CARD_MODE[0], self._game.board)
                except:
                    return
                pawn.position = self._game.board.slide(pawn)

    def card11_strategy(self, card):
        pawns = self.filtersortpawns()
        avaliable_pawn_1 = False
        avaliable_pawn_2 = False
        for pawn in pawns[::-1]:
            if pawn.position >= 0:
                avaliable_pawn_1 = True
                if not self._game.board.in_safetyzone(pawn):
                    avaliable_pawn_2 = True
                    break
        if avaliable_pawn_1 and not avaliable_pawn_2: 
            # forfeit the turn due to no available pawns
            card.apply(pawn, None, card11.CARD_MODE[0], self._game.board)
            pawn.position = self._game.board.slide(pawn)
            return

        elif not avaliable_pawn_1 and not avaliable_pawn_2:
            return

        min_dist = parameter().num_space 
        min_pawn = None
        max_score = -100 # amount of spaces pawn travels - the distance to home
        for player in self._game.players:
            if player != self._player:
                for op in player.pawns:
                    if not self._game.board.in_safetyzone(op) and not op.in_start():
                        score = self._game.board.distance(pawn, op) - self._game.board.dist_home(op)
                        if score > max_score:
                            max_score = score
                            min_pawn = op
        if min_pawn:
            if self._game.board.distance(pawn, min_pawn) > 11:
                card.apply(pawn, min_pawn, card11.CARD_MODE[1], self._game.board)
            else:
                card.apply(pawn, min_pawn, card11.CARD_MODE[0], self._game.board)
                pawn.position = self._game.board.slide(pawn)
        else:
            assert(not min_pawn)
            assert(max_score == -100)
            card.apply(pawn, min_pawn, card11.CARD_MODE[0], self._game.board)
            pawn.position = self._game.board.slide(pawn)

    def card12_strategy(self, card):
        self.only_move_cards_common_strategy(card)

    def cardsorry_strategy(self, card):
        pawns = self.filtersortpawns()
        avaliable_pawn = False
        for pawn in pawns:
            if pawn.position < 0:
                avaliable_pawn = True
                break
        if not avaliable_pawn: 
            # forfeit the turn due to no available pawns
            return

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
            card.apply(pawn, min_pawn, None, board)

class manual_strategy(strategy):
    def __str__(self):
        return "Manual"

    def apply(self, card, pawn, mode):
        self.cardstretegies[type(card)](card, pawn, mode)

    def card1_2_common_strategy(self, card, pawn, mode):
        card.apply(pawn, None, mode, self._game._board)
        pawn.position = self._game._board.slide(pawn)

    def only_move_cards_common_strategy(self, card, pawn, mode):
        card.apply(pawn, None, mode, self._game._board)
        pawn.position = self._game._board.slide(pawn)

    def card1_strategy(self, card, pawn, mode):
        self.card1_2_common_strategy(card, pawn, mode)

    def card2_strategy(self, card, pawn, mode):
        self.card1_2_common_strategy(card, pawn, mode)

    def card3_strategy(self, card, pawn, mode):
        self.only_move_cards_common_strategy(card, pawn, mode)

    def card4_strategy(self, card, pawn, mode):
        self.only_move_cards_common_strategy(card, pawn, mode)

    def card5_strategy(self, card, pawn, mode):
        self.only_move_cards_common_strategy(card, pawn, mode)

    def card7_strategy(self, card, pawn, mode):
        if mode == card.CARD_MODE[0]:
            self.only_move_cards_common_strategy(card, pawn, mode)
        else:
            self.card7_split_mode_strategy()

    def card7_split_mode_strategy(self):
        pawns = []
        while True:
            pawn1 = raw_input("Enter the pawn number for the first pawn: ")
            pawn2 = raw_input("Enter the pawn number for the second pawn: ")
            try:
                pawn1 = int(pawn1)
                pawn2 = int(pawn2)
            except ValueError:
                print("Wrong input!!!")
            if pawn1 < 4 and pawn1 >= 0 and pawn2 >= 0 and pawn2 < 4:
                break
            print("Wrong input!!!")

        while True:
            steps1 = raw_input("Enter the number of steps for the first pawn: ")
            steps2 = raw_input("Enter the number of steps for the second pawn: ")
            try:
                steps1 = int(steps1)
                steps2 = int(steps2)
            except ValueError:
                print("Wrong input!!!")
            if steps1 > 0 and steps2 > 0 and steps1 + steps2 == 7:
                break
            print("Wrong input!!!")

        pawn1 = self._player.pawns[pawn1-1]
        pawn2 = self._player.pawns[pawn2-1]
        cardcommon().apply(pawn1, None, None, self._game._board, steps1)
        pawn1.position = self._game._board.slide(pawn1)
        cardcommon().apply(pawn2, None, None, self._game._board, steps2)
        pawn2.position = self._game._board.slide(pawn2)

    def card8_strategy(self, card, pawn, mode):
        self.only_move_cards_common_strategy(card, pawn, mode)

    def card10_strategy(self, card):
        pass

    def card11_strategy(self, card):
        pass

    def card12_strategy(self, card, pawn, mode):
        self.only_move_cards_common_strategy(card, pawn, mode)

    def cardsorry_strategy(self, card):
        pass


class game(object):
    def __init__(self):
        self._board = board()
        self._strategies = [manual_strategy(self), manual_strategy(self), manual_strategy(self), manual_strategy(self)]
        self._players = [player("0", "YELLOW", self._strategies[0]), player("1", "GREEN", self._strategies[1]), player("2", "RED", self._strategies[2]), player("3", "BLUE", self._strategies[3])]
        for i in xrange(len(self._strategies)):
            self._strategies[i].set_player(self._players[i])
        self._deck = [card1(), card2(), card3(), card4(), card5(), card7(), card8(), card12()]

    def play(self):
        random.seed(0)
        num_of_player = int(raw_input("How many players(up to 4)?\n"))
        self._players = self._players[:num_of_player]
        if len(self._players) < 2 or len(self._players) > 4:
            return
        while True:
            auto_players = raw_input("How many automatic players(up to %d)\n" % (len(self._players)-1))
            try:
                auto_players = int(auto_players)
            except ValueError:
                print("Wrong input!!!\n")
                continue

            if int(auto_players) < len(self._players):
                break
            print("Wrong input!!!\n")

        for i in xrange(len(self._strategies[:auto_players])):
            self._strategies[i] = strategy(self)
            old_player = self._players[i]
            self._players[i] = player(old_player.name, old_player.color, self._strategies[i])
            self._strategies[i].set_player(self._players[i])

        while all([not game_player.is_win() for game_player in self._players]):
            for game_player in self._players:
                for playeri in self._players:
                    print(playeri.positions())
                print("It is player %s's turn\n" % game_player.name)
                i = random.randint(0, len(self._deck)-1)
                card = self._deck[i]
                print(card)
                if str(game_player._strategy) == "Automatic":
                    print("...\n")
                    game_player._strategy.apply(card)
                    continue

                if len(card.CARD_MODE) == 1:
                    print("\nThe only mode is %s\n".capitalize() % card.CARD_MODE[0])
                else:
                    assert(len(card.CARD_MODE) == 2)
                    print("\nThe modes are 1. %s and 2. %s\n".capitalize() % (card.CARD_MODE[0], card.CARD_MODE[1]))

                while True:
                    pawn = raw_input("Enter a number(1 for pawn 1 which has the position of %d, 2 for pawn 2 which has the position of %d, 3 for pawn 3 which has the position of %d, 4 for pawn 4 which has the position of %d):\n" % (game_player._pawns[0].position, game_player._pawns[1].position, game_player._pawns[2].position, game_player._pawns[3].position))
                    try:
                        pawn = int(pawn)
                    except ValueError:
                        print("Wrong input!!!\n")
                        continue

                    if pawn > 0 and pawn <= 4:
                        break
                    print("Wrong input!!!\n")

                while True:
                    mode = raw_input("Choose what to do(0 for mode 1, 1 for mode 2)\n")
                    if mode == '0' or mode == '1':
                        mode = int(mode)
                        if mode + 1 <= len(card.CARD_MODE):
                            break
                    print "Wrong input!!!\n"
                
                pawn = game_player.pawns[pawn-1]
                mode = card.CARD_MODE[mode]
                print mode
                game_player._strategy.apply(card, pawn, mode)

        print("Thank you for playing!")

    @property
    def board(self):
        return self._board

    @property
    def players(self):
        return self._players

    @property
    def strategy(self):
        return self._strategies
