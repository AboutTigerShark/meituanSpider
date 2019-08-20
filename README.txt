这是之前写的关于美团的爬虫,由于网页端的限制所以爬取的是它的http://i.meituan.com/,美团的店铺详情信息是"http://meishi.meituan.com/i/poi/170617865?ct_poi=056104330308190515238209188158399405961_a170617865_c0_e5447332902906651424"
类似这种地址,其中ct_poi参数是店铺参数,170617865是地区id

meituan.py:主要是爬取url参数ct_poi用于构建url

areaid.py:主要是爬取地区id,同样用于构建url

craw_meituan_detail.py:主要爬取详情页内容

另外美团对同一IP的访问限制很严格,所以需要有很多代理IP

