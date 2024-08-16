import requests as rq
from xml.etree import ElementTree
from typing import List, Optional
from datetime import datetime

class UnasAPIBase:
    def __init__(self, api_key):
        self.api_key = api_key
        self.token = None

    def get_unas_token(self):
        token_payload = f'<?xml version="1.0" encoding="UTF-8" ?><Params><ApiKey>{self.api_key}</ApiKey></Params>'
        token_request = rq.get("https://api.unas.eu/shop/login", data=token_payload)
        token_tree = ElementTree.fromstring(token_request.content)
        if token_tree[0].tag == "Token":
            self.token = token_tree[0].text
        return self.token

    def make_request(self, endpoint, payload, method='GET'):
        if not self.token:
            self.get_unas_token()
        headers = {"Authorization": f"Bearer {self.token}"}
        if method == 'GET':
            response = rq.get("https://api.unas.eu/shop/" +endpoint, headers=headers, data=payload)
        elif method == 'POST':
            response = rq.post(endpoint, headers=headers, data=payload)
        return ElementTree.fromstring(response.content)

    def get_unas_feed_url(self, lang="hu"):
        url_payload = f'<?xml version="1.0" encoding="UTF-8" ?><Params><Format>xlsx</Format><Lang>{lang}</Lang></Params>'
        url_request = self.make_request("getProductDB", url_payload)
        url_tree = ElementTree.fromstring(url_request.content)
        url = url_tree[0].text
        return url


class Display:
    def __init__(self, page: str, menu: str):
        self.page = page
        self.menu = menu

class PublicInterval:
    def __init__(self, start: str, end: str):
        self.start = start
        self.end = end

class NotVisibleInLanguage:
    def __init__(self, language: str):
        self.language = language

class PageLayout:
    def __init__(self, category_list: int, product_list: int):
        self.category_list = category_list
        self.product_list = product_list

class Parent:
    def __init__(self, id: int, tree: str):
        self.id = id
        self.tree = tree

class Products:
    def __init__(self, all: int, new: int):
        self.all = all
        self.new = new

class Texts:
    def __init__(self, top: str, bottom: str, menu: str):
        self.top = top
        self.bottom = bottom
        self.menu = menu

class Meta:
    def __init__(self, keywords: str, description: str, title: str, robots: str):
        self.keywords = keywords
        self.description = description
        self.title = title
        self.robots = robots

class AutomaticMeta:
    def __init__(self, keywords: str, description: str, title: str):
        self.keywords = keywords
        self.description = description
        self.title = title

class Image:
    def __init__(self, url: str, og: str):
        self.url = url
        self.og = og

class Tags:
    def __init__(self, tag: str):
        self.tag = tag

class HistoryEvent:
    def __init__(self, action: str, time: datetime, id: int):
        self.action = action
        self.time = time
        self.id = id

class History:
    def __init__(self, events: List[HistoryEvent]):
        self.events = events

class Category:
    def __init__(self, action: str, state: Optional[str], id: int, name: str, url: Optional[str], sef_url: str, alt_url: Optional[str], alt_url_blank: Optional[str], display: Display, disable_filter: Optional[str], public_interval: Optional[PublicInterval], not_visible_in_language: Optional[NotVisibleInLanguage], page_layout: Optional[PageLayout], parent: Optional[Parent], order: Optional[int], products: Optional[Products], texts: Optional[Texts], meta: Optional[Meta], automatic_meta: Optional[AutomaticMeta], create_time: Optional[int], last_mod_time: Optional[int], image: Optional[Image], tags: Optional[Tags], history: Optional[History]):
        self.action = action
        self.state = state
        self.id = id
        self.name = name
        self.url = url
        self.sef_url = sef_url
        self.alt_url = alt_url
        self.alt_url_blank = alt_url_blank
        self.display = display
        self.disable_filter = disable_filter
        self.public_interval = public_interval
        self.not_visible_in_language = not_visible_in_language
        self.page_layout = page_layout
        self.parent = parent
        self.order = order
        self.products = products
        self.texts = texts
        self.meta = meta
        self.automatic_meta = automatic_meta
        self.create_time = create_time
        self.last_mod_time = last_mod_time
        self.image = image
        self.tags = tags
        self.history = history

    def __repr__(self):
        return f"<Category(action={self.action}, state={self.state}, id={self.id}, name={self.name}, url={self.url}, sef_url={self.sef_url}, alt_url={self.alt_url}, alt_url_blank={self.alt_url_blank}, display={self.display}, disable_filter={self.disable_filter}, public_interval={self.public_interval}, not_visible_in_language={self.not_visible_in_language}, page_layout={self.page_layout}, parent={self.parent}, order={self.order}, products={self.products}, texts={self.texts}, meta={self.meta}, automatic_meta={self.automatic_meta}, create_time={self.create_time}, last_mod_time={self.last_mod_time}, image={self.image}, tags={self.tags}, history={self.history})>"

