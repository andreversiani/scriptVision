import os
import re

class Contrato:
  def __init__(self, numero_contrato: int, nome_concessionaria: str):
    self.numero = numero_contrato
    self.nome_concessionaria = nome_concessionaria

#cria os grupos passando a lista de contratos
def make_group(contratos: list, contrato_inicial: int, contrato_final: int) -> None:
  groups = ['VO Saude Seg Obra', 'VO Almoxarifado Obra', 'VO Administrativo Obra', 'VO Planejamento Obra']
  for contrato in contratos:
    for group in groups:
      comando = f'dsadd group "cn={contrato.numero} - {group}, ou={contrato.numero} - {contrato.nome_concessionaria}, ou={contrato_inicial} - {contrato_final}, ou=01 - Contratos, ou=Operacional (Contratos), ou=Grupos de Permissao, ou=VISION OU, dc=visionsistemas, dc=com, dc=br"'
      os.system(comando)
      print(f'Grupo criado: {contrato.numero} - {group}')

#cria as instancias de contratos em determinado range. Exemplo: 1000 - 1099
def make_contratos(range1: int, range2: int) -> list:
  pastas = os.listdir('.')
  contratos = []
  for pasta in pastas:
    if contrato_validator(pasta):
      numero_contrato = pasta[0:5]
      nome_concessionaria = pasta[7:len(pasta)+1]
      contrato  = Contrato(numero_contrato, nome_concessionaria)
      if int(numero_contrato) >= range1 and int(numero_contrato) <= range2:
        contratos.append(contrato)
        print(f'Contrato gerado: {contrato.numero} - {contrato.nome_concessionaria}')
      
  return contratos


#testa se os grupos estão sendo criados
def testmake_group(numero_contrato: int, contrato_inicial: int, contrato_final: int) -> None:
  contratos = make_contratos(numero_contrato, numero_contrato)
  make_group(contratos, contrato_inicial, contrato_final)

#adiciona as permissões de determinado range
def grantPermissions(range1: int, range2: int) -> None:
  new_groups = ['VO Saude Seg Obra', 'VO Almoxarifado Obra', 'VO Administrativo Obra', 'VO Planejamento Obra']
  existing_groups = ["VO - Equipe de Apoio", "VO - Amoxarifado de Apoio"]
  contratos = make_contratos(range1, range2)
  folderpath = os.getcwd()
  for contrato in contratos:
    folderpath += f'\{contrato.numero} - {contrato.nome_concessionaria}'
    for i in range(len(new_groups)):
      comando  = f'cmd /c "icacls {folderpath} /inheritance:e /grant:r "visionsistemas\{contrato.numero} - {new_groups[i]}:(OI)(CI)M"'
      os.system(comando)
      print(f'Permissão Garantida: {contrato.numero} - {new_groups[i]}')
    for j in range(len(existing_groups)):
      comando = f'cmd /c "icacls {folderpath} /inheritance:e /grant:r "visionsistemas\{existing_groups[j]}:(OI)(CI)M"'
      os.system(comando)
      print(f'Permissão Garantida: {contrato.numero} - {existing_groups[j]}')

def contrato_validator(contrato) -> bool:
  if re.fullmatch('[0-9]{4} - [A-zÀ-ÿ]*', contrato):
    return True
  return False

def main(range1, range2, contrato_inicial, contrato_final):
  while True:
    choice = int(input('1 - Fazer os grupos\n2 - Criar as pastas e dar permissão\n3 - Testar a criação de grupos\n4 - Sair\n-> '))
    if choice == 1:
      contratos = make_contratos(range1, range2)
      make_group(contratos, contrato_inicial, contrato_final)

    if choice == 2:
      grantPermissions(range1, range2)

    if choice == 3:
      contrato = str(input('Número do contrato para teste:\n->'))
      testmake_group(contrato, range1, range2)

    if choice == 4:
      break
    else:
      pass

range1 = 1000
range2 = 1000
contrato_inicial = 1000
contrato_final = 1099

main(range1, range2, contrato_inicial, contrato_final)