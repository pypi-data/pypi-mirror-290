from ..unas_api.unas import CategoriesAPI

category = CategoriesAPI("cfcdf8a7109a30971415ff7f026becdc50dbebbd").get_category("212349")
print(category)