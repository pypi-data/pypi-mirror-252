from __future__ import annotations

import io

from anyio import create_task_group
from ormspace import model as md
from ormspace.model import getmodel
from starlette.requests import Request
from typing_extensions import Self

from hx_markup import Element


class SpaceBase:

    
    async def display(self):
        with io.StringIO() as f:
            container: Element = Element('div', id=getattr(self, 'tablekey'))
            container.children.append(Element('h3', children=str(self)))
            container.children.append(Element('ul', '.nav', children=[Element('li','.nav-item', children=f'{k}: {v}') for k, v in dict(self).items() if v]))
            f.write(str(container))
            return f.getvalue()
        
    async def heading(self, tag: str, *args, **kwargs):
        with io.StringIO() as f:
            kwargs['children'] = str(self)
            f.write(str(Element(tag, *args, **kwargs)))
            return f.getvalue()
        

class SpaceModel(SpaceBase, md.Model):
    pass
    
class SpaceSearchModel(SpaceBase, md.SearchModel):
    pass