import os
import re

class Contrato:
  def __init__(self, numeroContrato, nomeConcessionaria):
    self.numero = numeroContrato
    self.nomeConcessionaria = nomeConcessionaria

#cria os grupos passando a lista de contratos
def makeGroup(contratos):
  groups = ['VO Saude Seg Obra', 'VO Almoxarifado Obra', 'VO Administrativo Obra', 'VO Planejamento Obra']
  for contrato in contratos:
    for group in groups:
      comando = f'dsadd group "cn={contrato.numero} - {group}, ou={contrato.numero} - {contrato.nomeConcessionaria}, ou={contrato[0].numero} - {contrato[-1].numero}, ou=01 - Contratos, ou=Operacional (Contratos), ou=Grupos de Permissao, ou=VISION OU, dc=visionsistemas, dc=com, dc=br"'
      os.system(comando)
      print(f'Grupo criado: {contrato.numero} - {group}')

#cria as instancias de contratos em determinado range. Exemplo: 1000 - 1099
def makeContratos(range1, range2):
  pastas = os.listdir('.')
  contratos = []
  for pasta in pastas:
    if contratoValidator(pasta):
      numeroContrato = pasta[0:5]
      nomeConcessionaria = pasta[7:len(pasta)+1]
      contrato  = Contrato(numeroContrato, nomeConcessionaria)
      if int(numeroContrato) >= range1 and int(numeroContrato) <= range2:
        contratos.append(contrato)
        print(f'Contrato gerado: {contrato.numero} - {contrato.nomeConcessionaria}')
      
  return contratos


#testa se os grupos estão sendo criados
def testMakeGroup(numeroContrato):
  contratos = makeContratos(numeroContrato, numeroContrato)
  makeGroup(contratos)

#adiciona as permissões de determinado range
def grantPermissions(range1, range2):
  newGroups = ['VO Saude Seg Obra', 'VO Almoxarifado Obra', 'VO Administrativo Obra', 'VO Planejamento Obra']
  existingGroups = ["VO - Equipe de Apoio", "VO - Amoxarifado de Apoio"]
  contratos = makeContratos(range1, range2)
  folderpath = os.getcwd()
  for contrato in contratos:
    folderpath += f'\{contrato.numero} - {contrato.nomeConcessionaria}'
    for i in range(len(newGroups)):
      comando  = f'cmd /c "icacls {folderpath} /inheritance:e /grant:r "visionsistemas\{contrato.numero} - {newGroups[i]}:(OI)(CI)M"'
      os.system(comando)
      print(f'Permissão Garantida: {contrato.numero} - {newGroups[i]}')
    for j in range(len(existingGroups)):
      comando = f'cmd /c "icacls {folderpath} /inheritance:e /grant:r "visionsistemas\{existingGroups[j]}:(OI)(CI)M"'
      os.system(comando)
      print(f'Permissão Garantida: {contrato.numero} - {existingGroups[j]}')

def contratoValidator(contrato):
  if re.fullmatch('[0-9]{4} - [A-zÀ-ÿ]*', contrato):
    return True
  return False

def main(range1, range2):
  while True:
    choice = int(input('1 - Fazer os grupos\n2 - Criar as pastas e dar permissão\n3 - Testar a criação de grupos\n4 - Sair\n-> '))
    if choice == 1:
      contratos = makeContratos(range1, range2)
      makeGroup(contratos)

    if choice == 3:
      contrato = str(input('Número do contrato para teste:\n->'))
      testMakeGroup(contrato)

    if choice == 4:
      break
    else:
      pass

range1 = 1000
range2 = 1000

main(range1, range2)