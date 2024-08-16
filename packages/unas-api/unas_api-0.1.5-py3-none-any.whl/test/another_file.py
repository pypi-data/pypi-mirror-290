from ..unas_api.unas import UnasAPIBase, Product

unas_client = UnasAPIBase("cfcdf8a7109a30971415ff7f026becdc50dbebbd")
product = unas_client.get_product("CS-F2811", "full")
product.categories = [
    Product.Category("base", "684112", "UTOLSÓ DARABOK"),
    *product.categories,
]
product.remove_category(684112)
product.categories[0].type = "base"
product.action = "modify"
resp = unas_client.set_product(product)
