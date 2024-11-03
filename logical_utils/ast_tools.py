import ast

def if_logic_check(x):
    try:
        tree = ast.parse(x, mode='exec')
        san_checker = IfCounter()
        return san_checker.san_check(tree)
    except SyntaxError:
        return False

def logical_consistency_check(x):
    try:
        tree = ast.parse(x, mode='exec')
        san_checker = LogicalChecker()
        return san_checker.san_check(tree)
    except SyntaxError:
        return False, ""

# def logical_consistency_check(x, type):
#     if type == "in":
#         try:
#             tree = ast.parse(x, mode='exec')
#             san_checker = LogicalChecker()
#             return san_checker.san_check(tree)
#         except SyntaxError:
#             return False, ""
#     elif type == "bool":
#         try:
#             tree = ast.parse(x, mode='exec')
#             san_checker = bool_LogicalChecker()
#             return san_checker.san_check(tree)
#         except SyntaxError:
#             return False, ""
            

# we only use simple examples with necessary Logic
class IfCounter(ast.NodeVisitor):
    def __init__(self):
        self.if_count = 0
        self.found_if_else = False

    def visit_If(self, node):
        if node.orelse:
            self.found_if_else = True

        self.if_count += 1
        self.generic_visit(node)

    def san_check(self, node):
        # the name of this func is just for fun
        self.visit(node)
        if self.if_count == 1 and self.found_if_else == False:
            return True
        else:
            return False


# Check if the candidates exist in the if structure
# We need to make sure the left value of the comparision is the value of remove function.
# By checking this, we can make sure the logical consistency is literally exist:
# Only if the Value exists, we are able to remove it.

class LogicalChecker(ast.NodeVisitor):
    def __init__(self):
        self.logical_consistency = False
        self.label = ""

    def get_var_name(self, node):
        """Helper function to extract the variable name from an AST node."""
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Name):
            return node.id
        return None

    def visit_If(self, node):
        # in - remove
        if isinstance(node.test, ast.Compare) and any(isinstance(op, ast.In) for op in node.test.ops):
            left_var = self.get_var_name(node.test.left)
            
            for expr in node.body:
                if (isinstance(expr, ast.Expr) and
                        isinstance(expr.value, ast.Call) and
                        isinstance(expr.value.func, ast.Attribute) and
                        expr.value.func.attr == 'remove'):
                    
                    if expr.value.args:  # 检查 args 列表是否非空
                        arg_var = self.get_var_name(expr.value.args[0])
                        if left_var == arg_var:
                            self.logical_consistency = True
                            self.label = "remove"

        # not in - append
        elif isinstance(node.test, ast.Compare) and any(isinstance(op, ast.NotIn) for op in node.test.ops):
            left_var = self.get_var_name(node.test.left)
            
            for expr in node.body:
                if (isinstance(expr, ast.Expr) and
                        isinstance(expr.value, ast.Call) and
                        isinstance(expr.value.func, ast.Attribute) and
                        expr.value.func.attr == 'append'):
                    
                    if expr.value.args:  # 检查 args 列表是否非空
                        arg_var = self.get_var_name(expr.value.args[0])
                        if left_var == arg_var:
                            self.logical_consistency = True
                            self.label = "append"

        else:
            self.logical_consistency = False

        return self.generic_visit(node)

    def san_check(self, node):
        # The name of this function is just for fun
        self.visit(node)
        return self.logical_consistency, self.label

# class bool_LogicalChecker(ast.NodeVisitor):
#     def __init__(self):
#         self.logical_consistency = False
#         self.label = ""

#     def visit_If(self, node):
#         # True - False
#         if isinstance(node.test, ast.Compare) and any(isinstance(op, ast.In) for op in node.test.ops):

#             left_value = node.test.left
#             if isinstance(left_value, ast.Constant):
#                 left_var = left_value.value
#             elif isinstance(left_value, ast.Name):
#                 left_var = left_value.id
#             else:
#                 left_var = None
    
#             for expr in node.body:
#                 if (isinstance(expr, ast.Expr) and
#                         isinstance(expr.value, ast.Call) and
#                         isinstance(expr.value.func, ast.Attribute) and
#                         expr.value.func.attr == 'remove'):
#                     arg_value = expr.value.args[0]
#                     if isinstance(arg_value, ast.Constant):
#                         arg_var = arg_value.value
#                     elif isinstance(arg_value, ast.Name):
#                         arg_var = arg_value.id
#                     else:
#                         arg_var = None
        
