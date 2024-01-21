from test_pdm import PdmTest, Identical

pdm = PdmTest('PdmTest', '0.1.0')
pdm.details()

value = 'Hola, cual es tu nombre: pdm ok'
model = 'Hola, cual es tu nombre: {name}'

comprobate = Identical(model, value)
data = comprobate.getData()
print(data, comprobate.getValidate())