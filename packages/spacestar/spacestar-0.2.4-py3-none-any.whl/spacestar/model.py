from __future__ import annotations


from hx_markup.element import NodeText
from markdown import markdown
from ormspace import model as md


from hx_markup import Element
from typing_extensions import Self


class SpaceModel(md.Model):
    
    def element_detail(self) -> Element:
        container: Element = Element('div', id=self.tablekey)
        container.children.append(Element('h3', children=str(self)))
        for k, v in self.model_fields.items():
            if value:= getattr(self, k):
                container.children.append(f"""
                ##### {v.title or k}
                {markdown(value)}
                """)
        # container.children.append(Element('ul', '.list-group', children=[Element('li','.list-group-item', children=f'{markdown(f"""# {k}""")}') for k, v in dict(self).items() if v]))
        return container
    
    def element_list_group_item(self) -> Element:
        return Element('li', '.list-group-item', NodeText(str(self)))
    
    def element_list_group_item_action(self, href: str):
        return Element('li', '.list-group-item', Element('a', '.list-group-item-action', href=href, children=str(self)))

    def element_list_group_item_htmx_action(self, href: str, target: str, indicator: str = '#bars'):
        return Element('li', '.list-group-item', Element('a', '.list-group-item-action', htmx={
                'target': target,
                'get': href,
                'indicator': indicator
        }, children=str(self)))
    
    @classmethod
    def element_list_group(cls, instances: list[Self]):
        return Element('li', '.list-group', children=[
                item.element_list_group_item() for item in instances
        ])
    


    
class SpaceSearchModel(SpaceModel, md.SearchModel):
    pass