#                     if left_var == arg_var:
#                         self.logical_consistency = True
#                         self.label = "remove"

#         # not in - append
#         elif isinstance(node.test, ast.Compare) and any(isinstance(op, ast.NotIn) for op in node.test.ops):
#             left_value = node.test.left
#             if isinstance(left_value, ast.Constant):
#                 left_var = left_value.value
#             elif isinstance(left_value, ast.Name):
#                 left_var = left_value.id
#             else:
#                 left_var = None
                
#             for expr in node.body:
#                 if (isinstance(expr, ast.Expr) and
#                         isinstance(expr.value, ast.Call) and
#                         isinstance(expr.value.func, ast.Attribute) and
#                         expr.value.func.attr == 'append'):
                    
#                     arg_value = expr.value.args[0]
#                     if isinstance(arg_value, ast.Constant):
#                         arg_var = arg_value.value
#                     elif isinstance(arg_value, ast.Name):
#                         arg_var = arg_value.id
#                     else:
#                         arg_var = None
                        
#                     if left_var == arg_var:
#                         self.logical_consistency = True
#                         self.label = "append"

#         else:
#             self.logical_consistency = False

#         return self.generic_visit(node)

#     def san_check(self, node):
#         # the name of this func is just for fun
#         self.visit(node)
#         return self.logical_consistency, self.label


# to exchange in to not in (Unfortunately there is not "not in - append) relations in the dataset.
# With the method here we can easily generate logical consistency from any other exist code datasets.

# mask the "keyword" with "$$$", generate label for the individual example, and modify the inverse "in/not in".
class KeywordMasker(ast.NodeTransformer):
    def __init__(self, new_attr_value='$$$'):
        self.new_attr_value = new_attr_value
        self.flag = ""

    def visit_If(self, node):
        if any(isinstance(op, ast.In) for op in node.test.ops):
            left_value = node.test.left
            if isinstance(left_value, ast.Constant):
                left_var = left_value.value
            elif isinstance(left_value, ast.Name):
                left_var = left_value.id
            else:
                left_var = None

            for expr in node.body:
                if (isinstance(expr, ast.Expr) and
                        isinstance(expr.value, ast.Call) and
                        isinstance(expr.value.func, ast.Attribute) and
                        expr.value.func.attr == 'remove'):
                    arg_value = expr.value.args[0]
                    if isinstance(arg_value, ast.Constant):
                        arg_var = arg_value.value
                    elif isinstance(arg_value, ast.Name):
                        arg_var = arg_value.id
                    else:
                        arg_var = None

                    # check if this arg is what we want
                    if left_var == arg_var:
                        #print(self.flag)
                        if self.flag == "masker":
                            expr.value.func.attr = self.new_attr_value

                        elif self.flag == "inverser":
                            #print("aaaaaaaaaa")
                            expr.value.func.attr = self.new_attr_value
                            node.test.ops = [ast.NotIn()]

        elif any(isinstance(op, ast.NotIn) for op in node.test.ops):
            left_value = node.test.left
            if isinstance(left_value, ast.Constant):
                left_var = left_value.value
            elif isinstance(left_value, ast.Name):
                left_var = left_value.id
            else:
                left_var = None

            for expr in node.body:
                if (isinstance(expr, ast.Expr) and
                        isinstance(expr.value, ast.Call) and
                        isinstance(expr.value.func, ast.Attribute) and
                        expr.value.func.attr == 'append'):
                    arg_value = expr.value.args[0]
                    if isinstance(arg_value, ast.Constant):
                        arg_var = arg_value.value
                    elif isinstance(arg_value, ast.Name):
                        arg_var = arg_value.id
                    else:
                        arg_var = None

                    # check if this arg is what we want
                    if left_var == arg_var:
                        if self.flag == "masker":
                            expr.value.func.attr = self.new_attr_value

                        elif self.flag == "inverser":
                            expr.value.func.attr = self.new_attr_value
                            node.test.ops = [ast.In()]
                        
        return self.generic_visit(node)

    def processor(self, node, flag):
        # Apply masking
        self.flag = flag
        tree = self.visit(node)
        return tree
