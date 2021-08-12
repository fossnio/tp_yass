import logging

from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound

from tp_yass.dal import DAL
from tp_yass.enum import ThemeConfigCustomType
from tp_yass.views.helper.file import get_project_abspath
from tp_yass.forms.backend.theme_config import ThemeConfigGeneralForm, ThemeConfigBannersEditForm

logger = logging.getLogger(__name__)


@view_config(route_name='backend_theme_config_list',
             renderer='tp_yass:themes/default/backend/theme_config_list.jinja2',
             permission='view')
def theme_config_list_view(request):
    return {'theme_config_list': DAL.get_theme_config_list()}


@view_defaults(route_name='backend_theme_config_general_edit',
               renderer='tp_yass:themes/default/backend/theme_config_general_edit.jinja2',
               permission='edit')
class ThemeConfigGeneralEditView:
    """處理樣板的設定值內容"""

    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def get_view(self):
        theme_name = self.request.matchdict['theme_name']
        theme_config = DAL.get_theme_config(theme_name)
        form = ThemeConfigGeneralForm()
        form.custom_css.default = theme_config['settings']['custom_css']['value']
        form.custom_css_visible.default = theme_config['settings']['custom_css']['visible']
        form.custom_js.default = theme_config['settings']['custom_js']['value']
        form.custom_js_visible.default = theme_config['settings']['custom_js']['visible']
        form.process()
        for each_custom_setting in theme_config['settings']['custom']['value']:
            form.custom.append_entry(each_custom_setting)
        return {'theme_config': theme_config,
                'form': form}

    @view_config(request_method='POST')
    def post_view(self):
        theme_name = self.request.matchdict['theme_name']
        theme_config = DAL.get_theme_config(theme_name)
        form = ThemeConfigGeneralForm(self.request.POST)
        if form.validate():
            theme_config['settings']['custom_css']['value'] = form.custom_css.data
            theme_config['settings']['custom_css']['visible'] = form.custom_css_visible.data
            theme_config['settings']['custom_js']['value'] = form.custom_js.data
            theme_config['settings']['custom_js']['visible'] = form.custom_js_visible.data
            custom_value = form.custom.data
            try:
                for each_setting in custom_value:
                    if each_setting['type'] == ThemeConfigCustomType.BOOLEAN:
                        if each_setting['value'].upper() in ('FALSE', '0', ''):
                            each_setting['value'] = False
                        else:
                            each_setting['value'] = True
                    elif each_setting['type'] == ThemeConfigCustomType.INTEGER:
                        each_setting['value'] = int(each_setting['value'])
                theme_config['settings']['custom']['value'] = custom_value
            except ValueError as e:
                pass
            DAL.update_theme_config(theme_config)
            self.request.cache.delete_theme_config()
            return HTTPFound(location=self.request.route_url('backend_theme_config_list'))
        return {'theme_config': theme_config,
                'form': form}


@view_defaults(route_name='backend_theme_config_banners_edit',
               renderer='tp_yass:themes/default/backend/theme_config_banners_edit.jinja2',
               permission='edit')
class ThemeConfigBannersEditView:
    """用來處理橫幅的列表與增刪"""

    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def get_view(self):
        theme_name = self.request.matchdict['theme_name']
        theme_config = DAL.get_theme_config(theme_name)
        form = ThemeConfigBannersEditForm()
        banners_dict = self._get_banners(theme_name)
        for each_banner in banners_dict:
            if each_banner in theme_config['settings']['banners']['value']:
                each_banner_is_visible = True
            else:
                each_banner_is_visible = False
            form.banners.append_entry({'name': each_banner, 'is_visible': each_banner_is_visible})
        return {'theme_config': theme_config, 'form': form, 'banners_dict': banners_dict}

    @view_config(request_method='POST')
    def post_view(self):
        theme_name = self.request.matchdict['theme_name']
        theme_config = DAL.get_theme_config(theme_name)
        form = ThemeConfigBannersEditForm(self.request.POST)
        banners_dict = self._get_banners(theme_name)
        if form.validate():
            theme_config_changed = False
            for each_banner in form.banners:
                if each_banner.data['name'] in banners_dict:
                    if each_banner.data['is_visible'] and (each_banner.data['name'] not in theme_config['settings']['banners']['value']):
                        theme_config['settings']['banners']['value'].append(each_banner.data['name'])
                        theme_config_changed = True
                    elif (not each_banner.data['is_visible']) and (each_banner.data['name'] in theme_config['settings']['banners']['value']):
                        theme_config['settings']['banners']['value'].remove(each_banner.data['name'])
                        theme_config_changed = True
            if theme_config_changed:
                DAL.update_theme_config(theme_config)
                self.request.cache.delete_theme_config()
            return HTTPFound(location=self.request.route_url('backend_theme_config_list'))
        else:
            return {'theme_config': theme_config, 'form': form, 'banners_dict': banners_dict}

    def _get_banners(self, theme_name):
        """回傳一個由 banner 檔名與 url 組成的 dict"""
        banners = {}
        for each_banner in (get_project_abspath() / 'uploads/themes' / theme_name / 'banners').glob('*'):
            if each_banner.name.startswith('.'):
                continue
            banners[each_banner.name] = \
                self.request.static_url(f'tp_yass:uploads/themes/{theme_name}/banners/{each_banner.name}')
        return banners
