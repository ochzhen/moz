from moz.models import MOZDocument


def get_all_documents_order_by_title(desc=False):
    if desc:
        return MOZDocument.objects.order_by('-title')
    return MOZDocument.objects.order_by('title')


def get_number_of_documents_order_by_title(limit, desc=False):
    if desc:
        return MOZDocument.objects.order_by('-title')[:limit]
    return MOZDocument.objects.order_by('title')[:limit]


def get_document_by_id(ID):
    return MOZDocument.objects.get(id=ID)
