from xl_word.sheet import Sheet
from pathlib import Path
import os 


class Document(Sheet):
    """Word表单对象"""
    def __init__(self, tpl_path, component_folder=None, xml_folder=None):
        super().__init__(tpl_path, xml_folder)
        self.component_folder = component_folder


    def render(self, data):
        template_xml = '($ for item in data $)'
        component_files = [
            f for f in Path(self.component_folder).rglob('*.xml')
        ]
        for index, filepath in enumerate(component_files):
            component_type = filepath.stem
            with open(filepath, 'r', encoding='utf-8') as file:
                component_content = file.read()
                condition = 'if' if index == 0 else 'elif'
                template_xml += f"($ {condition} item['component']=='{component_type}' $){component_content}"
  
        template_xml += '($ endif $)($ endfor $)'
        document_xml = self.render_xml('document', dict(document=template_xml)).decode()
        syntax_map = {
            r'($': '{%',
            r'$)': '%}',
            r'((': '{{',
            r'))': '}}',
        }
        for k, v in syntax_map.items():
            document_xml = document_xml.replace(k, v)
        self['word/document.xml'] = document_xml.encode('utf-8')
        for item in data['data']: 
            if item['component'] == 'image':
                image_path = Path(item['content']['url'])
                self['word/media/1.png'] = image_path.read_bytes()
                relation_id = self.append_relation('document.xml', 'image', 'media/1.png')
                item['content']['relation_id'] = relation_id
        super().render(data)

