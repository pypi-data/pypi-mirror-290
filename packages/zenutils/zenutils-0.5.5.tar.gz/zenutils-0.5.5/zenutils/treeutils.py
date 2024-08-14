#!/usr/bin/env python
# -*- coding: utf8 -*-
"""树结构工具。"""
from __future__ import (
    absolute_import,
    division,
    generators,
    nested_scopes,
    print_function,
    unicode_literals,
    with_statement,
)
from zenutils import dictutils

__all__ = [
    "build_tree",
    "tree_walk",
    "print_tree_callback",
    "print_tree",
    "SimpleRouterTree",
]


def build_tree(
    thelist, pk_attr="id", parent_attr="parent_id", children_attr="children"
):
    """
    Tree node is a dict with pk_attr, parent_attr and children_attr fields:
        {
            "id": 2,
            "parent_id": 1,
            "children": []
        }.
    """

    roots = []
    nodes = {}
    for node in thelist:
        dictutils.touch(node, children_attr, [])
        node_id = dictutils.select(node, pk_attr)
        nodes[node_id] = node
    for node in thelist:
        parent_id = dictutils.select(node, parent_attr)
        if (not parent_id) or (not parent_id in nodes):
            roots.append(node)
        else:
            dictutils.select(nodes[parent_id], children_attr).append(node)
    return roots


def tree_walk(
    tree,
    callback,
    children_attr="children",
    callback_args=None,
    callback_kwargs=None,
    depth=0,
    parent=None,
):
    """遍历树，并执行回调函数。"""
    callback_args = callback_args or ()
    callback_kwargs = callback_kwargs or {}

    for node in tree:
        callback(node, tree, depth, parent, *callback_args, **callback_kwargs)
        children = dictutils.select(node, children_attr, [])
        if children:
            tree_walk(
                children,
                callback,
                children_attr,
                callback_args,
                callback_kwargs,
                depth + 1,
                node,
            )


def print_tree_callback(node, tree, depth, parent, *args, **kwargs):
    """遍历树并打印输出节点。使用4个空格做缩进。"""
    title_attr = kwargs.get("title_attr", "title")
    indent_string = kwargs.get("indent_string", "    ")
    print(indent_string * depth + dictutils.select(node, title_attr))


def print_tree(
    tree, title_attr="title", children_attr="children", indent_string="     "
):
    """遍历树并打印输出节点。使用4个空格做缩进。"""
    tree_walk(
        tree,
        print_tree_callback,
        children_attr,
        (),
        {"title_attr": title_attr, "indent_string": indent_string},
    )


class SimpleRouterTree(object):
    """
    简单的路由索引和搜索树。
    """

    def __init__(self):
        self.data = {}
        self.paths = {}

    def index(self, path, data):
        """索引"""
        cp = self.data
        for c in path:
            if not c in cp:
                cp[c] = {}
            cp = cp[c]
        cp["_data"] = data
        cp["_path"] = path
        self.paths[path] = cp
        return cp

    def get(self, path):
        """精确匹配"""
        cp = self.data
        for c in path:
            if c in cp:
                cp = cp[c]
            else:
                return None
        if "_data" not in cp:
            return None
        else:
            return cp["_data"]

    def get_best_match(self, path):
        """最长匹配"""
        best_match = None
        best_path = None
        cp = self.data
        for c in path:
            if "_data" in cp:
                best_match = cp["_data"]
                best_path = cp["_path"]
            if c in cp:
                cp = cp[c]
            else:
                break
        if "_data" in cp:
            best_match = cp["_data"]
            best_path = cp["_path"]
        return best_path, best_match

    def delete(self, path):
        """删除索引。

        数据已删除，但没有清理遗留结构。
        """
        if path in self.paths:
            del self.paths[path]
        cp = self.data
        for c in path:
            if c in cp:
                cp = cp[c]
            else:
                return False
        if "_data" not in cp:
            return False
        else:
            del cp["_data"]
            return True

    def get_all_paths(self):
        paths = list(self.paths.keys())
        paths.sort()
        return paths


class BinaryTreeNode(object):
    def __init__(self, data):
        self.data = data
        self.left_node = None
        self.right_node = None

    def set_left_node_data(self, data):
        if self.left_node:
            self.left_node.data = data
        else:
            self.left_node = BinaryTreeNode(data)
        return self.left_node

    def set_left_node(self, node):
        self.left_node = node
        return self.left_node

    def set_right_node_data(self, data):
        if self.right_node:
            self.right_node.data = data
        else:
            self.right_node = BinaryTreeNode(data)
        return self.right_node

    def set_right_node(self, node):
        self.right_node = node
        return self.right_node
