# Лабораторная работа №3: Исупов Григорий, Рид Екатерина
# Python 3.12.1

from __future__ import annotations


class Node(object):
    """
    Элемент дерева
    """
    def __init__(self, value: int):
        self.value = value
        self.left = None
        self.right = None

    def setLeft(self, left: Node) -> None:
        self.left = left

    def setRight(self, right: Node) -> None:
        self.right = right


class BinaryTree(object):
    """
    Бинарное дерево
    """
    def __init__(self):
        self.root = None

    def _height(self):
        """
        Возвращает высоту дерева
        :return: {int} высота дерева
        """
        def height(node):
            if node is None:
                return 0

            left_height = height(node.left)
            right_height = height(node.right)

            return max(left_height, right_height) + 1

        return height(self.root)

    def insert(self, value: int) -> None:
        """
        Вставляет элемент в дерево
        :param value: {int} значение элемента
        :return: None
        """
        self.root = self._insert_recursive(value, self.root)

    def _insert_recursive(self, value: int, root: Node) -> Node:
        """
        Вставляет элемент в дерево рекурсивно
        :param value: {int} значение элемента
        :param root: {Node} корень дерева (или корень поддерева)
        :return: {Node} корень всего дерева
        """
        if root is None:
            return Node(value)

        if value < root.value:
            root.setLeft(self._insert_recursive(value, root.left))
        elif value > root.value:
            root.setRight(self._insert_recursive(value, root.right))
        return root

    def delete(self, value: int) -> None:
        """
        Удаляет элемент из дерева
        :param value: {int} значение элемента
        :return: None
        """
        self.root = self._delete_recursive(value, self.root)

    def _delete_recursive(self, value: int, root: Node) -> Node:
        """
        Удаляет элемент из дерева рекурсивно
        :param value: {int} значение элемента
        :param root: {Node} корень дерева (или корень поддерева)
        :return: {Node} корень всего дерева
        """
        if root is None:
            return root
        if value < root.value:
            root.setLeft(self._delete_recursive(value, root.left))
        elif value > root.value:
            root.setRight(self._delete_recursive(value, root.right))
        else:
            if root.left is None:
                return root.right
            if root.right is None:
                return root.left

            root.value = self._max_value_in_subTree(root.right).value
            root.right = self._delete_recursive(root.value, root.right)
        return root

    def _max_value_in_subTree(self, node):
        """
        Возвращает максимальное значение в поддереве
        :param node: {Node} корень поддерева
        :return: {Node} узел с максимальным значением
        """
        current = node
        while current.left is not None:
            print(current)
            current = current.left
        return current

    def __str__(self):
        """
        Красивый и понятный вывод дерева.
        :return: {str} дерево в виде строки
        """
        height_of_tree: int = self._height()

        line_length: int = 2 ** height_of_tree

        # [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '5', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        # [' ', ' ', ' ', ' ', '┌','─', '─', '─', '┴', '─', '─', '─', '┐', ' ', ' ', ' '], ...
        # Вот так в итоге будет выглядеть этот двумерный список, который потом просто join в строку
        tree_lines_list: list[list[str]] = [[' '] * line_length * 2 for _ in range(height_of_tree * 2)]

        current_level = [(self.root, line_length)]
        for level_index in range(height_of_tree):
            next_level = []
            for node, line_length_local in current_level:
                tree_lines_list[level_index * 2][line_length_local] = str(node.value)
                conn_row = tree_lines_list[level_index * 2 + 1]
                if node.left:
                    left_line_length = line_length_local - 2 ** (height_of_tree - level_index - 1)
                    next_level.append((node.left, left_line_length))

                    conn_row[line_length_local] = "┘"
                    conn_row[left_line_length] = "┌"
                    for j in range(left_line_length + 1, line_length_local):
                        conn_row[j] = "─"
                if node.right:
                    right_line_length = line_length_local + 2 ** (height_of_tree - level_index - 1)
                    next_level.append((node.right, right_line_length))

                    conn_row[line_length_local] = "└"
                    conn_row[right_line_length] = "┐"
                    for j in range(line_length_local + 1, right_line_length):
                        conn_row[j] = "─"
                if node.left and node.right:
                    conn_row[line_length_local] = "┴"
            current_level = next_level

        res: str = ""
        for row in tree_lines_list:
            res += ''.join(row) + "\n"
        return res


if __name__ == '__main__':
    convert_to_int_or_float = (lambda x: float(x) if '.' in x else int(x))

    tree = BinaryTree()
    tree_elements = list(map(convert_to_int_or_float, input("Введите элементы дерева через пробел: ").split()))
    for element in tree_elements:
        tree.insert(element)

    delete_element = convert_to_int_or_float(input("Введите элемент для удаления: "))
    tree.delete(delete_element)
    print(tree)
