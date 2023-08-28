#!/usr/bin/env python3

__copyright__ = """

    Copyright 2023 Marc SIBERT

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""
__license__ = "Apache 2.0"

class Board:
    def __init__(self):
        """Constructeur d'instance, initialise le tableau avec des espaces"""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

    def evaluate(self) -> int:
        """Vérifier les lignes, colonnes et diagonales pour voir s'il y a un gagnant.

        :return: Une valeur entière indiquant +10 si X est gagnant, -10 si O est gagnant, 0 sinon
        (nulle ou partie en cours)
        """
        # alignement horizontal
        for row in self.board:
            if all(cell == 'X' for cell in row):
                return 10
            elif all(cell == 'O' for cell in row):
                return -10

        # alignement vertical
        for col in range(3):
            if all(self[row, col] == 'X' for row in range(3)):
                return 10
            elif all(self[row, col] == 'O' for row in range(3)):
                return -10

        # test des diagonales
        if all(self[i, i] == 'X' for i in range(3)) or all(self[i, 2 - i] == 'X' for i in range(3)):
            return 10
        elif all(self[i, i] == 'O' for i in range(3)) or all(self[i, 2 - i] == 'O' for i in range(3)):
            return -10

        return 0  # Match nul

    def __str__(self) -> str:
        """Crée une représentation du plateau de jeu.

        :return: La représentation du jeu sous forme de caractères ASCII."""
        s: str = " " * 5 + (" " * 5).join(chr(ord('A') + i) for i in range(3)) + "\n"
        s += "  +" + "-----+" * 3 + "\n"
        for i, _ in enumerate(self.board):
            s += str(i) + " |  " + '  |  '.join(_) + "  |\n"
            s += "  +" + "-----+" * 3 + "\n"
        return s

    def __getitem__(self, key: (int, int)) -> str:
        """Ajoute la capacité de lire un élément de la matrice avec une liste de 2 entiers
        au moyen d'une syntaxe de tableau : Jeu[x, y]

        :param key: Un tuple contenant les 2 index (x, y) de la matrice du jeu.
        :type key: (int, int)
        :return: Le signe stocké dans la matrice du jeu.
        :rtype: str
        """
        _row, _col = list(key)
        assert _row in (0, 1, 2) and _col in (0, 1, 2)
        return self.board[_row][_col]

    def __setitem__(self, key: (int, int), value: chr):
        _row, _col = list(key)
        assert _row in (0, 1, 2) and _col in (0, 1, 2)
        assert value in ('X', 'O', ' ')
        self.board[_row][_col] = value

    def is_moves_left(self) -> bool:
        """Indique s'il reste encore des emplacements libres : la partie peut se poursuivre."""
        return any(cell == ' ' for row in self.board for cell in row)

    def find_best_move(self) -> (int, int):
        """Retourne le meilleur coup de X."""
        best_move = (-1, -1)
        best_score = -float('inf')

        _all = list()
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.board[i][j] = 'X'
                    move_score = self.minimax(0, False)
                    _all.append(move_score)
                    self.board[i][j] = ' '
                    if move_score > best_score:
                        best_score = move_score
                        best_move = (i, j)

        if min(_all) > 0 and max(_all) > 0:
            print("++")
        elif min(_all) == 0 and max(_all) > 0:
            print("0+ C'est mort là !")
        elif min(_all) == 0 and max(_all) == 0:
            print("00 C'est indécis.")
        elif min(_all) < 0 and max(_all) > 0:
            print("-+ Ah c'est gagné !")
        elif min(_all) < 0 and max(_all) == 0:
            print("-0")
        elif min(_all) < 0 and max(_all) < 0:
            print("--")
        return best_move

    def minimax(self, depth, is_maximizer) -> int:
        """Algorithme du MinMax retournant la note du dernier cout selon le min ou le max.
        :param depth: Profondeur du coup à étudier.
        :type depth: int
        :param is_maximizer: Indique si recherche du min ou du max et du joueur courant.
        :type is_maximizer: bool
        """
        if not self.is_moves_left():
            return 0

        score = self.evaluate()
        if score != 0:
            return score - round((score * depth) / abs(score))

        if is_maximizer:
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = 'X'
                        best_score = max(best_score, self.minimax(depth + 1, not is_maximizer))
                        self.board[i][j] = ' '
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = 'O'
                        best_score = min(best_score, self.minimax(depth + 1, not is_maximizer))
                        self.board[i][j] = ' '
            return best_score

    @staticmethod
    def plays_first() -> str:
        """Lance le jeu avec le programme qui joue les X en premier
        :return: Un court texte indiquant la raison de l'arrêt (succès, échec ou nul)
        """
        board = Board()
        while board.is_moves_left():
            print("Je joue :")
            row, col = board.find_best_move()
            board[row, col] = 'X'

            print(board)

            if board.evaluate() == 10:
                return "Tu as perdu !"

            if not board.is_moves_left():
                return "Match nul !"

            inp = input("Position pour O (lettre + chiffre) : ")
            col = ord(inp[0]) - ord('A')
            row = int(inp[1])
            while col not in range(3) or row not in range(3) or board[row, col] != ' ':
                print("Saisie incorrecte ou cellule déjà occupée. Réessaye !")
                inp = input("Position pour O (lettre + chiffre) : ")
                col = ord(inp[0]) - ord('A')
                row = int(inp[1])

            board[row, col] = 'O'
            print(board)

            if board.evaluate() == -10:
                return "Tu as gagné !"


if __name__ == "__main__":
    print(Board.plays_first())
