from movie_node import MovieNode

class MovieRatingSystem:
    def __init__(self):
        self.root = None

        # Used so delete(name) can locate the movie's rating quickly.
        # The movies themselves are still stored in the AVL tree.
        self._ratings_by_name = {}

    def _getHeight(self, node):
        if not node:
            return 0

        return node.height

    def _getBalanceFactor(self, node):
        if not node:
            return 0

        return self._getHeight(node.left) - self._getHeight(node.right)

    def _rightRotate(self, y):
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        y.height = 1 + max(
            self._getHeight(y.left),
            self._getHeight(y.right)
        )

        x.height = 1 + max(
            self._getHeight(x.left),
            self._getHeight(x.right)
        )

        return x

    def _leftRotate(self, x):
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights
        x.height = 1 + max(
            self._getHeight(x.left),
            self._getHeight(x.right)
        )

        y.height = 1 + max(
            self._getHeight(y.left),
            self._getHeight(y.right)
        )

        return y

    def _key(self, name, rating):
        # Rating is the main AVL-tree key.
        # Name is only used when two movies have the same rating.
        return (rating, name)

    def insert(self, name, rating):
        if rating < 1 or rating > 10:
            return

        # If the same movie already exists,
        # remove its old entry before inserting again.
        if name in self._ratings_by_name:
            self.delete(name)

        self.root = self._insert(self.root, name, rating)

        self._ratings_by_name[name] = rating

    def _insert(self, node, name, rating):
        # Normal BST insertion
        if not node:
            return MovieNode(name, rating)

        key = self._key(name, rating)
        node_key = self._key(node.name, node.rating)

        if key < node_key:
            node.left = self._insert(
                node.left,
                name,
                rating
            )
        else:
            node.right = self._insert(
                node.right,
                name,
                rating
            )

        # Update height
        node.height = 1 + max(
            self._getHeight(node.left),
            self._getHeight(node.right)
        )

        # Get balance factor
        balance = self._getBalanceFactor(node)

        # Left Left Case
        if balance > 1:
            left_key = self._key(
                node.left.name,
                node.left.rating
            )

            if key < left_key:
                return self._rightRotate(node)

            # Left Right Case
            else:
                node.left = self._leftRotate(node.left)
                return self._rightRotate(node)

        # Right Right Case
        if balance < -1:
            right_key = self._key(
                node.right.name,
                node.right.rating
            )

            if key > right_key:
                return self._leftRotate(node)

            # Right Left Case
            else:
                node.right = self._rightRotate(node.right)
                return self._leftRotate(node)

        return node

    def get_top_rated(self):
        if not self.root:
            return None

        current = self.root

        # Highest rating is at the rightmost node
        while current.right:
            current = current.right

        return current.name

    def get_movies_in_range(self, min_rating, max_rating):
        movies = []

        self._get_movies_in_range(
            self.root,
            min_rating,
            max_rating,
            movies
        )

        return movies

    def _get_movies_in_range(
        self,
        node,
        min_rating,
        max_rating,
        movies
    ):
        if not node:
            return

        # In-order traversal:
        # left -> root -> right

        if node.rating >= min_rating:
            self._get_movies_in_range(
                node.left,
                min_rating,
                max_rating,
                movies
            )

        if min_rating <= node.rating <= max_rating:
            movies.append(node.name)

        if node.rating <= max_rating:
            self._get_movies_in_range(
                node.right,
                min_rating,
                max_rating,
                movies
            )

    def delete(self, name):
        if name not in self._ratings_by_name:
            return

        rating = self._ratings_by_name[name]

        self.root = self._delete(
            self.root,
            name,
            rating
        )

        del self._ratings_by_name[name]

    def _delete(self, node, name, rating):
        if not node:
            return None

        key = self._key(name, rating)
        node_key = self._key(
            node.name,
            node.rating
        )

        # Normal BST deletion
        if key < node_key:
            node.left = self._delete(
                node.left,
                name,
                rating
            )

        elif key > node_key:
            node.right = self._delete(
                node.right,
                name,
                rating
            )

        else:
            # Node with only right child or no child
            if not node.left:
                return node.right

            # Node with only left child
            elif not node.right:
                return node.left

            # Node with two children:
            # get smallest node from right subtree
            min_node = self._findMin(node.right)

            node.name = min_node.name
            node.rating = min_node.rating

            node.right = self._delete(
                node.right,
                min_node.name,
                min_node.rating
            )

        # Update height
        node.height = 1 + max(
            self._getHeight(node.left),
            self._getHeight(node.right)
        )

        # Get balance factor
        balance = self._getBalanceFactor(node)

        # Left Left Case
        if balance > 1 and \
                self._getBalanceFactor(node.left) >= 0:

            return self._rightRotate(node)

        # Left Right Case
        if balance > 1 and \
                self._getBalanceFactor(node.left) < 0:

            node.left = self._leftRotate(node.left)
            return self._rightRotate(node)

        # Right Right Case
        if balance < -1 and \
                self._getBalanceFactor(node.right) <= 0:

            return self._leftRotate(node)

        # Right Left Case
        if balance < -1 and \
                self._getBalanceFactor(node.right) > 0:

            node.right = self._rightRotate(node.right)
            return self._leftRotate(node)

        return node

    def _findMin(self, node):
        current = node

        while current.left:
            current = current.left

        return current