from bs4 import BeautifulSoup
import requests
import csv
from PIL import Image

def findeAngebote():
    #find and save deals as csv file
    csv_file=open('Angebote.csv','w',newline="")
    csv_writer=csv.writer(csv_file)
    csv_writer.writerow(['Name der Produkt','Preis','Preis vor Rabatt','Rabatt%','Bild','Supermarkt'])
    source=requests.get('https://www.penny.de/angebote').text
    soup=BeautifulSoup(source,'lxml')
    for product in soup.find_all('li',class_=['tile-list__item','tile-list__item--highlight']):
        try:
            product_image_code=product.find('div',class_='offer-tile__image-container')
            product_image=product_image_code.find('img')['src']
            product_title=product.find('a',class_='tile__link--cover ellipsis').text
            price_code=product.find('div',class_='bubble__wrap')
            price=price_code.find('span',class_='ellipsis').text
            price2=''
            if ('value' in str(price_code)) or (not price.replace('.','').isnumeric()):
                probstr=str(price_code).split('\n')[-2]
                num=''
                for l in probstr:
                    if l.isdigit() or l in '.,':
                        num+=l
                price=num
                if 'value' in str(price_code):
                    probstr2=str(price_code).split('\n')[-4]
                    num2=''
                    for l2 in probstr2:
                        if l2.isdigit() or l2 in '.,':
                            num2+=l2
                    price2=num2

            discount=product.find('div',class_='offer-tile__badges badge__container').text
            #removes extra symbols from the name and price
            product_title=product_title.replace(r'*','')
            product_title=product_title.replace(r',','')
            product_title=product_title.replace(r'"','')
            product_title=product_title.replace(r'­','')
            product_title=product_title.replace('-',' ')
            price=price.replace(r'*','')
            price=price.replace(r'"','')
            discount=discount.replace(r'*','')
            discount=discount.replace(r'"','')
            product_image=product_image.replace(r'*','')
            product_image=product_image.replace(r'"','')
            if product_title[0]==' ':
                product_title=product_title[1:]
            csv_writer.writerow([product_title,price,price2,discount,product_image,'Penny'])
        except Exception as a:
            discount='-0%'
    csv_file.close()


def findeProdukt(product_to_look_for,show_pic=False,filtprice=0):
    #find and show matching products
    if product_to_look_for=='':
        return None
    i=0
    show=True
    with open('Angebote.csv','r') as f:
        f_reader=csv.reader(f)
        for line in f_reader:
            if product_to_look_for.lower() in line[0].lower():
                i+=1
                finded_product=line[0]
                finded_price=line[1]
                finded_price2=line[2]
                finded_discount=line[3]
                finded_img=line[4]
                finded_shop=line[5]
                if float(filtprice)>0:
                    show=False
                    if float(finded_price)<=float(filtprice):
                        show=True
                if show:
                    print(f'{i}) Markt:',finded_shop)
                    print('Produkt:',finded_product)
                    print('Preis:',finded_price,'€')
                    print('Preis vor Rabatt:',f'{finded_price2}€' if finded_price2!='' else 'unbestimmt')
                    print('Info:',finded_discount.strip() if len(finded_discount.strip())>0 else 'keine')
                    print('Bild:',finded_img)
                    print()
                    if show_pic:
                        im = Image.open(requests.get(finded_img, stream=True).raw)
                        im.show()
    if i==0:
        print('lieder nichts gefunden')


findeAngebote()
findeProdukt('käse',True,2)
