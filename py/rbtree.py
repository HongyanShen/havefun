import enum

class color(enum.Enum):
    RED = 1
    BLACK = 2

class node:
    parent: 'node'
    left: 'node'
    right: 'node'
    value: 'node'
    color: color

    def __init__(self, parent: 'node', left: 'node', right: 'node', value = None, color: color = color.BLACK):
        super(node, self).__init__()
        self.parent = parent
        self.left = left
        self.right = right
        self.value = value
        self.color = color

def is_red(node: node):
    return node and node.color is color.RED

def is_black(node: node):
    return not node or node.color is color.BLACK # nil 节点为空

def set_red(*args):
    for node in args:
        node.color = color.RED

def set_black(*args):
    for node in args:
        node.color = color.BLACK

def set_color(node: node, color: color):
    if node: node.color = color

def get_color(node: node) -> color:
    if not node: return color.BLACK
    return node.color

class rb_tree:
    root: node

    def __init__(self):
        super(rb_tree, self).__init__()
        self.root = None

    def rotate_left(self, node: node):
        if node:
            r = node.right

            node.right = r.left
            if r.left: r.left.parent = node

            p = node.parent
            if not p: self.root = r
            elif p.right is node: p.right = r
            else: p.left = r
            r.parent = p

            r.left = node
            node.parent = r

    def rotate_right(self, node: node):
        if node:
            l = node.left

            node.left = l.right
            if l.right: l.right.parent = node

            p = node.parent
            if not p: self.root = l
            elif p.right is node: p.right = l
            else: p.left = l
            l.parent = p

            node.parent = l
            l.right = node

    def add(self, value):
        if not self.root:
            self.root = node(None, None, None, value=value, color=color.BLACK)
            return True

        p = self.root
        newnode: node = None
        while True:
            v = p.value

            if v == value: 
                return False
            elif v < value:
                if p.right: 
                    p = p.right
                else:
                    p.right = newnode = node(p, None, None, value=value, color=color.RED)
                    break
            else:
                if p.left: 
                    p = p.left
                else: 
                    p.left = newnode = node(p, None, None, value=value, color=color.RED)
                    break

        self.fix_after_insertion(newnode)
        return True
        
    def fix_after_insertion(self, node: node):
        while node and node.parent and node.color is color.RED:
            p = node.parent
            if p.color is color.BLACK: return

            pp = p.parent

            if p is pp.left:
                u = pp.right
                if is_red(u):
                    set_black(p, u)
                    set_red(pp)
                    node = pp
                else:
                    if node is p.right:
                        self.rotate_left(p)
                        node = p
                    set_black(node.parent)
                    set_red(node, node.parent.parent)
                    self.rotate_right(pp)
            else:
                u = pp.left
                if is_red(u):
                    set_black(p, u)
                    set_red(pp)
                    node = pp
                else:
                    if node is p.left:
                        self.rotate_right(p)
                        node = p
                    set_black(node.parent)
                    set_red(node, node.parent.parent)
                    self.rotate_left(pp)

        self.root.color = color.BLACK

    def remove(self, value):
        n = self.root
        if not n: return False

        while n:
            v = n.value
            if v == value:
                break
            elif v < value:
                n = n.right
            else:
                n = n.left

        if not n:
            return False

        d = n
        # 从右子树找后继节点
        if d.right:
            d = d.right
            while d.left:
                d = d.left

        d.value, n.value = n.value, d.value
        if d is n:
            if d.left:
                d = d.left
                while d.right:
                    d = d.right


        repalce = d.left if d.left else d.right # 后继节点的替换节点
        if repalce: # 直接用子节点替代被删除的节点，该子节点必然为红色，只需要将其涂黑即可
            repalce.parent = d.parent
            if d.parent:
                if d.parent.left is d: d.parent.left = repalce
                else: d.parent.right = repalce
            else: self.root = repalce

            d.parent, d.left, d.right = None, None, None
            if is_black(d):
                self.fix_after_deletion(repalce) # replace为红节点 直接涂黑
        elif d.parent is None: # 被删除节点为根节点
            self.root = None
        else: # 删除节点没有替换节点
            if is_black(d):
                self.fix_after_deletion(d)

            if d.parent:
                if d is d.parent.left: d.parent.left = None
                else: d.parent.right = None
                d.parent = None

        # 删除d
        return True

    def fix_after_deletion(self, node: node):
        while node and node.parent and is_black(node):
            if node is node.parent.left:
                sib = node.parent.right
                if is_red(sib):
                    set_black(sib)
                    set_red(node.parent)
                    self.rotate_left(node.parent)
                    sib = node.parent.right

                if is_black(sib.left) and is_black(sib.right):
                    set_red(sib)
                    node = node.parent
                else:
                    if is_black(sib.right): # 将远侄子节点处理成红色
                        set_black(sib.left)
                        set_red(sib)
                        self.rotate_right(sib)
                        sib = node.parent.right

                    set_color(sib, get_color(node.parent))
                    set_black(node.parent, sib.right)
                    self.rotate_left(node.parent)
                    node = self.root
            else:
                sib = node.parent.left

                if is_red(sib):
                    set_red(node.parent)
                    set_black(sib)
                    self.rotate_right(node.parent)
                    sib = node.parent.left

                if is_black(sib.left) and is_black(node.right):
                    set_red(sib)
                    node = node.parent
                else:
                    if is_black(sib.left):
                        set_red(sib)
                        set_black(sib.right)
                        self.rotate_left(sib)
                        sib = node.parent.left

                    set_color(sib, get_color(node.parent))
                    set_black(sib.left, node.parent)
                    self.rotate_right(node.parent)
                    node = self.root

        set_black(node)

def print_rb_tree(t: rb_tree):
    if not t.root: print("empty")
    
    l = [t.root]
    layer = 1

    while l:
        next_layer = list()
        for item in l:
            if item:
                next_layer.append(item.left)
                next_layer.append(item.right)
            else:
                next_layer.append(None)
                next_layer.append(None)

        for item in l:
            print("-" * layer, end="")
            c = 'b' if is_black(item) else 'r'
            if item:
                print(f'[{item.value}, {c}]')
            else:
                print('[nil, b]')

        hasElement = False
        for item in next_layer:
            if item: hasElement = True

        if hasElement:
            l = next_layer
            layer += 1
        else:
            break

if __name__ == '__main__':
    rbt = rb_tree()
    rbt.add(10)
    rbt.add(5)
    rbt.add(6)
    rbt.add(8)
    rbt.add(2)
    rbt.add(1)
    rbt.add(3)
    rbt.add(7)
    rbt.add(9)
    rbt.add(4)
    rbt.add(0)

    rbt.remove(8)
    rbt.remove(7)
    rbt.remove(6)
    rbt.remove(9)

    print_rb_tree(rbt)