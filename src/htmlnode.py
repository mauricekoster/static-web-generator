from typing import List


class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children: List["HTMLNode"] | None = None, props: dict | None = None):
        self.tag: str | None= tag
        self.value: str | None = value
        self.children: List["HTMLNode"] | None = children
        self.props: dict | None = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        retval = ""
        if self.props:
            for k, v in self.props.items():
                retval += f' {k}="{v}"'
        return retval

    def __repr__(self):
        return f"<HTMLNode tag={self.tag} value={self.value} #children={len(self.children)} props={self.props_to_html()}>"
    
    

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str | None, props: dict | None = None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Empty value")
        
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return f"<LeafNode tag={self.tag} value={self.value} props={self.props_to_html()}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag: str | None, children: List["HTMLNode"] | None, props: dict | None = None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Empty tag")
        
        if self.children is None or len(self.children) == 0:
            raise ValueError("Empty children")
        
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
            
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
        
    def __repr__(self):
        return f"<LeafNode tag={self.tag} value={self.value} props={self.props_to_html()}>"
    
