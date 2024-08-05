import pandas as pd
from datasets import load_dataset

# Veri setini yükle
dataset = load_dataset("WhiteAngelss/magaza-urun-listesi-with-links", split='train')

# Veriyi bir DataFrame'e dönüştür
df = pd.DataFrame(dataset)

# Veriyi 'Mağaza;Ürün;Link' sütunlarına ayır
df = df['Mağaza;Ürün;Link'].str.split(';', expand=True)
df.columns = ['Mağaza', 'Ürün', 'Link']

def find_stores_with_products(products, df):
    # Ürünler ile mağazaları ve linkleri gruplama
    store_products_links = df.groupby('Mağaza').agg(
        {'Ürün': lambda x: list(x), 'Link': lambda x: list(x)}
    ).reset_index()

    # Mağazalar ve ürünlerin linklerini sözlüğe dönüştürme
    store_products_dict = store_products_links.set_index('Mağaza').to_dict('index')

    # Kullanıcının seçtiği ürünlerin bulunduğu mağazaları ve linkleri filtreleme
    matching_stores = {
        store: {prod: store_products_dict[store]['Link'][idx] for idx, prod in enumerate(store_products_dict[store]['Ürün']) if prod in products}
        for store in store_products_dict
        if all(prod in store_products_dict[store]['Ürün'] for prod in products)
    }
    return matching_stores

# Kullanıcıdan ürünleri al
user_input = input("Lütfen almak istediğiniz ürünleri virgülle ayırarak girin: ")
user_products = [product.strip() for product in user_input.split(',')]

# Mağazaları ve linkleri bul
matching_stores = find_stores_with_products(user_products, df)

if matching_stores:
    print("Bu ürünleri bulabileceğiniz mağazalar ve linkler:")
    for store, products in matching_stores.items():
        print(f"Mağaza: {store}")
        for product, link in products.items():
            print(f"  Ürün: {product} - Link: {link}")
else:
    print("Bu ürünleri bulabileceğiniz mağaza bulunamadı.")
