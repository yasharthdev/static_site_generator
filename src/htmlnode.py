class HTMLNode:
    def __init__(
            self, tag: str | None = None,
            value: str | None = None,
            children: list[HTMLNode] | None = None,
            props: dict[str, str] | None = None
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError(
            "Subclass must implement to_html method"
        )
    
    def props_to_html(self) -> str:
        result = ""
        if not self.props:
            return result
        for key, value in self.props.items():
            # HTML attributes must be separated by a space
            result += f' {key}="{value}"'
        
        return result
    
    def __repr__(self) -> str:
        return (
            f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children},"
            f" props={self.props})"
        )

class LeafNode(HTMLNode):
    def __init__(
            self, tag: str | None, value: str, props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, value, children=None, props=props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self) -> str:
        return (
            f"LeafNode(tag: {self.tag}, value: {self.value}, props: {self.props})"
        )