from django import template

register = template.Library()


def refresh_url_pag(val, next_p):
    print("filter_tag")
    print(val)
    print(next_p)
    next_page = "page="+str(next_p)
    st_rem = val.find("page=")
    if st_rem != -1:
        end_rem = val.find("&", st_rem+5)
        if end_rem != -1:
            print(st_rem)
            print(end_rem)
            val = val.replace(val[st_rem:end_rem], next_page)
            print(val)
        else:
            val = val.replace(val[st_rem:], next_page)
    elif val.find("?") != -1:
        val = val+"&"+next_page
    else:
        val = val+"?"+next_page
    return val


register.filter('refresh_url_pag', refresh_url_pag)