class CategoriesAPI(UnasAPIBase):
    def get_category(self, category_id: int) -> Category:
        payload = f'<?xml version="1.0" encoding="UTF-8" ?><Params><Id>{category_id}</Id></Params>'
        response = self.make_request("getCategory", payload)
        category_tree = response.find(".//Category")
        
        # Parse the XML response into the Category data structure
        category = Category(
            action=None,
            state=category_tree.findtext('State'),
            id=int(category_tree.findtext('Id')),
            name=category_tree.findtext('Name'),
            url=category_tree.findtext('Url'),
            sef_url=category_tree.findtext('SefUrl'),
            alt_url=category_tree.findtext('AltUrl'),
            alt_url_blank=category_tree.findtext('AltUrlBlank'),
            display=Display(
                page=category_tree.findtext('Display/Page'),
                menu=category_tree.findtext('Display/Menu')
            ),
            disable_filter=category_tree.findtext('DisableFilter'),
            public_interval=PublicInterval(
                start=category_tree.findtext('PublicInterval/Start'),
                end=category_tree.findtext('PublicInterval/End')
            ) if category_tree.find('PublicInterval') is not None else None,
            not_visible_in_language=NotVisibleInLanguage(
                language=category_tree.findtext('NotVisibleInLanguage/Language')
            ) if category_tree.find('NotVisibleInLanguage') is not None else None,
            page_layout=PageLayout(
                category_list=int(category_tree.findtext('PageLayout/CategoryList')) if category_tree.findtext('PageLayout/CategoryList') is not None else None,
                product_list=int(category_tree.findtext('PageLayout/ProductList')) if category_tree.findtext('PageLayout/ProductList') is not None else None
            ) if category_tree.find('PageLayout') is not None else None,
            parent=Parent(
                id=int(category_tree.findtext('Parent/Id')) if category_tree.findtext('Parent/Id') is not None else None,
                tree=category_tree.findtext('Parent/Tree')
            ) if category_tree.find('Parent') is not None else None,
            order=int(category_tree.findtext('Order')) if category_tree.findtext('Order') is not None else None,
            products=Products(
                all=int(category_tree.findtext('Products/All')) if category_tree.findtext('Products/All') is not None else None,
                new=int(category_tree.findtext('Products/New')) if category_tree.findtext('Products/New') is not None else None
            ) if category_tree.find('Products') is not None else None,
            texts=Texts(
                top=category_tree.findtext('Texts/Top'),
                bottom=category_tree.findtext('Texts/Bottom'),
                menu=category_tree.findtext('Texts/Menu')
            ) if category_tree.find('Texts') is not None else None,
            meta=Meta(
                keywords=category_tree.findtext('Meta/Keywords'),
                description=category_tree.findtext('Meta/Description'),
                title=category_tree.findtext('Meta/Title'),
                robots=category_tree.findtext('Meta/Robots')
            ) if category_tree.find('Meta') is not None else None,
            automatic_meta=AutomaticMeta(
                keywords=category_tree.findtext('AutomaticMeta/Keywords'),
                description=category_tree.findtext('AutomaticMeta/Description'),
                title=category_tree.findtext('AutomaticMeta/Title')
            ) if category_tree.find('AutomaticMeta') is not None else None,
            create_time=int(category_tree.findtext('CreateTime')) if category_tree.findtext('CreateTime') is not None else None,
            last_mod_time=int(category_tree.findtext('LastModTime')) if category_tree.findtext('LastModTime') is not None else None,
            image=Image(
                url=category_tree.findtext('Image/Url'),
                og=category_tree.findtext('Image/OG')
            ) if category_tree.find('Image') is not None else None,
            tags=Tags(
                tag=category_tree.findtext('Tags/Tag')
            ) if category_tree.find('Tags') is not None else None,
            history=History(
                events=[
                    HistoryEvent(
                        action=event.findtext('Action'),
                        time=datetime.fromtimestamp(int(event.findtext('Time'))),
                        id=int(event.findtext('Id'))
                    ) for event in category_tree.findall('History/Event')
                ]
            ) if category_tree.find('History') is not None else None
        )
        
        return category

    def set_category(self, category: Category):
        payload = f'''<?xml version="1.0" encoding="UTF-8" ?>
        <Params>
            <Action>{category.action}</Action>
            <Id>{category.id}</Id>
            <Name>{category.name}</Name>
            <SefUrl>{category.sef_url}</SefUrl>
            <AltUrl>{category.alt_url}</AltUrl>
            <AltUrlBlank>{category.alt_url_blank}</AltUrlBlank>
            <Display>
                <Page>{category.display.page}</Page>
                <Menu>{category.display.menu}</Menu>
            </Display>
            <DisableFilter>{category.disable_filter}</DisableFilter>
            <PublicInterval>
                <Start>{category.public_interval.start}</Start>
                <End>{category.public_interval.end}</End>
            </PublicInterval>
            <NotVisibleInLanguage>
                <Language>{category.not_visible_in_language.language}</Language>
            </NotVisibleInLanguage>
            <PageLayout>
                <CategoryList>{category.page_layout.category_list}</CategoryList>
                <ProductList>{category.page_layout.product_list}</ProductList>
            </PageLayout>
            <Parent>
                <Id>{category.parent.id}</Id>
                <Tree>{category.parent.tree}</Tree>
            </Parent>
            <Order>{category.order}</Order>
            <Texts>
                <Top>{category.texts.top}</Top>
                <Bottom>{category.texts.bottom}</Bottom>
                <Menu>{category.texts.menu}</Menu>
            </Texts>
            <Meta>
                <Keywords>{category.meta.keywords}</Keywords>
                <Description>{category.meta.description}</Description>
                <Title>{category.meta.title}</Title>
                <Robots>{category.meta.robots}</Robots>
            </Meta>
            <AutomaticMeta>
                <Keywords>{category.automatic_meta.keywords}</Keywords>
                <Description>{category.automatic_meta.description}</Description>
                <Title>{category.automatic_meta.title}</Title>
            </AutomaticMeta>
            <Image>
                <OG>{category.image.og}</OG>
            </Image>
            <Tags>
                <Tag>{category.tags.tag}</Tag>
            </Tags>
        </Params>'''
        
        response = self.make_request("setCategory", payload)
        return response