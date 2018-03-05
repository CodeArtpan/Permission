import re
import os
from django.template import Library
from django.conf import settings
from django.utils.safestring import mark_safe
register = Library()


def process_menu_data(request):
    """
    生成菜单相关数据
    :param request:
    :return:
    """
    menu_permission_list = request.session.get(settings.SESSION_PERMISSION_MENU_URL_KEY)

    menu_list = menu_permission_list[settings.ALL_MENU_KEY]
    permission_list = menu_permission_list[settings.PERMISSION_URL_KEY]

    all_menu_dict = {}
    for item in menu_list:
        item['children'] = []
        item['status'] = False
        item['open'] = False
        all_menu_dict[item['id']] = item

    for per in permission_list:
        per['status'] = True
        pattern = settings.URL_REGEX.format(per['url'])
        if re.match(pattern, request.path_info):
            per['open'] = True
        else:
            per['open'] = False

        all_menu_dict[per['menu_id']]['children'].append(per)

        pid = per['menu_id']
        while pid:
            all_menu_dict[pid]['status'] = True
            pid = all_menu_dict[pid]['parent_id']

        if per['open']:
            ppid = per['menu_id']
            while ppid:
                all_menu_dict[ppid]['open'] = True
                ppid = all_menu_dict[ppid]['parent_id']

    result = []
    for k, v in all_menu_dict.items():
        if not v.get('parent_id'):
            result.append(v)
        else:
            parent_id = v['parent_id']
            all_menu_dict[parent_id]['children'].append(v)

    return result


def process_menu_html(menu_list):
    tpl1 = """
            <div class='rbac-menu-item'>
                <div class='rbac-menu-header'>{0}</div>
                <div class='rbac-menu-body {2}'>{1}</div>
            </div>
        """
    tpl2 = """
            <a href='{0}' class='{1}'>{2}</a>
        """

    html = ""

    for item in menu_list:
        if not item['status']:
            continue
        if item.get('url'):
            # 权限
            html += tpl2.format(item['url'], "rbac-active" if item['open'] else "",item['title'])
        else:
            # 菜单
            html += tpl1.format(item['caption'],process_menu_html(item['children']), "" if item['open'] else "rbac-hide")

    return html

@register.simple_tag
def rbac_menus(request):
    # 数据库取到菜单相关数据
    result = process_menu_data(request)
    # 生成HTML
    html = process_menu_html(result)
    return mark_safe(html)

@register.simple_tag
def rbac_css():
    file_path = os.path.join('rbac', 'theme', 'rbac.css')
    if os.path.exists(file_path):
        return mark_safe(open(file_path, 'r', encoding='utf-8').read())
    else:
        raise Exception('rbac主题CSS文件不存在')


@register.simple_tag
def rbac_js():
    file_path = os.path.join('rbac', 'theme', 'rbac.js')
    if os.path.exists(file_path):
        return mark_safe(open(file_path, 'r', encoding='utf-8').read())
    else:
        raise Exception('rbac主题JavaScript文件不存在')