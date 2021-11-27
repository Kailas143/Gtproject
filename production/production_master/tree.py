from . models import sub_process
from . serializers import Subprocess_serializer

def recursive_node_to_dict(node,pk):
    node.pk=pk
    subp=sub_process.objects.filter(mainprocess__id=node.pk)
    subser=Subprocess_serializer(subp,many=True)
    result = {
        'id': node.pk,
        'name': node.process_name,
        'subprocess':subser.data
    }
    print(node.get_children(),'cc')
    children = [recursive_node_to_dict(c) for c in node.get_children()]
    print(children,'chiillldrrr')
    if children:
        result['children'] = children
    print(result,'resss')
    return result