from __future__ import annotations

import io

from anyio import create_task_group
from hx_markup.element import NodeText
from ormspace import model as md
from ormspace.model import getmodel
from starlette.requests import Request
from typing_extensions import Self

from hx_markup import Element


class SpaceModel(md.Model):
    
    def element_detail(self) -> Element:
        container: Element = Element('div', id=getattr(self, 'tablekey'))
        container.children.append(Element('h3', children=str(self)))
        container.children.append(Element('ul', '.list-group', children=[Element('li','.list-group-item', children=f'{k}: {v}') for k, v in dict(self).items() if v]))
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


    
class SpaceSearchModel(SpaceModel, md.SearchModel):
    pass