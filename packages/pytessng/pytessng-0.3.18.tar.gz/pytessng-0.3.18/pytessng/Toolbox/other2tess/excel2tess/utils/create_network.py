
from .functions import get_coo_list
try:
    from .....Tessng.MyMenu import ProgressDialog as pgd
except:
    class pgd: progress = lambda values, text="": values


def create_network(netiface, links_data, other_data):
    # 记录属性，如：路网来源
    netiface.setNetAttrs("Excel Network", otherAttrsJson=other_data)

    # 创建路段
    for link_id, link_data in pgd.progress(links_data.items(), '路段创建中（2/2）'):
        linkName = link_data["link_name"]
        linkCount = link_data["link_count"]
        linkPoint = get_coo_list(link_data["link_points"])

        # 创建路段及车道
        try:
            try:
                link_obj = netiface.createLink(linkPoint, linkCount)
            except:
                link_obj = netiface.createLink3D(linkPoint, linkCount)
        except Exception as e:
            link_obj = None
            print(str(e))

        # 判断路段是否存在，并设置属性
        if link_obj:
            link_obj.setName(f"{link_id}-{linkName}")
